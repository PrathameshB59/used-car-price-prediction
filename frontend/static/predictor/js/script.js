const predictButton = document.getElementById("predict-button");
const resultBox = document.getElementById("result");
const predictedPrice = document.getElementById("predicted-price");

predictButton.addEventListener("click", () => {
    const brand = document.getElementById("brand").value;
    const year = document.getElementById("year").value;
    const km = document.getElementById("km").value;
    const fuel = document.getElementById("fuel").value;

    if (!brand || !year || !km || !fuel) {
        alert("Please fill in all car details.");
        return;
    }

    predictedPrice.textContent = "₹ --";
    resultBox.classList.remove("hidden");

    console.log("Prediction form data:", {
        brand,
        year,
        kilometersDriven: km,
        fuel
    });
});
