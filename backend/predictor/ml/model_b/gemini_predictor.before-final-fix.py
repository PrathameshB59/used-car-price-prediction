import json

from django.conf import settings
from google import genai
from google.genai import types
from tavily import TavilyClient


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

gemini_client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# ---------------------------------------------------------
# Tavily client
# ---------------------------------------------------------

tavily_client = TavilyClient(
    api_key=settings.TAVILY_API_KEY
)


# ---------------------------------------------------------
# Response schema
# ---------------------------------------------------------

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "estimated_price": {
            "type": "number",
            "description": "Estimated used car selling price in Indian Rupees."
        },
        "confidence": {
            "type": "string",
            "description": "Confidence level: Low, Medium, or High."
        },
        "reasoning": {
            "type": "string",
            "description": "Short explanation of the estimate using the available market data."
        },
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "url": {
                        "type": "string"
                    }
                },
                "required": [
                    "title",
                    "url"
                ]
            }
        },
        "search_method": {
            "type": "string",
            "description": "Search method used: gemini_google_search or tavily_fallback."
        },
    },
    "required": [
        "estimated_price",
        "confidence",
        "reasoning",
        "sources",
        "search_method",
    ],
}


# ---------------------------------------------------------
# Build the common car prompt
# ---------------------------------------------------------

def build_prompt(car_data, web_data=""):
    """
    Build the prompt used by Gemini.

    web_data contains information collected from the internet.
    """

    return f"""
You are an AI assistant helping estimate the selling price
of a used car in India.

Analyze the following car:

Car details:
{car_data}

Use current Indian used-car market information when available.

{web_data}

Important instructions:

1. Estimate a realistic selling price in Indian Rupees.
2. Consider:
   - car age
   - kilometres driven
   - fuel type
   - transmission
   - ownership
   - brand/model demand
   - current used-car market prices
3. Do not blindly copy one listing.
4. Compare multiple market signals when available.
5. Give a short explanation for the estimate.
6. Return ONLY JSON matching the requested schema.
"""


# ---------------------------------------------------------
# Primary method:
# Gemini + Google Search
# ---------------------------------------------------------

def predict_with_gemini_search(car_data):
    """
    Primary prediction method.

    Gemini performs the search itself using Google Search grounding.
    """

    prompt = build_prompt(
        car_data,
        """
Gemini has access to Google Search grounding.

Search the web for relevant current used-car prices
and use those results in your analysis.
"""
    )

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    response = gemini_client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[grounding_tool],
            response_mime_type="application/json",
            response_schema=RESPONSE_SCHEMA,
        ),
    )

    result = json.loads(response.text)
    result["search_method"] = "gemini_google_search"

    return result


# ---------------------------------------------------------
# Fallback method:
# Tavily Search -> Gemini
# ---------------------------------------------------------

def predict_with_tavily_fallback(car_data):
    """
    Fallback prediction method.

    Strategy:

    1. Search multiple market queries using Tavily.
    2. Collect results from different search angles.
    3. Remove duplicate and weak sources.
    4. Give the cleaned market evidence to Gemini.
    5. Gemini produces the final price estimate.
    """

    brand = car_data.get("Brand", "")
    model = car_data.get("model", "")
    year = car_data.get("Year", "")
    km_driven = car_data.get("kmDriven", "")

    # -----------------------------------------------------
    # Build multiple search queries
    # -----------------------------------------------------

    fuel_type = car_data.get("FuelType", "")
    transmission = car_data.get("Transmission", "")
    owner = car_data.get("Owner", "")

    queries = [
        (
            f"{year} {brand} {model} {fuel_type} "
            f"{transmission} used car price India "
            f"{km_driven} km"
        ),
        (
            f"{year} {brand} {model} {fuel_type} "
            f"second hand car price India"
        ),
        (
            f"{brand} {model} {year} {fuel_type} "
            f"used car valuation India"
        ),
    ]

    # -----------------------------------------------------
    # Search Tavily
    # -----------------------------------------------------

    all_results = []

    for query in queries:

        print(f"Tavily search: {query}")

        search_response = tavily_client.search(
            query=query,
            max_results=5,
            search_depth="advanced",
        )

        results = search_response.get("results", [])

        all_results.extend(results)

    # -----------------------------------------------------
    # Clean and deduplicate results
    # -----------------------------------------------------

    fuel_type = car_data.get("FuelType", "")

    seen_urls = set()

    cleaned_results = []

    weak_domains = [
        "facebook.com",
        "instagram.com",
        "youtube.com",
    ]

    for result in all_results:

        title = result.get("title", "").strip()
        url = result.get("url", "").strip()
        content = result.get("content", "").strip()

        # 1. Skip results without URL
        if not url:
            continue

        # 2. Skip duplicate URLs
        if url in seen_urls:
            continue

        # 3. Skip weak/social sources
        if any(domain in url.lower() for domain in weak_domains):
            continue

        # 4. Skip results without content
        if not content:
            continue

        # -------------------------------------------------
        # 5. Remove obvious fuel-type mismatches
        # -------------------------------------------------

        text = f"{title} {content}".lower()

        if fuel_type:

            fuel_lower = fuel_type.lower()

            opposite_fuel = {
                "petrol": "diesel",
                "diesel": "petrol",
            }.get(fuel_lower)

            if opposite_fuel and opposite_fuel in text:
                continue

        # -------------------------------------------------
        # Result passed all filters
        # -------------------------------------------------

        seen_urls.add(url)

        cleaned_results.append({
            "title": title,
            "url": url,
            "content": content,
            "score": result.get("score", 0),
        })

    # -----------------------------------------------------
    # Sort by Tavily relevance score
    # -----------------------------------------------------

    cleaned_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # Keep the strongest evidence
    cleaned_results = cleaned_results[:10]
    
    print("\n========== FINAL TAVILY EVIDENCE ==========")

    for i, result in enumerate(cleaned_results, 1):
        print(f"\n{i}. SCORE: {result['score']}")
        print("TITLE:", result["title"])
        print("URL:", result["url"])

    # -----------------------------------------------------
    # Convert search results into Gemini evidence
    # -----------------------------------------------------

    web_data_parts = []
    sources = []

    for result in cleaned_results:

        web_data_parts.append(
            f"""
SOURCE:
Title: {result["title"]}
URL: {result["url"]}
Relevance Score: {result["score"]}

Market Information:
{result["content"]}
"""
        )

        sources.append({
            "title": result["title"],
            "url": result["url"],
        })

    web_data = "\n".join(web_data_parts)

    # -----------------------------------------------------
    # Ask Gemini to analyze the market evidence
    # -----------------------------------------------------

    prompt = build_prompt(
        car_data,
        f"""
The following information was collected from multiple
live web searches using Tavily.

Use these sources as market evidence.

Important:

- Compare multiple listings.
- Do not blindly copy one price.
- Prefer listings matching the same year and model.
- Consider mileage when comparable mileage is available.
- Consider ownership, fuel type and transmission.
- Treat asking prices as market signals, not guaranteed
  transaction prices.
- Ignore unreliable or irrelevant information.

MARKET EVIDENCE:

{web_data}
"""
    )

    response = gemini_client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RESPONSE_SCHEMA,
        ),
    )

    result = json.loads(response.text)

    # -----------------------------------------------------
    # Important:
    # Keep URLs returned by Tavily.
    # Do not allow Gemini to invent source URLs.
    # -----------------------------------------------------

    result["sources"] = sources

    return result


# ---------------------------------------------------------
# Main prediction function
# ---------------------------------------------------------

def predict_with_gemini(car_data):
    """
    Predict used-car price.

    Strategy:

    1. Try Gemini + Google Search.
    2. If that fails, use Tavily Search.
    3. Give Tavily results to Gemini.
    """

    try:
        print("Trying Gemini Google Search...")

        result = predict_with_gemini_search(car_data)

        print("Gemini Google Search succeeded.")

        return result

    except Exception as gemini_search_error:

        print(
            "Gemini Google Search failed:"
        )
        print(
            gemini_search_error
        )

        print(
            "Switching to Tavily search fallback..."
        )

        return predict_with_tavily_fallback(car_data)
