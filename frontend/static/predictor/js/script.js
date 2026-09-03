const form = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");

const yearInput = document.getElementById("year");
const ageInput = document.getElementById("age");


/*
 * =========================================
 * VEHICLE AGE
 * =========================================
 *
 * The V2 dataset uses:
 *
 * Age = 2024 - Year
 *
 * We use the same relationship here so that
 * the frontend sends data consistent with
 * the training data.
 */

function updateVehicleAge() {

    const year = parseInt(yearInput.value);

    if (!year || year < 1980 || year > 2024) {

        ageInput.value = "";

        return;
    }

    const age = 2024 - year;

    ageInput.value = age;
}


if (yearInput && ageInput) {

    yearInput.addEventListener(
        "input",
        updateVehicleAge
    );
}


/*
 * =========================================
 * OTHER / CUSTOM OPTION
 * =========================================
 *
 * When the user selects:
 *
 * Other / Unknown
 *
 * we show a text box where the user can
 * enter the actual value.
 */

const otherFields = [
    {
        selectId: "brand",
        inputId: "brand_other"
    },

    {
        selectId: "model",
        inputId: "model_other"
    },

    {
        selectId: "transmission",
        inputId: "transmission_other"
    },

    {
        selectId: "owner",
        inputId: "owner_other"
    },

    {
        selectId: "fuel_type",
        inputId: "fuel_type_other"
    },

    {
        selectId: "seller_type",
        inputId: "seller_type_other"
    }
];


function setupOtherField(selectId, inputId) {

    const select = document.getElementById(selectId);
    const input = document.getElementById(inputId);

    if (!select || !input) {
        return;
    }


    function updateOtherField() {

        const isOther =
            select.value === "Other / Unknown";


        if (isOther) {

            input.classList.add("show");

            input.required = true;

            input.focus();

        } else {

            input.classList.remove("show");

            input.required = false;

            input.value = "";
        }
    }


    select.addEventListener(
        "change",
        updateOtherField
    );
}


otherFields.forEach(field => {

    setupOtherField(
        field.selectId,
        field.inputId
    );

});


/*
 * =========================================
 * FORM SUBMISSION
 * =========================================
 *
 * Django performs the actual prediction.
 *
 * JavaScript only provides frontend
 * behavior and feedback.
 */

if (form && predictButton) {

    form.addEventListener("submit", () => {

        predictButton.disabled = true;

        const icon =
            predictButton.querySelector(
                ".button-icon"
            );

        const text =
            predictButton.querySelector(
                ".button-text"
            );


        if (icon) {
            icon.textContent = "⏳";
        }

        if (text) {
            text.textContent = "Predicting...";
        }

    });

}
