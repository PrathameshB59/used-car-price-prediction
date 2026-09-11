(function () {
    "use strict";

    const PAGE_URL = "/static/predictor/pages/how-it-works.html";

    async function loadPage() {
        const response = await fetch(PAGE_URL, {
            cache: "no-cache"
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const html = await response.text();

        const doc = new DOMParser().parseFromString(
            html,
            "text/html"
        );

        const page = doc.querySelector(".how-it-works-page");

        if (!page) {
            throw new Error(
                "Missing .how-it-works-page in how-it-works.html"
            );
        }

        return page.outerHTML;
    }

    async function showHowItWorks() {
        const main =
            document.querySelector("main.page") ||
            document.querySelector("main") ||
            document.querySelector(".page");

        if (!main) {
            console.error(
                "How It Works: main content container not found."
            );
            return;
        }

        try {
            main.classList.add("page-loading");

            main.innerHTML = await loadPage();

            main.classList.remove("page-loading");

            document.title = "How It Works | AutoValue AI";

        } catch (error) {
            console.error(
                "How It Works page failed:",
                error
            );

            main.classList.remove("page-loading");

            main.innerHTML = `
                <section class="how-it-works-page">
                    <div class="how-hero">
                        <p class="page-eyebrow">
                            AUTOVALUE AI
                        </p>

                        <h1>
                            How the valuation works
                        </h1>

                        <p class="page-subtitle">
                            The How It Works page could not be loaded.
                            Please refresh the application.
                        </p>
                    </div>
                </section>
            `;
        }
    }

    function handleRoute() {
        const route =
            window.location.hash.replace("#", "");

        if (route === "how-it-works") {
            showHowItWorks();
        }
    }

    window.initHowItWorksPage = showHowItWorks;

    window.addEventListener(
        "hashchange",
        handleRoute
    );

    document.addEventListener(
        "DOMContentLoaded",
        handleRoute
    );

})();
