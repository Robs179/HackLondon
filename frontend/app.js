async function getFares() {
  let fromStation = document.getElementById("from").value;
  let toStation = document.getElementById("to").value;
  
  let response = await fetch(`http://127.0.0.1:8000/get-fares/?from_station=${fromStation}&to_station=${toStation}`);
  let data = await response.json();

  document.getElementById("results").innerHTML = `
      <h3>TfL Fare:</h3> ${JSON.stringify(data.tfl_fares, null, 2)}
      <h3>National Rail Fare:</h3> ${JSON.stringify(data.national_rail_fares, null, 2)}
    `;
}
