# 🎙️ AI Voice Assistant

A simple AI Voice Assistant built using **Python Flask**, **HTML**, **CSS**, and **JavaScript**. The assistant can understand voice commands, respond with speech, and maintain basic conversational memory for a personalized user experience.

---

## 🚀 Features

- 🎤 Voice Input using Web Speech API
- 🔊 Text-to-Speech Responses
- 💬 Interactive Chat Interface
- 🧠 Basic Memory System
- ⚡ Real-time Communication using Flask API
- 🎨 Clean and Responsive UI
- 🌐 Frontend & Backend Separation

---

## 📂 Project Structure

```bash
ai-voice-assistant/
│
├── backend/
│   └── app.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── README.md
```

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript
- Web Speech API

### Backend
- Python
- Flask
- Flask-CORS

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-voice-assistant.git
cd ai-voice-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask flask-cors
```

---

## ▶️ Running the Project

### Start Backend

```bash
cd backend
python app.py
```

Backend runs on:

```bash
http://127.0.0.1:5000
```

### Start Frontend

Open `frontend/index.html`

OR

Use VS Code Live Server:

```bash
Right Click → Open with Live Server
```

Frontend runs on:

```bash
http://127.0.0.1:5500
```

---

## 🧠 Assistant Memory

Current assistant memory example:

```python
memory = {
    "user_name": "Nikesh",
    "bot_name": "MYRA",
    "tone": "friendly"
}
```

The assistant can remember:

- User Name
- Bot Name
- Conversation Tone

---

## 🎤 Voice Interaction

### Speech Recognition

Converts user voice into text using:

```javascript
SpeechRecognition
```

### Speech Synthesis

Converts assistant responses into speech using:

```javascript
speechSynthesis
```

---

## 📸 Screenshots

Add screenshots here:

### Main Interface

![Home Screen](images/home.png)

### Voice Assistant Working

![Assistant](images/assistant.png)

---

## 🔮 Future Improvements

- OpenAI API Integration
- Gemini API Integration
- Wake Word Detection
- Multi-language Support
- Persistent Database Memory
- User Authentication
- Chat History Storage
- Smart Task Automation

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push to branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Nikesh Babu S**


---

⭐ If you found this project useful, consider giving it a star on GitHub.
