// Function to fetch fares from the backend API
async function getFares() {
    let fromStation = document.getElementById("from").value;
    let toStation = document.getElementById("to").value;

    // Fetch data from the backend API
    let response = await fetch(`http://127.0.0.1:8000/get-fares/?from_station=${fromStation}&to_station=${toStation}`);
    let data = await response.json();

    // Update results in the UI
    document.getElementById("results").innerHTML = `
        <div class="result-card">
            <h3>🚇 TfL Fare:</h3> 
            <p>£${data.tfl_fares}</p>
        </div>
        <div class="result-card">
            <h3>🚆 National Rail Fare:</h3> 
            <p>£${data.national_rail_fares}</p>
        </div>
    `;
}

// Function to handle Dark Mode toggle
function toggleDarkMode() {
    const body = document.body;
    const toggleButton = document.getElementById("dark-mode-toggle");

    // Check if dark mode is currently enabled
    if (body.classList.contains("dark-mode")) {
        body.classList.remove("dark-mode");
        toggleButton.textContent = "Dark Mode 🌙";
        localStorage.setItem("darkMode", "disabled"); // Save preference
    } else {
        body.classList.add("dark-mode");
        toggleButton.textContent = "Light Mode ☀️";
        localStorage.setItem("darkMode", "enabled"); // Save preference
    }
}

// Ensure Dark Mode is remembered across refreshes
document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const body = document.body;

    // Check if dark mode was previously enabled
    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
        toggleButton.textContent = "☀️ Light Mode";
    } else {
        toggleButton.textContent = "🌙 Dark Mode";
    }

    // Attach event listener to the toggle button
    toggleButton.addEventListener("click", toggleDarkMode);
});
