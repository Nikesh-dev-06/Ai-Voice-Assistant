// DOM Elements
const micBtn = document.getElementById("micBtn");
const muteBtn = document.getElementById("muteBtn");
const settingsToggleBtn = document.getElementById("settingsToggleBtn");
const closeSettingsBtn = document.getElementById("closeSettingsBtn");
const saveSettingsBtn = document.getElementById("saveSettingsBtn");
const settingsCloseBg = document.getElementById("settingsCloseBg");
const settingsModal = document.getElementById("settingsModal");

const chatLogs = document.getElementById("chatLogs");
const textForm = document.getElementById("textForm");
const textQuery = document.getElementById("textQuery");
const statusText = document.getElementById("statusText");
const statusDot = document.getElementById("statusDot");
const botFace = document.getElementById("botFace");
const headerBotName = document.getElementById("headerBotName");

// Form controls in settings
const usernameInput = document.getElementById("usernameInput");
const botnameInput = document.getElementById("botnameInput");
const toneInput = document.getElementById("toneInput");
const voiceGenderInput = document.getElementById("voiceGenderInput");
const voiceSelect = document.getElementById("voiceSelect");

// Canvas
const canvas = document.getElementById("visualizerCanvas");
const ctx = canvas.getContext("2d");

// Application State
let appSettings = {
  user_name: "Nikesh",
  bot_name: "MYRA",
  tone: "friendly"
};
let isMuted = localStorage.getItem("isMuted") === "true";
let selectedVoiceName = localStorage.getItem("selectedVoiceName") || "";
let voicePreference = localStorage.getItem("voicePreference") || "all";
let activeTheme = localStorage.getItem("theme") || "cyberpunk";

let isListening = false;
let isSpeaking = false;
let allVoices = [];

// Initialize layout
document.body.className = `theme-${activeTheme}`;
updateMuteButtonUI();

// ----------------------------------------------------
// 1. Settings & Sync API
// ----------------------------------------------------
async function fetchSettings() {
  try {
    const res = await fetch("http://127.0.0.1:5000/settings");
    if (res.ok) {
      appSettings = await res.json();
      syncSettingsToUI();
    }
  } catch (err) {
    console.warn("Failed to fetch settings from backend, using defaults.", err);
    syncSettingsToUI();
  }
}

async function saveSettings(settingsPayload) {
  try {
    const res = await fetch("http://127.0.0.1:5000/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(settingsPayload)
    });
    if (res.ok) {
      appSettings = await res.json();
      syncSettingsToUI();
    }
  } catch (err) {
    console.error("Error saving settings to backend:", err);
  }
}

function syncSettingsToUI() {
  headerBotName.innerText = appSettings.bot_name;
  usernameInput.value = appSettings.user_name;
  botnameInput.value = appSettings.bot_name;
  toneInput.value = appSettings.tone;
}

// ----------------------------------------------------
// 2. Speech Synthesis (TTS) & Male/Female Voice Logic
// ----------------------------------------------------
const synth = window.speechSynthesis;

function loadVoices() {
  allVoices = synth.getVoices();
  populateVoiceSelect();
}

// System voices can load asynchronously
if (synth.onvoiceschanged !== undefined) {
  synth.onvoiceschanged = loadVoices;
}
// Run once on load
loadVoices();

function populateVoiceSelect() {
  voiceSelect.innerHTML = "";
  
  // Filter voices based on gender preference
  const filtered = filterVoicesByGender(allVoices, voicePreference);

  // Add default option if none
  if (filtered.length === 0) {
    const option = document.createElement("option");
    option.textContent = "No matching voices found";
    option.value = "";
    voiceSelect.appendChild(option);
    return;
  }

  filtered.forEach(voice => {
    const option = document.createElement("option");
    option.value = voice.name;
    option.textContent = `${voice.name} (${voice.lang})`;
    
    if (voice.name === selectedVoiceName) {
      option.selected = true;
    }
    voiceSelect.appendChild(option);
  });

  // If no matching voice selected, pick the first one
  if (!voiceSelect.value && filtered.length > 0) {
    selectedVoiceName = filtered[0].name;
    localStorage.setItem("selectedVoiceName", selectedVoiceName);
  }
}

function filterVoicesByGender(voicesList, gender) {
  // Only target English and Indian English for MYRA
  const englishVoices = voicesList.filter(v => v.lang.startsWith("en-") || v.lang.startsWith("ta-"));
  const targetList = englishVoices.length > 0 ? englishVoices : voicesList;

  if (gender === "all") return targetList;

  return targetList.filter(voice => {
    const name = voice.name.toLowerCase();
    
    // Keywords indicating male gender
    const isMale = name.includes("male") || 
                   name.includes("david") || 
                   name.includes("ravi") || 
                   name.includes("george") || 
                   name.includes("mark") || 
                   name.includes("guy") || 
                   name.includes("stefan") || 
                   name.includes("microsoft david") ||
                   name.includes("google uk english male") ||
                   name.includes("standard-b") ||
                   name.includes("standard-d");

    if (gender === "male") return isMale;
    // Prefer female
    return !isMale;
  });
}

function speak(text) {
  if (isMuted) return;
  
  // Cancel current speak
  synth.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  
  // Find selected voice
  const voice = allVoices.find(v => v.name === selectedVoiceName);
  if (voice) {
    utterance.voice = voice;
  } else {
    // Fallback to first available English/Indian-English
    const fallback = allVoices.find(v => v.lang.startsWith("en-"));
    if (fallback) utterance.voice = fallback;
  }

  utterance.onstart = () => {
    isSpeaking = true;
    updateStatus("Speaking", "speaking", "🗣️");
  };

  utterance.onend = () => {
    isSpeaking = false;
    updateStatus("Ready to talk", "ready", "🤖");
  };

  utterance.onerror = () => {
    isSpeaking = false;
    updateStatus("Ready to talk", "ready", "🤖");
  };

  synth.speak(utterance);
}

// ----------------------------------------------------
// 3. Speech Recognition (STT)
// ----------------------------------------------------
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.lang = "en-IN";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    isListening = true;
    micBtn.classList.add("listening");
    updateStatus("Listening...", "listening", "👂");
    synth.cancel(); // Stop talking if the user starts speaking
  };

  recognition.onend = () => {
    isListening = false;
    micBtn.classList.remove("listening");
    updateStatus("Ready to talk", "ready", "🤖");
  };

  recognition.onresult = async (event) => {
    const transcript = event.results[0][0].transcript;
    handleUserQuery(transcript);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    if (event.error === 'not-allowed') {
      updateStatus("Mic permission denied", "ready", "⚠️");
    } else {
      updateStatus("Didn't catch that", "ready", "🤖");
    }
  };
} else {
  console.warn("Speech recognition not supported in this browser.");
  micBtn.style.display = "none";
}

// ----------------------------------------------------
// 4. Conversation Handlers
// ----------------------------------------------------
async function handleUserQuery(text) {
  if (!text.trim()) return;

  // Render user bubble
  appendMessage("You", text, false);

  updateStatus("Processing...", "speaking", "⚡");

  try {
    const res = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!res.ok) throw new Error("Server error");
    
    const data = await res.json();
    
    // Render bot bubble
    appendMessage(data.bot_name, data.reply, true);
    
    // Play text response
    speak(data.reply);

    // Run action if dispatched
    if (data.action) {
      executeAction(data.action);
    }

  } catch (err) {
    console.error("Chat error:", err);
    const errorMsg = "Sorry machi, server connect aagala. Check setup!";
    appendMessage("System", errorMsg, true);
    speak(errorMsg);
    updateStatus("Ready to talk", "ready", "🤖");
  }
}

function appendMessage(sender, text, isBot) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${isBot ? 'bot-msg' : 'user-msg'}`;
  
  const textHtml = isBot 
    ? `<div class="msg-bubble"><strong class="bot-label">${sender}:</strong> ${text}</div>`
    : `<div class="msg-bubble">${text}</div>`;

  msgDiv.innerHTML = textHtml;
  chatLogs.appendChild(msgDiv);
  chatLogs.scrollTop = chatLogs.scrollHeight;
}

// ----------------------------------------------------
// 5. Action Execution System
// ----------------------------------------------------
function executeAction(action) {
  console.log("Executing Action:", action);
  
  if (action.type === "open_url") {
    appendMessage("System", `Opening url: ${action.url}`, true);
    window.open(action.url, "_blank");
  } 
  
  else if (action.type === "change_theme") {
    document.body.className = `theme-${action.theme}`;
    localStorage.setItem("theme", action.theme);
    appendMessage("System", `Theme changed to ${action.theme.toUpperCase()}`, true);
  } 
  
  else if (action.type === "sync_settings") {
    appSettings = action.settings;
    syncSettingsToUI();
  } 
  
  else if (action.type === "clear_chat") {
    chatLogs.innerHTML = `
      <div class="message bot-msg">
        <div class="msg-bubble">
          Chat cleared. Enna machi, fresh-aa start pannalaama! 🚀
        </div>
      </div>
    `;
  }
}

// ----------------------------------------------------
// 6. UI Interaction & Control Bindings
// ----------------------------------------------------
// Mic Button Click
micBtn.onclick = () => {
  if (!recognition) {
    alert("Speech recognition not supported in this browser. Use input box instead.");
    return;
  }
  if (isListening) {
    recognition.stop();
  } else {
    try {
      recognition.start();
    } catch (e) {
      console.warn("Recognition already started or error: ", e);
    }
  }
};

// Form Text Query Submit
textForm.onsubmit = (e) => {
  e.preventDefault();
  const text = textQuery.value.trim();
  if (text) {
    handleUserQuery(text);
    textQuery.value = "";
  }
};

// Settings Panel Toggle
settingsToggleBtn.onclick = () => {
  settingsModal.classList.add("active");
  // Populate settings inputs
  syncSettingsToUI();
  voiceGenderInput.value = voicePreference;
  populateVoiceSelect();
};

const closeSettings = () => {
  settingsModal.classList.remove("active");
};
closeSettingsBtn.onclick = closeSettings;
settingsCloseBg.onclick = closeSettings;

// Mute Toggle Button
muteBtn.onclick = () => {
  isMuted = !isMuted;
  localStorage.setItem("isMuted", isMuted);
  updateMuteButtonUI();
  if (isMuted) {
    synth.cancel();
    isSpeaking = false;
    updateStatus("Ready to talk", "ready", "🤖");
  }
};

function updateMuteButtonUI() {
  muteBtn.innerText = isMuted ? "🔇" : "🔊";
  muteBtn.title = isMuted ? "Unmute Voice" : "Mute Voice";
}

// Save Settings Button click
saveSettingsBtn.onclick = () => {
  const user_name = usernameInput.value.trim() || appSettings.user_name;
  const bot_name = botnameInput.value.trim() || appSettings.bot_name;
  const tone = toneInput.value;
  
  voicePreference = voiceGenderInput.value;
  selectedVoiceName = voiceSelect.value;
  
  localStorage.setItem("voicePreference", voicePreference);
  localStorage.setItem("selectedVoiceName", selectedVoiceName);

  saveSettings({ user_name, bot_name, tone });
  closeSettings();
};

// Voice gender filter change
voiceGenderInput.onchange = () => {
  voicePreference = voiceGenderInput.value;
  populateVoiceSelect();
};

function updateStatus(text, dotClass, faceEmoji) {
  statusText.innerText = text;
  
  // Status Dot
  statusDot.className = "bot-status-indicator";
  if (dotClass) statusDot.classList.add(dotClass);

  // Bot face emoji
  botFace.innerText = faceEmoji;
}

// ----------------------------------------------------
// 7. Dynamic Canvas Audio Visualizer
// ----------------------------------------------------
function resizeCanvas() {
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

let phase = 0;
function drawVisualizer() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Get CSS colors based on active theme
  const style = getComputedStyle(document.body);
  const accentColor = style.getPropertyValue('--accent-color').trim() || '#a855f7';
  const secondaryColor = style.getPropertyValue('--accent-secondary').trim() || '#f43f5e';
  
  ctx.lineWidth = 2;
  
  let linesCount = 3;
  let amplitude = 6;
  let frequency = 0.02;
  let speed = 0.04;

  if (isListening) {
    linesCount = 5;
    amplitude = 25;
    frequency = 0.04;
    speed = 0.15;
  } else if (isSpeaking) {
    linesCount = 4;
    amplitude = 18;
    frequency = 0.03;
    speed = 0.1;
  } else {
    // Idle state: draw simple flat resting wave
    linesCount = 2;
    amplitude = 3;
    frequency = 0.01;
    speed = 0.02;
  }

  for (let i = 0; i < linesCount; i++) {
    ctx.beginPath();
    
    // Vary waves slightly
    const waveAmp = amplitude * (1 - i * 0.2);
    const waveFreq = frequency * (1 + i * 0.1);
    
    // Set color with fading alpha
    ctx.strokeStyle = i === 0 
      ? accentColor 
      : i === 1 ? secondaryColor : `rgba(255, 255, 255, ${0.15 - i * 0.03})`;

    for (let x = 0; x < canvas.width; x++) {
      // Draw wavy sine wave
      const y = canvas.height / 2 + 
                Math.sin(x * waveFreq + phase + i) * waveAmp * Math.sin(x * Math.PI / canvas.width);
      if (x === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.stroke();
  }
  
  phase += speed;
  requestAnimationFrame(drawVisualizer);
}

// Start visualizer draw loop
drawVisualizer();

// Fetch settings from server on page load
fetchSettings();
