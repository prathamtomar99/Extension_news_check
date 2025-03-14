// Function to initialize the "Go" button
function initializeGoButton() {
    const goButton = document.getElementById("go");
    goButton.addEventListener("click", function () {
        goButton.disabled = true;
        goButton.innerHTML = `<span class="spinner"></span> Processing...`;

        // Send a message to the background script to process the page
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const activeTab = tabs[0].id;
            chrome.scripting.executeScript({
                target: { tabId: activeTab },
                function: parsePage
            }, (results) => {
                if (!results || !results[0] || !results[0].result) {
                    console.error("Error: No result from content script.");
                    goButton.disabled = false;
                    goButton.textContent = "Process News";
                    return;
                }
                
                const parsedContent = results[0].result;
                chrome.runtime.sendMessage(
                    { action: "process", content: parsedContent },
                    function (response) {
                        const output = response.result || "Error processing the page.";
                        const mainDiv = document.getElementById("main");
                        mainDiv.innerHTML = formatOutput(output);
                        attachDropdownListeners();

                        document.getElementById("back-button").addEventListener("click", function () {
                            document.getElementById("main").innerHTML = `
                                <div id="content">
                                    <button id="go">Process News</button>
                                </div>
                            `;
                            initializeGoButton();
                        });
                    }
                );
            });
        });
    });
}

// Function to format the output into a UI with dropdown descriptions
function formatOutput(data) {
    try {
        const results = JSON.parse(data);
        let html = `<h3>Results:</h3>`;
        results.forEach((item, index) => {
            html += `
                <div class="result-card">
                    <strong class="title-toggle" data-index="${index}">📰 ${item.Title || "N/A"}</strong><br>
                    <strong>🔗 Link:</strong> <a href="${item.Link || "#"}" target="_blank">${item.Link || "N/A"}</a>
                    <div class="description" id="desc-${index}" style="display: none;">
                        <strong>📄 Description:</strong> ${item.Description ? item.Description : "No description available"}<br>
                    </div>
                    <strong>🎯 Similarity:</strong> ${item.Similarity ? (item.Similarity * 100).toFixed(2) + "%" : "N/A"}<br>
                </div>
            `;
        });
        html += `<button id="back-button">⬅ Back</button>`;
        return html;
    } catch (error) {
        console.error("Error formatting output:", error);
        return `<div>Error displaying results.</div><button id="back-button">⬅ Back</button>`;
    }
}

// Function to toggle dropdown description when clicking on title
function attachDropdownListeners() {
    document.querySelectorAll(".title-toggle").forEach((title) => {
        title.addEventListener("click", function () {
            const index = this.getAttribute("data-index");
            const desc = document.getElementById(`desc-${index}`);
            desc.style.display = desc.style.display === "none" ? "block" : "none";
        });
    });
}

// Initialize the "Go" button when the popup loads
document.addEventListener("DOMContentLoaded", function () {
    initializeGoButton();
});

// Function to parse the page content
function parsePage() {
    const headline = document.querySelector("h1")?.innerText || "No headline found";
    const paragraphs = [...document.querySelectorAll("p")].map(p => p.innerText).join("\n");
    const text = paragraphs || document.body.innerText || "No text found";
    return { headline, text };
}