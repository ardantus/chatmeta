document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chat-container");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", () => {
        const userMessage = messageInput.value.trim();
        if (userMessage) {
            appendMessage("You: " + userMessage);
            sendMessageToServer(userMessage);
            messageInput.value = "";
        }
    });

    messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });

    function appendMessage(message, isError = false) {
        const messageDiv = document.createElement("div");
        messageDiv.textContent = message;

        if (isError) {
            messageDiv.style.color = "red";
        }

        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function appendImage(imageUrl) {
        const imageElement = document.createElement("img");
        imageElement.src = imageUrl;
        imageElement.alt = "Generated Image";
        imageElement.style.maxWidth = "300px";
        imageElement.style.marginTop = "10px";

        chatContainer.appendChild(imageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function sendMessageToServer(message) {
        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.image_url) {
                appendMessage("MetaAI: " + data.response);
                appendImage(data.image_url);  // Tampilkan gambar jika tersedia
            } else {
                appendMessage("MetaAI: " + data.response);
            }
        })
        .catch(error => {
            appendMessage("Error: Tidak bisa terhubung ke server.", true);
            console.error("Error:", error);
        });
    }
});
