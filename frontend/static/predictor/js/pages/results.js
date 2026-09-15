(function () {
    "use strict";

    const STORAGE_KEY = "autovalue_predictions";

    function getResults() {
        try {
            return JSON.parse(
                localStorage.getItem(STORAGE_KEY)
            ) || [];
        } catch (error) {
            console.error(
                "Could not read prediction history:",
                error
            );

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
        const container =
            document.getElementById("results-dashboard");

        if (!container) {
            return;
        }

        const results = getResults();

        if (!results.length) {
            container.innerHTML = `
                <div class="results-empty">
                    <div class="results-empty-icon">◈</div>

                    <p class="results-empty-label">
                        NO HISTORY
                    </p>

                    <h2>
                        No predictions yet
                    </h2>

                    <p>
                        Complete your first vehicle price prediction
                        and it will appear here automatically.
                    </p>

                    <a
                        href="#predict"
                        class="results-predict-link"
                    >
                        Predict a car →
                    </a>
                </div>
            `;

            bindResultsNavigation();
            return;
        }

        container.innerHTML = `
            <div class="results-header">

                <div>
                    <p class="eyebrow">
                        PREDICTION HISTORY
                    </p>

                    <h2>
                        Previous predictions
                    </h2>

                    <p>
                        Your recent ${window.AutoValueConfig.modelA.name}
                                    vs
                                    ${window.AutoValueConfig.modelB.name}
                        predictions are stored locally
                        in this browser.
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

                            <span>
                                Prediction #${results.length - index}
                            </span>

                            <time>
                                ${new Date(
                                    item.createdAt
                                ).toLocaleString()}
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
            ?.addEventListener(
                "click",
                clearResults
            );

        bindResultsNavigation();
    }

    function bindResultsNavigation() {
        const links = document.querySelectorAll(
            '.results-page a[href="#predict"]'
        );

        links.forEach((link) => {
            link.addEventListener(
                "click",
                handleBackToPrediction
            );
        });

        const backButton =
            document.getElementById(
                "results-back-button"
            );

        if (backButton) {
            backButton.addEventListener(
                "click",
                handleBackToPrediction
            );
        }
    }

    function handleBackToPrediction(event) {
        event.preventDefault();

        /*
         * Results is a separately loaded frontend page.
         * Reloading the Django page gives us a clean,
         * server-rendered prediction form again.
         */
        window.location.hash = "predict";
        window.location.reload();
    }

    async function loadResultsPage() {
        const page =
            document.querySelector(".page");

        if (!page) {
            return;
        }

        try {
            const response = await fetch(
                "/static/predictor/pages/results.html",
                {
                    cache: "no-cache"
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Could not load Results page (${response.status}).`
                );
            }

            const html = await response.text();

            page.innerHTML = html;

            document.title =
                "Prediction Results | AutoValue AI";

            renderResults();

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        } catch (error) {
            console.error(
                "Results page error:",
                error
            );

            page.innerHTML = `
                <section class="results-page">
                    <div class="results-page-shell">

                        <div class="results-empty">

                            <p class="results-empty-label">
                                RESULTS ERROR
                            </p>

                            <h1>
                                Could not load results
                            </h1>

                            <p>
                                ${error.message}
                            </p>

                            <a
                                href="#predict"
                                class="results-predict-link"
                            >
                                ← Back to prediction
                            </a>

                        </div>

                    </div>
                </section>
            `;

            bindResultsNavigation();
        }
    }

    function handleRoute() {
        const hash =
            window.location.hash.replace(
                "#",
                ""
            );

        if (hash !== "results") {
            return;
        }

        loadResultsPage();
    }

    function setupNavigation() {
        const links = document.querySelectorAll(
            'a[href="#results"], [data-page="results"]'
        );

        links.forEach((link) => {
            link.addEventListener(
                "click",
                (event) => {
                    event.preventDefault();

                    if (
                        window.location.hash ===
                        "#results"
                    ) {
                        loadResultsPage();
                    } else {
                        window.location.hash =
                            "results";
                    }
                }
            );
        });
    }

    window.AutoValueResults = {
        saveResult,
        renderResults,
        initResultsPage: loadResultsPage
    };

    window.addEventListener(
        "hashchange",
        handleRoute
    );

    document.addEventListener(
        "DOMContentLoaded",
        () => {
            setupNavigation();
            handleRoute();
        }
    );
})();
