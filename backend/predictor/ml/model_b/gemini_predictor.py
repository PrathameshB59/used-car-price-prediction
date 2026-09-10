import json

from django.conf import settings
from google import genai
from google.genai import types
from tavily import TavilyClient


# =========================================================
# Gemini clients
# =========================================================

# ---------------------------------------------------------
# Gemini clients
# ---------------------------------------------------------

primary_gemini_client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

backup_gemini_client = genai.Client(
    api_key=settings.GEMINI_BACKUP_API_KEY
)


# =========================================================
# Tavily client
# =========================================================

tavily_client = TavilyClient(
    api_key=settings.TAVILY_API_KEY
)


# =========================================================
# Response schema
# =========================================================

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "estimated_price": {
            "type": "number",
            "description": (
                "Estimated used car selling price "
                "in Indian Rupees."
            ),
        },
        "confidence": {
            "type": "string",
            "description": (
                "Confidence level: Low, Medium, or High."
            ),
        },
        "reasoning": {
            "type": "string",
            "description": (
                "Short explanation of the estimate "
                "using the available market data."
            ),
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
                    },
                },
                "required": [
                    "title",
                    "url",
                ],
            },
        },
        "search_method": {
            "type": "string",
            "description": (
                "Search method used by Model B."
            ),
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


# =========================================================
# Gemini generation helper
# =========================================================

def generate_json_response(
    prompt,
    model_name,
    client,
    tools=None,
):
    """
    Generate a structured JSON response using Gemini.

    client:
        The Gemini account to use.

    model_name:
        The Gemini model to use.

    tools:
        Optional Gemini tools such as Google Search.
    """

    config_kwargs = {
        "response_mime_type": "application/json",
        "response_schema": RESPONSE_SCHEMA,
    }

    if tools:
        config_kwargs["tools"] = tools

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            **config_kwargs
        ),
    )

    return response

# =========================================================
# Common Gemini prompt
# =========================================================

def build_prompt(car_data, web_data=""):
    """
    Build the common prompt used by Gemini.
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


# =========================================================
# Gemini + Google Search
# =========================================================

def predict_with_gemini_search(
    car_data,
    client,
    model_name,
):
    """
    Ask a specific Gemini account/model to perform
    the prediction using Google Search grounding.

    This function receives the client and model explicitly.

    That is important because we have TWO Gemini accounts.
    """

    prompt = build_prompt(
        car_data,
        """
Use Google Search grounding to search the web for
relevant current Indian used-car prices.

Search multiple sources when possible.

Use the search results as market evidence.
"""
    )

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    response = generate_json_response(
        prompt=prompt,
        model_name=model_name,
        tools=[grounding_tool],
        client=client,
    )

    result = json.loads(response.text)

    result["search_method"] = (
        "gemini_google_search"
    )

    return result


# =========================================================
# Tavily fallback
# =========================================================

def predict_with_tavily_fallback(car_data):
    """
    Fallback prediction strategy:

    1. Search the used-car market with Tavily.
    2. Collect multiple market sources.
    3. Remove duplicate/weak sources.
    4. Send the evidence to the backup Gemini account.
    5. Gemini produces the final estimate.
    """

    brand = car_data.get("Brand", "")
    model = car_data.get("model", "")
    year = car_data.get("Year", "")
    km_driven = car_data.get("kmDriven", "")

    fuel_type = car_data.get("FuelType", "")
    transmission = car_data.get("Transmission", "")
    owner = car_data.get("Owner", "")

    # -----------------------------------------------------
    # Build search queries
    # -----------------------------------------------------

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
    # Tavily search
    # -----------------------------------------------------

    all_results = []

    for query in queries:

        print(
            f"Tavily search: {query}"
        )

        search_response = tavily_client.search(
            query=query,
            max_results=5,
            search_depth="advanced",
        )

        results = search_response.get(
            "results",
            []
        )

        all_results.extend(results)

    # -----------------------------------------------------
    # Clean and deduplicate
    # -----------------------------------------------------

    seen_urls = set()
    cleaned_results = []

    weak_domains = [
        "facebook.com",
        "instagram.com",
        "youtube.com",
    ]

    for result in all_results:

        title = result.get(
            "title",
            ""
        ).strip()

        url = result.get(
            "url",
            ""
        ).strip()

        content = result.get(
            "content",
            ""
        ).strip()

        # Skip results without URL
        if not url:
            continue

        # Skip duplicate URLs
        if url in seen_urls:
            continue

        # Skip social media sources
        if any(
            domain in url.lower()
            for domain in weak_domains
        ):
            continue

        # Skip results without useful content
        if not content:
            continue

        # -------------------------------------------------
        # Remove obvious fuel mismatches
        # -------------------------------------------------

        text = (
            f"{title} {content}"
        ).lower()

        if fuel_type:

            fuel_lower = fuel_type.lower()

            opposite_fuel = {
                "petrol": "diesel",
                "diesel": "petrol",
            }.get(fuel_lower)

            if (
                opposite_fuel
                and opposite_fuel in text
            ):
                continue

        seen_urls.add(url)

        cleaned_results.append({
            "title": title,
            "url": url,
            "content": content,
            "score": result.get(
                "score",
                0
            ),
        })

    # -----------------------------------------------------
    # Sort by Tavily relevance
    # -----------------------------------------------------

    cleaned_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # Keep strongest 10 sources
    cleaned_results = cleaned_results[:10]

    print(
        "\n========== FINAL TAVILY EVIDENCE =========="
    )

    for i, result in enumerate(
        cleaned_results,
        1
    ):

        print(
            f"\n{i}. SCORE: "
            f"{result['score']}"
        )

        print(
            "TITLE:",
            result["title"]
        )

        print(
            "URL:",
            result["url"]
        )

    # -----------------------------------------------------
    # Convert evidence for Gemini
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

    web_data = "\n".join(
        web_data_parts
    )

    # -----------------------------------------------------
    # Ask backup Gemini to analyze Tavily evidence
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

    response = generate_json_response(
        prompt=prompt,
        model_name=settings.GEMINI_BACKUP_MODEL,
        client=backup_gemini_client,
    )

    result = json.loads(
        response.text
    )

    result["search_method"] = (
        "tavily_fallback"
    )

    result["model_used"] = (
        settings.GEMINI_BACKUP_MODEL
    )

    result["fallback_used"] = True

    # -----------------------------------------------------
    # Keep Tavily's real URLs.
    # Do not allow Gemini to invent URLs.
    # -----------------------------------------------------

    result["sources"] = sources

    return result


# =========================================================
# Main Model B prediction
# =========================================================

def predict_with_gemini(car_data):
    """
    Predict used-car price using Model B.

    Fallback order:

    1. Primary Gemini account + Google Search
    2. Backup Gemini account + Google Search
    3. Tavily + backup Gemini

    Both Gemini accounts use the same model:
    gemini-3.6-flash

    The API keys are different, so if the primary account
    hits a quota/rate-limit/problem, the backup account
    can be used.
    """

    primary_model = settings.GEMINI_MODEL
    backup_model = settings.GEMINI_BACKUP_MODEL

    # -----------------------------------------------------
    # 1. PRIMARY GEMINI ACCOUNT
    # -----------------------------------------------------

    try:

        print()
        print("=" * 60)
        print("MODEL B: PRIMARY GEMINI")
        print("=" * 60)

        print(
            f"Primary model: {primary_model}"
        )

        result = predict_with_gemini_search(
            car_data,
            primary_gemini_client,
            primary_model,
        )

        result["model_used"] = primary_model
        result["fallback_used"] = False
        result["account_used"] = "primary"

        print(
            f"Primary Gemini succeeded: "
            f"{primary_model}"
        )

        return result

    except Exception as primary_error:

        print()
        print(
            f"Primary Gemini failed "
            f"({primary_model})"
        )

        print(
            f"Error: {primary_error}"
        )

    # -----------------------------------------------------
    # 2. BACKUP GEMINI ACCOUNT
    # -----------------------------------------------------

    try:

        print()
        print("=" * 60)
        print("MODEL B: BACKUP GEMINI")
        print("=" * 60)

        print(
            f"Backup model: {backup_model}"
        )

        result = predict_with_gemini_search(
            car_data,
            backup_gemini_client,
            backup_model,
        )

        result["model_used"] = backup_model
        result["fallback_used"] = True
        result["account_used"] = "backup"

        print(
            f"Backup Gemini succeeded: "
            f"{backup_model}"
        )

        return result

    except Exception as backup_error:

        print()
        print(
            f"Backup Gemini failed "
            f"({backup_model})"
        )

        print(
            f"Error: {backup_error}"
        )

    # -----------------------------------------------------
    # 3. TAVILY FALLBACK
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("MODEL B: TAVILY FALLBACK")
    print("=" * 60)

    print(
        "Both Gemini accounts failed."
    )

    print(
        "Switching to Tavily market research."
    )

    result = predict_with_tavily_fallback(
        car_data
    )

    result["model_used"] = "tavily"
    result["fallback_used"] = True
    result["account_used"] = "tavily"

    return result
