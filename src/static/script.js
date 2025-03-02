document.getElementById("fetchMessage").addEventListener("click", async () => {
    const response = await fetch("/api/greet");
    const data = await response.json();
    document.getElementById("message").innerText = data.message;
});

document.getElementById("submitName").addEventListener("click", async () => {
    const name = document.getElementById("nameInput").value;
    
    const response = await fetch("/api/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: name })
    });

    const data = await response.json();
    document.getElementById("response").innerText = data.message;
});
