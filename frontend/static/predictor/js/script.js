/* Used Car Price Prediction - polished FORM -> LOADING -> RESULT flow */
(function () {
    "use strict";

    const page = document.querySelector(".page");
    if (!page) return;

    const otherFields = [
        ["brand", "brand_other"],
        ["model", "model_other"],
        ["transmission", "transmission_other"],
        ["owner", "owner_other"],
        ["fuel_type", "fuel_type_other"],
        ["seller_type", "seller_type_other"]
    ];

    const style = document.createElement("style");
    style.textContent = `
        body.stage-active { overflow-x: hidden; }
        body.stage-active .page {
            width:100%; max-width:none; min-height:100vh; margin:0; padding:0;
        }
        .flow-screen {
            min-height:100vh; width:100%; display:flex; align-items:center;
            justify-content:center; box-sizing:border-box; padding:32px 20px;
            animation:screenIn .45s ease both;
        }
        .flow-shell { width:min(900px,100%); text-align:center; }
        .flow-kicker {
            display:inline-flex; align-items:center; gap:8px; padding:7px 12px;
            border:1px solid rgba(45,212,191,.22); border-radius:999px;
            background:rgba(20,184,166,.07); color:#5eead4; font-size:11px;
            font-weight:800; letter-spacing:.16em; text-transform:uppercase;
        }
        .flow-kicker::before {
            content:""; width:7px; height:7px; border-radius:50%;
            background:#2dd4bf; box-shadow:0 0 14px rgba(45,212,191,.9);
        }
        .flow-title {
            margin:20px 0 10px; color:#f8fafc; font-size:clamp(34px,6vw,64px);
            line-height:1.03; letter-spacing:-.04em;
        }
        .flow-subtitle {
            max-width:620px; margin:0 auto; color:#94a3b8;
            font-size:16px; line-height:1.7;
        }
        .loading-panel {
            width:min(620px,100%); margin:42px auto 0; padding:30px;
            border:1px solid rgba(148,163,184,.15); border-radius:28px;
            background:rgba(15,23,42,.78); box-shadow:0 30px 80px rgba(0,0,0,.35);
            backdrop-filter:blur(18px);
        }
        .loading-car {
            position:relative; width:92px; height:92px; margin:0 auto 26px;
            display:grid; place-items:center; border:1px solid rgba(45,212,191,.28);
            border-radius:50%; background:radial-gradient(circle,rgba(20,184,166,.16),rgba(15,23,42,.2) 68%);
            font-size:42px; animation:carFloat 1.8s ease-in-out infinite;
        }
        .loading-car::before,.loading-car::after {
            content:""; position:absolute; inset:-10px; border:1px solid rgba(45,212,191,.12);
            border-radius:50%; animation:orbit 2.8s linear infinite;
        }
        .loading-car::after {
            inset:-20px; border-color:rgba(45,212,191,.06);
            animation-duration:4s; animation-direction:reverse;
        }
        .loading-message {
            min-height:28px; margin:0 0 20px; color:#e2e8f0;
            font-size:18px; font-weight:700;
        }
        .loading-progress {
            height:7px; overflow:hidden; border-radius:999px; background:#1e293b;
        }
        .loading-progress>span {
            display:block; width:35%; height:100%; border-radius:inherit;
            background:linear-gradient(90deg,#14b8a6,#5eead4,#14b8a6);
            background-size:200% 100%; animation:progressMove 1.25s ease-in-out infinite;
        }
        .loading-steps {
            display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:24px;
        }
        .loading-step {
            padding:12px 8px; border:1px solid rgba(148,163,184,.1); border-radius:14px;
            color:#64748b; font-size:12px; font-weight:700; transition:.3s ease;
        }
        .loading-step.active {
            color:#99f6e4; border-color:rgba(45,212,191,.3);
            background:rgba(20,184,166,.08);
        }
        .result-screen { align-items:flex-start; padding-top:55px; padding-bottom:70px; }
        .result-screen .flow-shell { max-width:1040px; }
        .result-container { margin-top:38px; text-align:left; }
        .result-container .result {
            display:block; width:100%; margin:0; padding:0;
            border:0; background:transparent;
        }
        .result-container .comparison-title,
        .result-container .comparison-heading {
            color:#f8fafc; letter-spacing:.08em; text-transform:uppercase;
            font-size:11px; font-weight:800;
        }
        .result-container .result-note { margin-bottom:24px; color:#94a3b8; }
        .result-container .model-comparison {
            display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:18px;
        }
        .result-container .model-card,
        .result-container .comparison-summary,
        .result-container .model-b-analysis,
        .result-container .prediction-sources {
            box-sizing:border-box; border:1px solid rgba(148,163,184,.14);
            border-radius:22px; background:rgba(15,23,42,.72);
            box-shadow:0 18px 50px rgba(0,0,0,.22);
        }
        .result-container .model-card { min-height:270px; padding:28px; }
        .result-container .model-b-card { border-color:rgba(45,212,191,.3); }
        .result-container .model-label {
            margin:0 0 8px; color:#64748b; font-size:10px; font-weight:900;
            letter-spacing:.18em;
        }
        .result-container .model-card h3 {
            margin:0 0 22px; color:#e2e8f0; font-size:20px;
        }
        .result-container .model-price {
            display:block; margin-bottom:16px; color:#2dd4bf;
            font-size:clamp(34px,5vw,48px); line-height:1; letter-spacing:-.04em;
        }
        .result-container .model-description,
        .result-container .model-detail,
        .result-container .model-error,
        .result-container .model-error-detail { color:#94a3b8; line-height:1.65; }
        .result-container .model-detail strong { color:#cbd5e1; }
        .result-container .comparison-summary {
            margin-top:18px; padding:28px; text-align:center;
        }
        .result-container .comparison-difference {
            display:block; margin:12px 0; color:#5eead4;
            font-size:clamp(34px,5vw,50px);
        }
        .result-container .comparison-summary p { color:#94a3b8; }
        .result-container .comparison-summary strong { color:#e2e8f0; }
        .result-container .model-b-analysis,
        .result-container .prediction-sources { margin-top:18px; padding:28px; }
        .result-container .model-b-analysis>p:last-child {
            color:#cbd5e1; line-height:1.8;
        }
        .result-container .prediction-sources ul { margin:12px 0 0; padding-left:20px; }
        .result-container .prediction-sources li { margin:8px 0; }
        .result-container .prediction-sources a { color:#5eead4; }
        .result-actions {
            display:flex; justify-content:center; gap:12px; margin-top:28px;
        }
        .result-actions button {
            appearance:none; border:1px solid rgba(148,163,184,.2); border-radius:14px;
            padding:13px 20px; background:#0f172a; color:#e2e8f0; font:inherit;
            font-weight:800; cursor:pointer; transition:transform .2s ease,border-color .2s ease;
        }
        .result-actions button:hover {
            transform:translateY(-2px); border-color:rgba(45,212,191,.45);
        }
        .flow-error {
            margin:28px auto 0; padding:22px; border:1px solid rgba(248,113,113,.25);
            border-radius:18px; background:rgba(127,29,29,.12); color:#fecaca;
        }
        @keyframes screenIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
        @keyframes carFloat { 0%,100%{transform:translateY(0) rotate(-2deg)} 50%{transform:translateY(-8px) rotate(2deg)} }
        @keyframes orbit { to{transform:rotate(360deg)} }
        @keyframes progressMove {
            0%{transform:translateX(-110%);background-position:0 0}
            100%{transform:translateX(310%);background-position:100% 0}
        }
        @media(max-width:720px) {
            .loading-steps,.result-container .model-comparison { grid-template-columns:1fr; }
            .loading-panel { padding:22px; }
            .result-screen { padding-top:30px; }
        }
    `;
    document.head.appendChild(style);

    const originalPageHTML = page.innerHTML;
    let loadingTimer = null;

    function setHash(stage) {
        try { history.replaceState(null, "", `#${stage}`); } catch (_) {}
    }

    function setupOtherFields() {
        otherFields.forEach(([selectId, inputId]) => {
            const select = document.getElementById(selectId);
            const input = document.getElementById(inputId);
            if (!select || !input) return;

            const update = () => {
                const isOther = select.value === "Other / Unknown";
                input.classList.toggle("show", isOther);
                input.required = isOther;
                if (!isOther) input.value = "";
            };

            select.addEventListener("change", update);
            update();
        });
    }

    function setupAge() {
        const year = document.getElementById("year");
        const age = document.getElementById("age");
        if (!year || !age) return;

        year.addEventListener("input", () => {
            const value = parseInt(year.value, 10);
            age.value = value >= 1980 && value <= 2024 ? 2024 - value : "";
        });
    }

    function renderLoading() {
        page.innerHTML = `
            <section class="flow-screen loading-screen" aria-live="polite">
                <div class="flow-shell">
                    <div class="flow-kicker">Prediction in progress</div>
                    <h1 class="flow-title">Analysing your car</h1>
                    <p class="flow-subtitle">
                        The local ML model and current-market AI analysis are working together.
                    </p>
                    <div class="loading-panel">
                        <div class="loading-car" aria-hidden="true">🚗</div>
                        <p class="loading-message" id="loading-message">Preparing your vehicle data…</p>
                        <div class="loading-progress" aria-hidden="true"><span></span></div>
                        <div class="loading-steps">
                            <div class="loading-step active">01 · Input</div>
                            <div class="loading-step">02 · ML Model</div>
                            <div class="loading-step">03 · Market AI</div>
                        </div>
                    </div>
                </div>
            </section>
        `;

        document.body.classList.add("stage-active");
        setHash("loading");

        const messages = [
            "Preparing your vehicle data…",
            "Running the trained ML model…",
            "Researching current market signals…",
            "Comparing both predictions…"
        ];
        let index = 0;
        const message = document.getElementById("loading-message");
        const steps = [...document.querySelectorAll(".loading-step")];

        const tick = () => {
            if (message) message.textContent = messages[index % messages.length];
            steps.forEach((step, i) => step.classList.toggle("active", i <= Math.min(index, 2)));
            index++;
        };

        tick();
        loadingTimer = window.setInterval(tick, 1400);
    }

    function stopLoading() {
        if (loadingTimer) {
            clearInterval(loadingTimer);
            loadingTimer = null;
        }
    }

    function escapeHTML(value) {
        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function renderError(message) {
        stopLoading();
        page.innerHTML = `
            <section class="flow-screen result-screen">
                <div class="flow-shell">
                    <div class="flow-kicker">Prediction issue</div>
                    <h1 class="flow-title">We couldn't finish that</h1>
                    <p class="flow-subtitle">
                        The prediction request did not return a usable result.
                    </p>
                    <div class="flow-error">${escapeHTML(message)}</div>
                    <div class="result-actions">
                        <button type="button" id="retry-prediction">← Back to form</button>
                    </div>
                </div>
            </section>
        `;
        setHash("error");
        document.getElementById("retry-prediction")?.addEventListener("click", restoreForm);
    }

    function renderResult(resultElement) {
        stopLoading();
        page.innerHTML = `
            <section class="flow-screen result-screen">
                <div class="flow-shell">
                    <div class="flow-kicker">Prediction complete</div>
                    <h1 class="flow-title">Your valuation is ready</h1>
                    <p class="flow-subtitle">
                        A clear comparison between the trained ML model and AI market analysis.
                    </p>
                    <div class="result-container">${resultElement.outerHTML}</div>
                    <div class="result-actions">
                        <button type="button" id="new-prediction">↻ Predict another car</button>
                    </div>
                </div>
            </section>
        `;
        document.body.classList.add("stage-active");
        setHash("results");
        document.getElementById("new-prediction")?.addEventListener("click", restoreForm);
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function restoreForm() {
        stopLoading();
        page.innerHTML = originalPageHTML;
        document.body.classList.remove("stage-active");
        setHash("form");
        window.scrollTo({ top: 0, behavior: "smooth" });
        bootForm();
    }

    function submitPrediction(currentForm, currentButton) {
        renderLoading();
        currentButton.disabled = true;

        const formData = new FormData(currentForm);
        const csrfToken = currentForm.querySelector(
            'input[name="csrfmiddlewaretoken"]'
        )?.value;

        fetch(currentForm.action || window.location.href, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                ...(csrfToken ? { "X-CSRFToken": csrfToken } : {})
            },
            credentials: "same-origin"
        })
            .then(async (response) => {
                const html = await response.text();
                if (!response.ok) {
                    throw new Error(`Server returned ${response.status}.`);
                }
                return html;
            })
            .then((html) => {
                const doc = new DOMParser().parseFromString(html, "text/html");
                const result = doc.querySelector("#result");

                if (result) {
                    renderResult(result);
                    return;
                }

                const error = doc.querySelector(".error");
                if (error) {
                    renderError(error.textContent.trim());
                    return;
                }

                renderError("No prediction result was found in the server response.");
            })
            .catch((error) => {
                renderError(error.message || "Network error while requesting prediction.");
            });
    }

    function bootForm() {
        const currentForm = document.getElementById("prediction-form");
        const currentButton = document.getElementById("predict-button");
        if (!currentForm || !currentButton) return;

        setupAge();
        setupOtherFields();

        currentForm.addEventListener("submit", (event) => {
            event.preventDefault();

            if (!currentForm.checkValidity()) {
                currentForm.reportValidity();
                return;
            }

            submitPrediction(currentForm, currentButton);
        });
    }

    bootForm();
})();

(function () {
    "use strict";

    function setupFrontendPages() {
        const howItWorksLinks = document.querySelectorAll(
            'a[href="#how-it-works"], [data-page="how-it-works"]'
        );

        if (!howItWorksLinks.length) {
            return;
        }

        howItWorksLinks.forEach((link) => {
            link.addEventListener("click", async (event) => {
                event.preventDefault();

                if (window.initHowItWorksPage) {
                    await window.initHowItWorksPage();
                }
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", setupFrontendPages);
    } else {
        setupFrontendPages();
    }
})();
