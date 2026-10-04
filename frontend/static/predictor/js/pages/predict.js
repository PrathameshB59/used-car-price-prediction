/*
 * AutoValue AI
 * ============================================================
 * Prediction page module.
 *
 * PURPOSE:
 *     Collect vehicle information from the Predict page and
 *     send it to Django's JSON prediction API.
 *
 * FLOW:
 *     Form
 *       ↓
 *     JavaScript
 *       ↓
 *     POST /api/predict/
 *       ↓
 *     Django
 *       ↓
 *     Model A + Model B
 *       ↓
 *     JSON
 *       ↓
 *     Results page
 *
 * IMPORTANT:
 *     Model A and Model B calculations remain on the backend.
 *     This file only handles frontend communication and UI state.
 */

(function initializePredictModule() {
    window.AutoValuePredict = {

        /*
         * Purpose:
         * Initialize the prediction page.
         *
         * Inputs:
         * None.
         *
         * Output:
         * Attaches the prediction form submit handler.
         */
        init() {
            const form =
                document.getElementById("predictionForm");

            if (!form) {
                return;
            }

            this.bindForm(form);
            this.bindAgeCalculation();
        },

        /*
         * Purpose:
         * Connect the form submit event to the API request.
         *
         * Inputs:
         * form: HTML prediction form.
         *
         * Output:
         * None.
         */
        bindForm(form) {
            form.addEventListener(
                "submit",
                async (event) => {
                    event.preventDefault();

                    await this.submitPrediction(form);
                }
            );
        },

        /*
         * Purpose:
         * Calculate vehicle age automatically from manufacturing year.
         *
         * Why:
         * Age is one of Model A's required features and should match
         * the value displayed to the user.
         */
        bindAgeCalculation() {
            const yearInput =
                document.getElementById("year");

            const ageInput =
                document.getElementById("age");

            if (!yearInput || !ageInput) {
                return;
            }

            const updateAge = () => {
                const year =
                    Number(yearInput.value);

                const currentYear =
                    new Date().getFullYear();

                if (
                    Number.isInteger(year) &&
                    year > 0 &&
                    year <= currentYear
                ) {
                    ageInput.value =
                        currentYear - year;
                } else {
                    ageInput.value = "";
                }
            };

            yearInput.addEventListener(
                "input",
                updateAge
            );

            yearInput.addEventListener(
                "change",
                updateAge
            );
        },

        /*
         * Purpose:
         * Collect form values and send them to Django.
         *
         * Inputs:
         * form: HTML prediction form.
         *
         * Output:
         * None.
         */
        async submitPrediction(form) {
            const button =
                document.getElementById("predictBtn");

            this.setLoadingState(button, true);
            this.clearError();

            const payload = {
                brand:
                    document.getElementById("brand")?.value
                    || "",

                model:
                    document.getElementById("model")?.value
                    || "",

                year:
                    document.getElementById("year")?.value
                    || "",

                age:
                    document.getElementById("age")?.value
                    || "",

                km_driven:
                    document.getElementById("kmDriven")?.value
                    || "",

                transmission:
                    document.getElementById("transmission")?.value
                    || "",

                owner:
                    document.getElementById("owner")?.value
                    || "",

                fuel_type:
                    document.getElementById("fuelType")?.value
                    || "",

                seller_type:
                    document.getElementById("sellerType")?.value
                    || "",
            };

            try {
                const csrfToken =
                    this.getCsrfToken();

                const response =
                    await fetch(
                        "/api/predict/",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",

                                "X-CSRFToken":
                                    csrfToken,
                            },

                            credentials: "same-origin",

                            body:
                                JSON.stringify(payload),
                        }
                    );

                const data =
                    await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.error
                        || "Prediction request failed."
                    );
                }

                /*
                 * Save the complete API result.
                 *
                 * WHY:
                 * The Results page is a separate frontend page,
                 * so localStorage gives it access to the latest
                 * prediction without another backend request.
                 */
                localStorage.setItem(
                    "autovalue-latest-result",
                    JSON.stringify(data)
                );

                /*
                 * Keep a simple prediction history.
                 *
                 * This allows the Results page to eventually show
                 * multiple previous valuations.
                 */
                this.saveToHistory(data);

                window.location.hash =
                    "results";

            } catch (error) {
                console.error(
                    "Prediction request failed:",
                    error
                );

                this.showError(
                    error.message
                    || "Unable to calculate the vehicle value."
                );

            } finally {
                this.setLoadingState(
                    button,
                    false
                );
            }
        },

        /*
         * Purpose:
         * Read Django's CSRF token from the rendered template.
         *
         * Output:
         * CSRF token string.
         */
        getCsrfToken() {
            const token =
                document.querySelector(
                    "#csrf-token-container " +
                    "input[name='csrfmiddlewaretoken']"
                );

            return token?.value || "";
        },

        /*
         * Purpose:
         * Save the prediction to browser history.
         *
         * Inputs:
         * data: JSON response from Django.
         *
         * Output:
         * None.
         */
        saveToHistory(data) {
            let history = [];

            try {
                history =
                    JSON.parse(
                        localStorage.getItem(
                            "autovalue-history"
                        )
                    ) || [];
            } catch {
                history = [];
            }

            history.unshift(data);

            /*
             * Keep the browser history lightweight.
             * Five recent predictions are enough for this UI stage.
             */
            history = history.slice(0, 5);

            localStorage.setItem(
                "autovalue-history",
                JSON.stringify(history)
            );
        },

        /*
         * Purpose:
         * Show a user-facing prediction error.
         *
         * Inputs:
         * message: Error description.
         */
        showError(message) {
            const errorElement =
                document.getElementById(
                    "errorMessage"
                );

            if (!errorElement) {
                return;
            }

            errorElement.textContent = message;
        },

        /*
         * Purpose:
         * Remove an old error message.
         */
        clearError() {
            const errorElement =
                document.getElementById(
                    "errorMessage"
                );

            if (errorElement) {
                errorElement.textContent = "";
            }
        },

        /*
         * Purpose:
         * Prevent duplicate submissions while Django is
         * calculating Model A and Model B.
         */
        setLoadingState(button, loading) {
            if (!button) {
                return;
            }

            button.disabled = loading;

            if (loading) {
                button.dataset.originalText =
                    button.textContent;

                button.textContent =
                    "Analysing...";
            } else {
                button.textContent =
                    button.dataset.originalText
                    || "Analyze car value";
            }
        },
    };
})();
