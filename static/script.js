document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chat-container");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", () => {
        const userMessage = messageInput.value.trim();
        if (userMessage) {
            appendMessage("You: " + userMessage);
            sendMessageToServer(userMessage);
            messageInput.value = ""; // Kosongkan input
        }
    });

    // Kirim pesan dengan menekan Enter
    messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });

    function appendMessage(message, isError = false) {
        const messageDiv = document.createElement("div");
        messageDiv.textContent = message;

        // Styling khusus untuk error
        if (isError) {
            messageDiv.style.color = "red";
        }

        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll ke bawah
    }

    function sendMessageToServer(message) {
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server Error: " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Server Response:", data); // Log respons untuk debugging
            if (data && data.response) {
                appendMessage("MetaAI: " + data.response);
            } else {
                appendMessage("MetaAI: Respons tidak valid dari server.", true);
            }
        })
        .catch(error => {
            appendMessage("Error: Tidak bisa terhubung ke server.", true);
            console.error("Error:", error);
        });
    }
});
