/*
 * AutoValue AI
 * ============================================================
 * Prediction page module.
 *
 * PURPOSE:
 * Connect the Predict form to the Django JSON prediction API.
 *
 * WHY:
 * The browser was performing a normal form submission, producing
 * GET /?brand=... instead of POST /api/predict/.
 *
 * This module takes control of the form submission, sends JSON
 * to Django, stores the returned valuation, and opens Results.
 *
 * ARCHITECTURE:
 *
 * Predict form
 *     ↓
 * preventDefault()
 *     ↓
 * POST /api/predict/
 *     ↓
 * Django Model A + Model B
 *     ↓
 * JSON response
 *     ↓
 * localStorage
 *     ↓
 * Results page
 */

(function initializePredictModule() {

    /*
     * Purpose:
     * Expose the prediction page functionality to app.js.
     */
    window.AutoValuePredict = {

        /*
         * Purpose:
         * Find the prediction form and attach its submit handler.
         *
         * Inputs:
         * None.
         *
         * Output:
         * None. The function attaches browser event listeners.
         */
        init() {

            const form = document.getElementById(
                "predictionForm"
            );

            /*
             * WHY:
             * app.js initializes this module on every route.
             * The form only exists on #predict.
             */
            if (!form) {
                return;
            }

            /*
             * Prevent duplicate listeners if the user visits
             * the Predict page more than once.
             */
            if (form.dataset.predictInitialized === "true") {
                return;
            }

            form.dataset.predictInitialized = "true";

            form.addEventListener(
                "submit",
                handleSubmit
            );

            /*
             * Calculate vehicle age automatically whenever
             * the year changes.
             */
            const yearInput =
                document.getElementById("year");

            const ageInput =
                document.getElementById("age");

            if (yearInput && ageInput) {

                yearInput.addEventListener(
                    "input",
                    updateAge
                );

                updateAge();
            }
        }
    };


    /*
     * Purpose:
     * Handle the Predict form submission.
     *
     * Inputs:
     * event: Browser submit event.
     *
     * Output:
     * Sends one JSON POST request to Django.
     */
    async function handleSubmit(event) {

        /*
         * THIS IS THE IMPORTANT FIX.
         *
         * Without this line, the browser performs its normal
         * HTML form submission and reloads /?brand=...
         */
        event.preventDefault();

        const form = event.currentTarget;

        const button =
            document.getElementById("predictBtn");

        const errorMessage =
            document.getElementById("errorMessage");

        clearError(errorMessage);

        /*
        * Show the full-page loading state immediately.
        *
        * WHY:
        * Model B can take many seconds because it may contact external
        * AI/search services. The user must know the application is
        * working rather than assume the page has frozen.
        */
        showPredictionLoading();

        setLoadingState(button, true);

        try {

            /*
             * Build the frontend API contract.
             *
             * Seller Type is included because Model B needs it.
             * Django deliberately removes it before Model A.
             */
            /*
            * Build the frontend API contract.
            *
            * WHY:
            * The HTML form uses its existing Django-oriented field names.
            * We read those exact names here so we do not need to rename
            * the form fields and risk breaking another part of the project.
            *
            * Seller Type is included because Model B needs it.
            * Django deliberately removes it before Model A.
            */
            const payload = {
                brand: getValue(form, "brand"),
                model: getValue(form, "model"),
                year: getValue(form, "Year"),
                age: getValue(form, "Age"),
                km_driven: getValue(form, "kmDriven"),
                transmission: getValue(
                    form,
                    "Transmission"
                ),
                owner: getValue(
                    form,
                    "Owner"
                ),
                fuel_type: getValue(
                    form,
                    "FuelType"
                ),
                seller_type: getValue(
                    form,
                    "Seller_Type"
                )
            };

            /*
             * Django's CSRF middleware protects the API.
             * The token is already rendered by index.html.
             */
            const csrfToken = getCsrfToken();

            if (!csrfToken) {
                throw new Error(
                    "Django CSRF token was not found."
                );
            }

            const response = await fetch(
                "/api/predict/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "X-CSRFToken":
                            csrfToken
                    },

                    credentials: "same-origin",

                    body: JSON.stringify(payload)
                }
            );

            /*
             * The API always returns JSON for normal
             * success/partial/error processing.
             */
            const data =
                await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error ||
                    "Prediction request failed."
                );
            }

            /*
             * Save the complete backend response.
             *
             * WHY:
             * Results.js can render the same structured response
             * without calling the prediction models again.
             */
            localStorage.setItem(
                "autovalue-latest-result",
                JSON.stringify(data)
            );

            saveToHistory(data);

            /*
             * Move to the Results route.
             *
             * app.js will load results.html and then initialize
             * results.js.
             */
            window.location.hash = "results";

        } catch (error) {

            console.error(
                "AutoValue AI prediction error:",
                error
            );

            showError(
                errorMessage,
                error.message
            );

        } finally {

            /*
            * Always remove the loading state.
            *
            * WHY:
            * This runs after success, partial failure, or an exception,
            * so the UI cannot remain permanently stuck in "loading".
            */
            hidePredictionLoading();

            setLoadingState(
                button,
                false
            );
        }
    }


    /*
     * Purpose:
     * Read a named field from the form.
     *
     * Inputs:
     * form: HTML form element.
     * fieldName: HTML input/select name.
     *
     * Output:
     * Trimmed string value.
     */
    function getValue(form, fieldName) {

        const field =
            form.elements[fieldName];

        if (!field) {
            return "";
        }

        return String(
            field.value || ""
        ).trim();
    }


    /*
     * Purpose:
     * Read the Django CSRF token rendered into index.html.
     *
     * Inputs:
     * None.
     *
     * Output:
     * CSRF token string or empty string.
     */
    /*
    * Purpose:
    * Read the Django CSRF token rendered by {% csrf_token %}.
    *
    * Inputs:
    * None.
    *
    * Output:
    * CSRF token string or an empty string.
    *
    * WHY:
    * index.html currently renders the token directly and does not
    * wrap it in a #csrf-token-container element.
    */
    function getCsrfToken() {

        const tokenInput =
            document.querySelector(
                "input[name='csrfmiddlewaretoken']"
            );

        return tokenInput
            ? tokenInput.value
            : "";
    }


    /*
     * Purpose:
     * Calculate vehicle age from the selected year.
     *
     * Inputs:
     * None. Reads the year input from the current page.
     *
     * Output:
     * Updates the age input.
     */
    function updateAge() {

        const yearInput =
            document.getElementById("year");

        const ageInput =
            document.getElementById("age");

        if (!yearInput || !ageInput) {
            return;
        }

        const year =
            Number(yearInput.value);

        if (!year) {
            ageInput.value = "";
            return;
        }

        const currentYear =
            new Date().getFullYear();

        const age =
            currentYear - year;

        ageInput.value =
            age >= 0 ? age : "";
    }


    /*
     * Purpose:
     * Store the latest prediction in the browser history.
     *
     * Inputs:
     * data: Complete API response.
     *
     * Output:
     * Keeps the five most recent predictions.
     */
    function saveToHistory(data) {

        const HISTORY_KEY =
            "autovalue-history";

        let history = [];

        try {

            history = JSON.parse(
                localStorage.getItem(
                    HISTORY_KEY
                ) || "[]"
            );

        } catch (error) {

            console.warn(
                "Could not read prediction history.",
                error
            );

            history = [];
        }

        history.unshift(data);

        /*
         * WHY:
         * A mini project does not need unlimited browser history.
         */
        history = history.slice(0, 5);

        localStorage.setItem(
            HISTORY_KEY,
            JSON.stringify(history)
        );
    }


    /*
     * Purpose:
     * Display the loading state on the prediction button.
     *
     * Inputs:
     * button: Prediction button.
     * isLoading: Whether the request is running.
     *
     * Output:
     * Updates button text and disabled state.
     */
    function setLoadingState(
        button,
        isLoading
    ) {

        if (!button) {
            return;
        }

        if (isLoading) {

            button.dataset.originalText =
                button.textContent;

            button.textContent =
                "Analysing...";

            button.disabled = true;

        } else {

            button.textContent =
                button.dataset.originalText ||
                "Estimate Value";

            button.disabled = false;
        }
    }


    /*
     * Purpose:
     * Remove an existing prediction error.
     *
     * Inputs:
     * element: Error message element.
     *
     * Output:
     * Clears the error display.
     */
    function clearError(element) {

        if (!element) {
            return;
        }

        element.textContent = "";
        element.hidden = true;
    }


    /*
     * Purpose:
     * Display a user-friendly prediction error.
     *
     * Inputs:
     * element: Error message element.
     * message: Error text.
     *
     * Output:
     * Updates the error display.
     */
    function showError(
        element,
        message
    ) {

        if (!element) {
            return;
        }

        element.textContent =
            message ||
            "Prediction failed.";

        element.hidden = false;
    }

    /*
    * Purpose:
    * Display the full-page prediction loading overlay.
    *
    * Inputs:
    * None.
    *
    * Output:
    * The loading overlay becomes visible.
    *
    * WHY:
    * Model B can take several seconds. Showing a dedicated loading
    * state gives immediate feedback and prevents the interface from
    * appearing frozen.
    */
    function showPredictionLoading() {

        const overlay =
            document.getElementById(
                "predictionLoadingOverlay"
            );

        if (!overlay) {
            return;
        }

        overlay.hidden = false;

        document.body.classList.add(
            "is-predicting"
        );
    }


    /*
    * Purpose:
    * Hide the full-page prediction loading overlay.
    *
    * Inputs:
    * None.
    *
    * Output:
    * The loading overlay becomes hidden.
    *
    * WHY:
    * The same function is used after success, partial failure, or
    * unexpected errors so the page always returns to a usable state.
    */
    function hidePredictionLoading() {

        const overlay =
            document.getElementById(
                "predictionLoadingOverlay"
            );

        if (!overlay) {
            return;
        }

        overlay.hidden = true;

        document.body.classList.remove(
            "is-predicting"
        );
    }
})();