const inputForm = document.querySelector(".input-form");
const input = document.querySelector(".input");
const messages = document.querySelector(".messages");
const toggleSwitch = document.querySelector(".toggle-switch");

// When the user clicks the toggle switch, toggle dark mode and save the preference to localStorage
toggleSwitch.addEventListener("change", (e) => {
  if (e.target.checked) {
    // Enable dark mode
    document.body.classList.add("dark-mode");
    localStorage.setItem("dark-mode", "true"); // Save the preference to localStorage
  } else {
    // Disable dark mode
    document.body.classList.remove("dark-mode");
    localStorage.removeItem("dark-mode"); // Remove the preference from localStorage
  }
});

// On page load, check localStorage for dark mode preference and apply it if necessary
document.addEventListener("DOMContentLoaded", () => {
  const inputForm = document.querySelector(".input-form");
  const input = document.querySelector(".input");
  const messages = document.querySelector(".messages");
  const toggleSwitch = document.querySelector(".toggle-switch");
  const newChatButton = document.getElementById("new-chat-button");
  const overlay = document.getElementById("overlay");
  const acknowledgeButton = document.getElementById("acknowledgeButton");

  if (localStorage.getItem("dark-mode") === "true") {
    document.body.classList.add("dark-mode");
    toggleSwitch.checked = true;
  }

  if (!isUserAuthenticated) {
    newChatButton.disabled = true;
    newChatButton.style.cursor = "not-allowed";
    newChatButton.style.backgroundColor = "grey";
    newChatButton.title = "You need to be logged in to make a new chat.";
  }

  inputForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const userInput = input.value.trim();
    if (userInput) {
      addMessage(userInput, "user");
      getResponse(userInput);
      input.value = "";
    }
  });

  // addMessage will only be responsible for adding the user message into the UI
  // independent of the server

  let firstMessage = true;

  function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = sender === "user" ? "user-message" : "bot-message";
    text = text.replace(/(?:\r\n|\r|\n)/g, '<br>');
    message.innerHTML = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
  }

  // getResponse will actually be responsible for the POST request and fetching a JSON containing
  // the response data from the server.
  function getResponse(userInput) {
    const DATA = { message: userInput };
    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(DATA),
    })
      .then((response) => response.json())
      .then((data) => {
        if (firstMessage && data.not_auth_msg) {
          const message = document.createElement("div");
          message.className = "bot-message";
          message.textContent = data.not_auth_msg;
          message.style.color = "#E2694F";
          messages.appendChild(message);
          messages.scrollTop = messages.scrollHeight;
          firstMessage = false;
        }
        addMessage(data.content, "bot");
      })
      .catch((error) => console.error("Error:", error));
  }

  // If the user clicks the acknowledge button, hide the overlay.
  acknowledgeButton.addEventListener("click", () => {
    const dontShowAgainCheckbox = document.getElementById(
      "dontShowAgainCheckbox"
    );
    if (dontShowAgainCheckbox.checked) {
      localStorage.setItem("acknowledged", "true");
    }
    overlay.classList.add("fade-out");
  });

  if (localStorage.getItem("acknowledged") === "true") {
    if (overlay) overlay.style.display = "none";
  } else {
    if (overlay) overlay.style.display = "flex";
  }
});

function refreshPage() {
  location.reload();
}
