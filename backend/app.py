from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

memory = {
    "user_name": "Nikesh",
    "bot_name": "MYRA",
    "tone": "friendly"
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_text = data.get("text", "").lower()

    name = memory["user_name"]
    bot = memory["bot_name"]

    # simple brain logic
    if "your name" in user_text or "who are you" in user_text:
        reply = f"Dei {name}, naan {bot} da 😄. Un personal AI machan."

    elif "how are you" in user_text:
        reply = f"Nalla irukken da {name}. Nee epdi irukka?"

    elif "what can you do" in user_text or "help" in user_text:
        reply = (
            f"{name}, naan un kooda pesuven, doubts explain pannuven, "
            "projects-la help pannuven, ideas kuduppen. "
            "Basically naan un AI machan 😎"
        )

    elif "project" in user_text:
        reply = (
            f"Aha {name}, project-aa 😏. "
            "Nee AI voice assistant project pannitu irukka nu theriyum. "
            "Next step epdi improve panna nu sollava?"
        )

    elif "thank" in user_text:
        reply = f"Parava illa da {name} 🤝. Naan irukken."

    else:
        reply = (
            f"Seri {name}, nee sonnadhu purinjiduchu. "
            "Idha konjam simple-aa explain panren. "
            f"'{user_text}' pathi detail-aa pesalaam da."
        )

    return jsonify({
        "reply": reply,
        "bot_name": bot
    })


if __name__ == "__main__":
    app.run(debug=True)
