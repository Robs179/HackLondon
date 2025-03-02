document.addEventListener('DOMContentLoaded', () => {
    // Find the container element (injected from src)
    const container = document.querySelector('.container');
    if (container) {
        // Create a new div for date and time inputs with custom styling
        const dtGroup = document.createElement('div');
        dtGroup.className = 'custom-datetime-group';
        dtGroup.innerHTML = `
            <div class="datetime-input">
                <label for="date">Date:</label>
                <input type="date" id="date">
            </div>
            <div class="datetime-input">
                <label for="time">Time:</label>
                <input type="time" id="time">
            </div>
        `;
        // Insert the datetime group above the input row without touching src files
        const inputRow = container.querySelector('.input-row');
        inputRow.parentNode.insertBefore(dtGroup, inputRow);
    }
    
    // Inject custom styles for the datetime group for a pretty look
    const style = document.createElement('style');
    style.textContent = `
        .custom-datetime-group {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
            padding: 10px;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        .custom-datetime-group .datetime-input {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .custom-datetime-group label {
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }
        .custom-datetime-group input[type="date"],
        .custom-datetime-group input[type="time"] {
            padding: 8px;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 150px;
        }
    `;
    document.head.appendChild(style);
    
    // Override the getFares function to include date and time parameters.
    // (Assumes getFares is globally defined by the src files.)
    window.getFares = async function() {
        let fromStation = document.getElementById("from").value;
        let toStation = document.getElementById("to").value;
        let hasRailcard = document.getElementById("railcard").checked;
        let dateVal = document.getElementById("date").value;  // new date input
        let timeVal = document.getElementById("time").value;  // new time input
        
        // Build the API URL including date and time params.
        let url = `http://127.0.0.1:8000/get-fares-tfl/?from_station=${fromStation}` +
                  `&to_station=${toStation}&railcard=${hasRailcard}` +
                  `&date=${dateVal}&time=${timeVal}`;
        let response = await fetch(url);
        let data = await response.json();
        
        // Update the results UI as before.
        document.getElementById("results").innerHTML = `
            <div class="result-card">
                <h3>🚇 TfL Fare:</h3>
                <p>£${data.tfl_fares}</p>
            </div>
            <div class="result-card">
                <h3>🚆 National Rail Fare:</h3>
                <p>${hasRailcard ? '(With Railcard) ' : ''}£${data.national_rail_fares}</p>
            </div>
        `;
        document.getElementById("results").style.display = "block";
        document.getElementById("results-title").style.display = "block";
    }
});
