/*
 * AutoValue AI — Results Page
 * ------------------------------------------------------------
 * Purpose:
 *     Read the latest prediction returned by Django and render
 *     Model A, Model B, comparison, and vehicle information.
 *
 * Inputs:
 *     The latest API response stored in localStorage by predict.js.
 *
 * Output:
 *     A complete valuation result displayed inside #results-content.
 *
 * Why:
 *     Django performs the prediction. This file is responsible only
 *     for presenting the already-calculated result to the user.
 */

(function () {
    "use strict";

    const STORAGE_KEY = "autovalue-latest-result";

    /**
     * Format an Indian Rupee value for display.
     *
     * Input:
     *     Numeric price.
     *
     * Output:
     *     Formatted string such as "₹8,42,000".
     */
    function formatPrice(value) {
        const number = Number(value);

        if (!Number.isFinite(number)) {
            return "Not available";
        }

        return new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0,
        }).format(number);
    }

    /**
     * Escape text before inserting it into HTML.
     *
     * Why:
     *     Vehicle values ultimately originate from user input or
     *     external services. Escaping prevents accidental HTML
     *     injection when rendering those values.
     */
    function escapeHtml(value) {
        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    /**
     * Create the HTML used for a successful or partial valuation.
     *
     * Input:
     *     API response object.
     *
     * Output:
     *     HTML string for the Results page.
     */
    function buildResultsHtml(result) {
        const car = result.car || {};
        const modelA = result.model_a;
        const modelB = result.model_b;
        const comparison = result.comparison;

        const modelAAvailable = modelA !== null && modelA !== undefined;
        const modelBAvailable =
            modelB &&
            modelB.estimated_price !== null &&
            modelB.estimated_price !== undefined;

        const status = result.status || "error";

        const modelBPrice = modelBAvailable
            ? formatPrice(modelB.estimated_price)
            : "Not available";

        const comparisonHtml = comparison
            ? `
                <section class="result-comparison">
                    <div class="result-section-heading">
                        <span>Price Comparison</span>
                    </div>

                    <div class="comparison-grid">
                        <div class="comparison-item">
                            <span>Difference</span>
                            <strong>${formatPrice(comparison.difference)}</strong>
                        </div>

                        <div class="comparison-item">
                            <span>Difference %</span>
                            <strong>${escapeHtml(comparison.difference_percent)}%</strong>
                        </div>

                        <div class="comparison-item">
                            <span>Higher Estimate</span>
                            <strong>${escapeHtml(comparison.higher_model)}</strong>
                        </div>
                    </div>
                </section>
            `
            : "";

        const modelBDetails = modelBAvailable
            ? `
                <div class="model-details">
                    ${
                        modelB.confidence
                            ? `<p><strong>Confidence:</strong> ${escapeHtml(modelB.confidence)}</p>`
                            : ""
                    }

                    ${
                        modelB.search_method
                            ? `<p><strong>Search:</strong> ${escapeHtml(modelB.search_method)}</p>`
                            : ""
                    }

                    ${
                        modelB.reasoning
                            ? `<p><strong>Reasoning:</strong> ${escapeHtml(modelB.reasoning)}</p>`
                            : ""
                    }
                </div>
            `
            : `
                <div class="model-unavailable">
                    Market AI estimate is currently unavailable.
                </div>
            `;

        const modelAError = result.model_a_error
            ? `
                <div class="model-error">
                    ${escapeHtml(result.model_a_error)}
                </div>
            `
            : "";

        const modelBError = result.model_b_error
            ? `
                <div class="model-error">
                    ${escapeHtml(result.model_b_error)}
                </div>
            `
            : "";

        return `
            <div class="valuation-result">

                <div class="result-header">
                    <div>
                        <span class="eyebrow">VALUATION RESULT</span>

                        <h1>
                            ${escapeHtml(car.year)}
                            ${escapeHtml(car.brand)}
                            ${escapeHtml(car.model)}
                        </h1>

                        <p class="vehicle-summary">
                            ${escapeHtml(car.fuel_type)}
                            ·
                            ${escapeHtml(car.transmission)}
                            ·
                            ${escapeHtml(car.owner)}
                        </p>
                    </div>

                    <span class="result-status result-status-${escapeHtml(status)}">
                        ${escapeHtml(status)}
                    </span>
                </div>

                <div class="result-model-grid">

                    <article class="result-model-card">
                        <span class="model-label">MODEL A</span>

                        <h2>ML Price Estimate</h2>

                        <div class="result-price">
                            ${
                                modelAAvailable
                                    ? formatPrice(modelA)
                                    : "Not available"
                            }
                        </div>

                        <p>
                            Random Forest estimate based on the
                            trained historical-data model.
                        </p>

                        ${modelAError}
                    </article>

                    <article class="result-model-card">
                        <span class="model-label">MODEL B</span>

                        <h2>Market AI Estimate</h2>

                        <div class="result-price">
                            ${modelBPrice}
                        </div>

                        <p>
                            Gemini market analysis supported by
                            web evidence.
                        </p>

                        ${modelBDetails}
                        ${modelBError}
                    </article>

                </div>

                ${comparisonHtml}

                <div class="result-actions">
                    <a href="#predict" class="btn btn-primary">
                        Predict Another Car
                    </a>

                    <a href="#dashboard" class="btn btn-secondary">
                        Back to Dashboard
                    </a>
                </div>

            </div>
        `;
    }

    /**
     * Show the empty Results state.
     *
     * Output:
     *     A helpful message when no prediction exists yet.
     */
    function renderEmptyState(container) {
        container.innerHTML = `
            <div class="empty-state">
                <span class="eyebrow">NO VALUATION YET</span>

                <h1>No prediction available</h1>

                <p>
                    Enter your vehicle details first to generate
                    an ML and Market AI valuation.
                </p>

                <a href="#predict" class="btn btn-primary">
                    Start Valuation
                </a>
            </div>
        `;
    }

    /**
     * Initialize the Results page.
     *
     * Reads the latest API response from localStorage and renders it.
     */
    function init() {
        const container = document.getElementById("results-content");

        if (!container) {
            return;
        }

        const storedResult = localStorage.getItem(STORAGE_KEY);

        if (!storedResult) {
            renderEmptyState(container);
            return;
        }

        try {
            const result = JSON.parse(storedResult);

            if (!result || typeof result !== "object") {
                renderEmptyState(container);
                return;
            }

            if (result.status === "error") {
                container.innerHTML = `
                    <div class="empty-state">
                        <span class="eyebrow">VALUATION ERROR</span>

                        <h1>Prediction could not be completed</h1>

                        <p>
                            The prediction service could not produce
                            a valuation. Please try again.
                        </p>

                        <a href="#predict" class="btn btn-primary">
                            Try Again
                        </a>
                    </div>
                `;

                return;
            }

            container.innerHTML = buildResultsHtml(result);
        } catch (error) {
            console.error("Could not read stored prediction:", error);
            renderEmptyState(container);
        }
    }

    window.AutoValueResults = {
        init,
    };
})();