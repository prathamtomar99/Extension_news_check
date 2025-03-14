chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "process") {
        const { content } = request;

        // Send data to the Flask backend
        fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                headline: content.headline, 
                text: content.text 
            }) // Send headline and text separately as required by the backend
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            sendResponse({ result: JSON.stringify(data) });
        })
        .catch(error => {
            console.error("Error:", error);
            sendResponse({ result: "Error processing the page." });
        });

        return true; // Ensure async response handling
    }
});
