const micBtn = document.getElementById("micBtn");
const userTextP = document.getElementById("userText");
const botTextP = document.getElementById("botText");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = "en-IN";

micBtn.onclick = () => {
  recognition.start();
};

recognition.onresult = async (event) => {
  const userText = event.results[0][0].transcript;
  userTextP.innerText = "You: " + userText;

  const res = await fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: userText })
  });

  const data = await res.json();
  botTextP.innerText = data.bot_name + ": " + data.reply;

  speak(data.reply);
};

function speak(text) {
  const speech = new SpeechSynthesisUtterance(text);
  speech.lang = "en-IN";
  window.speechSynthesis.speak(speech);
}
