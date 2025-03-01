document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/some-endpoint")
      .then(response => response.json())
      .then(data => console.log(data));
});