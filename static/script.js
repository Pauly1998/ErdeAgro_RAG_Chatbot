const questionInput = document.getElementById("question");
const sendButton = document.getElementById("sendButton");
const messages = document.getElementById("messages");
const welcomeScreen = document.getElementById("welcomeScreen");


// ===============================
// SEND MESSAGE
// ===============================

async function sendMessage() {

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    // Hide welcome screen
    if (welcomeScreen) {
        welcomeScreen.style.display = "none";
    }

    // Show user message
    addMessage(question, "user");

    // Clear input
    questionInput.value = "";

    // Disable send button
    sendButton.disabled = true;

    // Show typing animation
    const typingElement = addTyping();

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });


        const data = await response.json();


        // Remove typing animation
        typingElement.remove();


        if (!response.ok) {

            addMessage(
                "Sorry, something went wrong. Please try again.",
                "assistant"
            );

            console.error(data);

            return;
        }


        // Show AI answer
        addMessage(
            data.answer,
            "assistant"
        );


    } catch (error) {

        typingElement.remove();

        addMessage(
            "⚠️ Unable to connect to the AI server. Please check that Flask and Ollama are running.",
            "assistant"
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;

        questionInput.focus();
    }
}


// ===============================
// ADD MESSAGE
// ===============================

function addMessage(text, sender) {

    const message = document.createElement("div");

    message.className = "message " + sender;


    const content = document.createElement("div");

    content.className = "message-content";


    if (sender === "assistant") {

        content.innerHTML = formatText(text);

    } else {

        content.textContent = text;

    }


    message.appendChild(content);

    messages.appendChild(message);


    // Scroll chat
    const chatContainer = document.querySelector(".chat-container");

    chatContainer.scrollTop = chatContainer.scrollHeight;
}


// ===============================
// FORMAT AI RESPONSE
// ===============================

function formatText(text) {

    if (!text) {
        return "";
    }


    // Escape HTML
    let formatted = escapeHtml(text);


    // Bold
    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    // Bullet points
    formatted = formatted.replace(
        /^\s*[-•]\s+(.*)$/gm,
        "• $1"
    );


    // Numbered list
    formatted = formatted.replace(
        /^\s*(\d+)\.\s+(.*)$/gm,
        "$1. $2"
    );


    // Line breaks
    formatted = formatted.replace(
        /\n/g,
        "<br>"
    );


    return formatted;
}


// ===============================
// ESCAPE HTML
// ===============================

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// ===============================
// TYPING ANIMATION
// ===============================

function addTyping() {

    const message = document.createElement("div");

    message.className = "message assistant";


    const content = document.createElement("div");

    content.className = "message-content";


    const typing = document.createElement("div");

    typing.className = "typing";


    typing.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;


    content.appendChild(typing);

    message.appendChild(content);

    messages.appendChild(message);


    const chatContainer = document.querySelector(".chat-container");

    chatContainer.scrollTop = chatContainer.scrollHeight;


    return message;
}


// ===============================
// SUGGESTION BUTTON
// ===============================

function askSuggestion(question) {

    questionInput.value = question;

    sendMessage();
}


// ===============================
// ENTER KEY
// ===============================

function handleKeyDown(event) {

    // Enter = send
    // Shift + Enter = new line

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
}


// ===============================
// NEW CHAT
// ===============================

function newChat() {

    messages.innerHTML = "";

    questionInput.value = "";

    if (welcomeScreen) {
        welcomeScreen.style.display = "block";
    }

    questionInput.focus();
}