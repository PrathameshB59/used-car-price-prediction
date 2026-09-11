(function () {
    "use strict";

    const STORAGE_KEY = "autovalue_predictions";

    function getResults() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
        } catch (error) {
            console.error("Could not read prediction history:", error);
            return [];
        }
    }

    function saveResult(result) {
        const results = getResults();

        results.unshift({
            id: Date.now(),
            createdAt: new Date().toISOString(),
            html: result
        });

        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(results.slice(0, 20))
        );
    }

    function clearResults() {
        localStorage.removeItem(STORAGE_KEY);
        renderResults();
    }

    function renderResults() {
        const container = document.getElementById("results-dashboard");

        if (!container) {
            return;
        }

        const results = getResults();

        if (!results.length) {
            container.innerHTML = `
                <div class="results-empty">
                    <div class="results-empty-icon">◈</div>
                    <h2>No predictions yet</h2>
                    <p>
                        Your completed valuations will appear here
                        automatically after your first prediction.
                    </p>
                    <a href="#predict" class="results-predict-link">
                        Predict a car →
                    </a>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="results-header">
                <div>
                    <p class="eyebrow">PREDICTION HISTORY</p>
                    <h2>Previous valuations</h2>
                    <p>
                        Your recent Model A vs Model B predictions
                        are stored locally in this browser.
                    </p>
                </div>

                <button
                    type="button"
                    id="clear-results"
                    class="results-clear"
                >
                    Clear history
                </button>
            </div>

            <div class="results-list">
                ${results.map((item, index) => `
                    <article class="history-card">
                        <div class="history-card-top">
                            <span>Prediction #${results.length - index}</span>
                            <time>
                                ${new Date(item.createdAt).toLocaleString()}
                            </time>
                        </div>

                        <div class="history-content">
                            ${item.html}
                        </div>
                    </article>
                `).join("")}
            </div>
        `;

        document
            .getElementById("clear-results")
            ?.addEventListener("click", clearResults);
    }

    function initResultsPage() {
        renderResults();
    }

    window.AutoValueResults = {
        saveResult,
        renderResults,
        initResultsPage
    };
})();
