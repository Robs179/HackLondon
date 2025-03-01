async function getFares() {
  let fromStation = document.getElementById("from").value;
  let toStation = document.getElementById("to").value;

  let response = await fetch(`http://127.0.0.1:8000/get-fares/?from_station=${fromStation}&to_station=${toStation}`);
  let data = await response.json();

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

// Dark Mode Toggle
document.getElementById("dark-mode-toggle").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    let button = document.getElementById("dark-mode-toggle");
    button.textContent = document.body.classList.contains("dark-mode") ? "☀️ Light Mode" : "🌙 Dark Mode";
});
