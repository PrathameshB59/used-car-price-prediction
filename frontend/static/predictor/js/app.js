/*
 * AutoValue AI
 * ============================================================
 * Frontend application shell.
 *
 * WHY:
 * The Django backend should remain responsible for prediction.
 * This JavaScript controls only frontend page presentation.
 *
 * Routes:
 *   #dashboard
 *   #predict
 *   #results
 *   #how-it-works
 */

(function initializeApp() {
    const app = document.getElementById("app");

    if (!app) {
        return;
    }

    const routes = {
        dashboard: "/static/predictor/pages/dashboard.html",
        predict: "/static/predictor/pages/predict.html",
        results: "/static/predictor/pages/results.html",
        "how-it-works":
            "/static/predictor/pages/how-it-works.html"
    };

    /*
     * Purpose:
     * Convert the browser hash into a safe application route.
     *
     * Returns:
     * One of the known route names.
     */
    function getRoute() {
        const requested =
            window.location.hash
                .replace("#", "")
                .trim();

        return routes[requested]
            ? requested
            : "dashboard";
    }

    /*
     * Purpose:
     * Build the common application header.
     *
     * WHY:
     * Every page should share the same navigation and theme
     * control instead of duplicating header markup.
     */
    function renderShell(pageHtml, route) {
        app.innerHTML = `
            <div class="app-shell">

                <header class="app-header">
                    <div class="header-inner">

                        <a
                            class="brand"
                            href="#dashboard"
                            aria-label="AutoValue AI home"
                        >
                            <span class="brand-mark">
                                🚗
                            </span>

                            <span>
                                <span class="brand-text">
                                    AutoValue AI
                                </span>

                                <span class="brand-subtitle">
                                    Used Car Intelligence
                                </span>
                            </span>
                        </a>

                        <nav
                            class="main-nav"
                            aria-label="Main navigation"
                        >
                            ${renderNav(route)}
                        </nav>

                        <div class="header-actions">

                            <button
                                class="icon-button"
                                id="theme-toggle"
                                type="button"
                                aria-label="Toggle color theme"
                                title="Toggle light and dark mode"
                            >
                                ${getThemeIcon()}
                            </button>

                            <button
                                class="icon-button mobile-menu-button"
                                id="mobile-menu-button"
                                type="button"
                                aria-label="Open navigation menu"
                                aria-expanded="false"
                            >
                                ☰
                            </button>

                        </div>

                    </div>

                    <nav
                        class="mobile-nav"
                        id="mobile-nav"
                        aria-label="Mobile navigation"
                    >
                        ${renderNav(route)}
                    </nav>
                </header>

                <main>
                    ${pageHtml}
                </main>

                <footer class="app-footer">
                    AutoValue AI · Machine Learning Based Used-Car Valuation
                </footer>

            </div>
        `;

        bindShellEvents();
    }

    /*
     * Purpose:
     * Generate navigation links.
     *
     * Returns:
     * Navigation HTML.
     */
    function renderNav(activeRoute) {
        const links = [
            ["dashboard", "Dashboard"],
            ["predict", "Predict"],
            ["results", "Results"],
            ["how-it-works", "How It Works"]
        ];

        return links
            .map(([routeName, label]) => `
                <a
                    class="nav-link ${
                        activeRoute === routeName
                            ? "active"
                            : ""
                    }"
                    href="#${routeName}"
                >
                    ${label}
                </a>
            `)
            .join("");
    }

    /*
     * Purpose:
     * Display the correct sun/moon icon.
     */
    function getThemeIcon() {
        if (
            window.AutoValueTheme &&
            window.AutoValueTheme.get() === "light"
        ) {
            return "☾";
        }

        return "☀";
    }

    /*
     * Purpose:
     * Connect common header controls.
     */
    function bindShellEvents() {
        const themeButton =
            document.getElementById("theme-toggle");

        if (themeButton) {
            themeButton.addEventListener(
                "click",
                () => {
                    window.AutoValueTheme.toggle();

                    themeButton.textContent =
                        getThemeIcon();
                }
            );
        }

        const menuButton =
            document.getElementById(
                "mobile-menu-button"
            );

        const mobileNav =
            document.getElementById("mobile-nav");

        if (menuButton && mobileNav) {
            menuButton.addEventListener(
                "click",
                () => {
                    const isOpen =
                        mobileNav.classList.toggle(
                            "is-open"
                        );

                    menuButton.setAttribute(
                        "aria-expanded",
                        String(isOpen)
                    );
                }
            );
        }

        /*
         * Close the mobile menu after navigation.
         */
        mobileNav?.querySelectorAll("a").forEach(
            (link) => {
                link.addEventListener(
                    "click",
                    () => {
                        mobileNav.classList.remove(
                            "is-open"
                        );

                        menuButton?.setAttribute(
                            "aria-expanded",
                            "false"
                        );
                    }
                );
            }
        );
    }

    /*
     * Purpose:
     * Load an individual frontend page.
     */
    async function loadRoute() {
        const route = getRoute();
        const pageUrl = routes[route];

        try {
            app.innerHTML = `
                <div class="page">
                    <div class="empty-state">
                        Loading AutoValue AI…
                    </div>
                </div>
            `;

            const response =
                await fetch(pageUrl);

            if (!response.ok) {
                throw new Error(
                    `Failed to load ${pageUrl}`
                );
            }

            const pageHtml =
                await response.text();

            renderShell(pageHtml, route);

            /*
             * Page-specific initialization.
             *
             * WHY:
             * Page logic remains separate rather than creating
             * one huge JavaScript file.
             */
            initializePage(route);

        } catch (error) {
            console.error(
                "AutoValue AI page loading error:",
                error
            );

            renderShell(
                `
                <div class="page">
                    <div class="empty-state">
                        <div class="empty-state-icon">
                            ⚠️
                        </div>

                        <h2>
                            Page could not be loaded
                        </h2>

                        <p>
                            The frontend page failed to load.
                            Please refresh the application.
                        </p>

                        <a
                            class="button button-primary"
                            href="#dashboard"
                        >
                            Return to Dashboard
                        </a>
                    </div>
                </div>
                `,
                "dashboard"
            );
        }
    }

    /*
     * Purpose:
     * Initialize optional page modules.
     */
    function initializePage(route) {
        if (
            route === "dashboard" &&
            window.AutoValueDashboard
        ) {
            window.AutoValueDashboard.init();
        }

        if (
            route === "predict" &&
            window.AutoValuePredict
        ) {
            window.AutoValuePredict.init();
        }

        if (
            route === "results" &&
            window.AutoValueResults
        ) {
            window.AutoValueResults.init();
        }

        if (
            route === "how-it-works" &&
            window.AutoValueHowItWorks
        ) {
            window.AutoValueHowItWorks.init();
        }
    }

    window.addEventListener(
        "hashchange",
        loadRoute
    );

    /*
     * Start the application.
     */
    loadRoute();
})();
