async function getFares() {
    let fromStation = document.getElementById("from").value;
    let toStation = document.getElementById("to").value;
    let date = document.getElementById("date").value;
    let time = document.getElementById("time").value;
    let hasRailcard = document.getElementById("railcard").checked;

    // Show loading spinner
    document.getElementById("loading").style.display = "block";

    // Fetch data from the backend API
    let response = await fetch(`http://127.0.0.1:8000/find-best-fare/?from_station=${fromStation}&to_station=${toStation}&date=${date}&time=${time}&railcard=${hasRailcard}`);
    let data = await response.json();

    // Hide loading spinner
    document.getElementById("loading").style.display = "none";

    // Update results in the UI
    document.getElementById("results").innerHTML = `
        <div class="result-card">
            <h3>🚇 TfL Fare:</h3> 
            <p>From ${data.tfl.origin_code}, To ${data.tfl.destination_code} for the price of £${data.tfl.cost}</p>
        </div>
        <div class="result-card">
            <h3>🚆 National Rail Fare:</h3> 
            <p>${hasRailcard ? '(With Railcard) ' : ''} From ${data.nr.origin_code}, To ${data.nr.destination_code} for the price of £${data.nr.cost}</p>
            <p>Description ${data.nr.description}</p>
        </div>
    `;
    document.getElementById("results").style.display = "block";
    document.getElementById("results-title").style.display = "block";
}

// Dark Mode Toggle
function toggleDarkMode() {
    const body = document.body;
    const toggleButton = document.getElementById("dark-mode-toggle");

    if (body.classList.contains("dark-mode")) {
        body.classList.remove("dark-mode");
        toggleButton.textContent = "Dark Mode 🌙";
        localStorage.setItem("darkMode", "disabled");
    } else {
        body.classList.add("dark-mode");
        toggleButton.textContent = "Light Mode ☀️";
        localStorage.setItem("darkMode", "enabled");
    }
}

// Ensure Dark Mode is remembered across refreshes
document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const body = document.body;

    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
        toggleButton.textContent = "Light Mode ☀️";
    } else {
        toggleButton.textContent = "Dark Mode 🌙";
    }

    toggleButton.addEventListener("click", toggleDarkMode);
});