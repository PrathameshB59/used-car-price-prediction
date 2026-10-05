/*
 * AutoValue AI
 * ============================================================
 * Playwright prediction-flow regression test.
 *
 * PURPOSE:
 * Verify that a real browser shows the loading state before the
 * prediction response is displayed.
 *
 * WHY:
 * Model B may take several seconds because it can use external
 * AI/search services. The loading screen must therefore appear
 * immediately after the user submits the form.
 *
 * TEST STRATEGY:
 * The API response is mocked and deliberately delayed.
 * This makes the test deterministic and avoids calling Gemini
 * or Tavily during normal automated testing.
 */

import { test, expect } from "@playwright/test";


test("prediction shows loading state before results", async ({ page }) => {
    /*
     * Open the Predict route.
     */
    await page.goto(
        "http://127.0.0.1:8000/#predict"
    );


    /*
     * Fill the form using values that actually exist in the
     * current HTML select options.
     *
     * WHY:
     * The test should exercise the real form instead of inventing
     * values that the user cannot select.
     */
    await page.locator("#brand").selectOption({
        label: "Toyota"
    });

    await page.locator("#model").selectOption({
        label: "Fortuner"
    });

    await page.locator("#year").fill("2021");

    await page.locator("#kmDriven").fill("42000");

    await page.locator("#transmission").selectOption({
        label: "Manual"
    });

    await page.locator("#owner").selectOption({
        label: "First Owner"
    });

    await page.locator("#sellerType").selectOption({
        label: "Dealer"
    });

    await page.locator("#fuelType").selectOption({
        label: "Diesel"
    });


    /*
     * Intercept the prediction API.
     *
     * WHY:
     * We deliberately delay the response so Playwright has time
     * to verify that the loading overlay appears before results.
     *
     * This does NOT call Gemini or Tavily.
     */
    await page.route(
        "**/api/predict/",
        async (route) => {

            await new Promise(
                (resolve) => setTimeout(resolve, 1500)
            );

            await route.fulfill({
                status: 200,

                contentType:
                    "application/json",

                body: JSON.stringify({
                    status: "success",

                    car: {
                        brand: "Toyota",
                        model: "Fortuner",
                        year: 2021,
                        age: 5,
                        km_driven: 42000,
                        transmission: "Manual",
                        owner: "First Owner",
                        fuel_type: "Diesel",
                        seller_type: "Dealer"
                    },

                    model_a: {
                        estimated_price: 842000
                    },

                    model_b: {
                        estimated_price: 875000,
                        confidence: "Medium",
                        reasoning:
                            "Mocked market evidence.",
                        sources: [],
                        search_method: "mock"
                    },

                    comparison: {
                        difference: 33000,
                        difference_percent: 3.92,
                        higher_model: "Model B"
                    }
                })
            });
        }
    );


    /*
     * Submit the real prediction form.
     */
    await page.locator(
        "#predictionForm button[type='submit']"
    ).click();


    /*
     * IMPORTANT REGRESSION CHECK.
     *
     * The actual HTML id is:
     * #predictionLoadingOverlay
     *
     * This must become visible BEFORE the delayed API response
     * arrives.
     */
    await expect(
        page.locator("#predictionLoadingOverlay")
    ).toBeVisible();


    /*
     * After the mocked response arrives, the loading overlay
     * should disappear.
     */
    await expect(
        page.locator("#predictionLoadingOverlay")
    ).toBeHidden();


    /*
     * Successful prediction should navigate to Results.
     */
    await expect(page).toHaveURL(
        /#results/
    );
});