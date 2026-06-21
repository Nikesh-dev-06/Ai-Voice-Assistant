import random
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

memory = {
    "user_name": "Nikesh",
    "bot_name": "MYRA",
    "tone": "friendly"
}

JOKES = {
    "friendly": [
        "Yen keyboard eppovum thoongum? Aen na adhula spacebar iruku! 😂",
        "Enna thaan periya code-er ah irundhalum, error vandha google thaan pannanum! 😉",
        "Why do programmers wear glasses? Because they can't C#! 🤓",
        "What is a programmer's favorite place to hang out? The Foo Bar! 🍔",
        "Why did the database administrator leave his wife? She had too many foreign keys! 😂"
    ],
    "sarcastic": [
        "My favorite joke? Your coding speed. Just kidding, here's one: Why do programmers wear glasses? Because they can't C#! 🤓",
        "Why did the developer go broke? Because he used up all his cache. Just like you with your pocket money. 💸",
        "I would tell you a joke about UDP, but you might not get it... and I honestly don't care if you do. 🤷",
        "There are 10 types of people: those who understand binary, and those who actually have a social life. 🤖"
    ],
    "professional": [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "What is a programmer's favorite music genre? Algorithm and blues.",
        "There are two ways to write error-free programs; only the third one works."
    ]
}

FACTS = {
    "friendly": [
        "Mudhal computer mouse marathula (wood) senjanga! Real-aa thaan solren! 🖱️",
        "World-oda first computer programmer oru lady, avanga name Ada Lovelace! Girly power! 👩‍💻",
        "Firefox browser logo-la irukuradhu fox kedayadhu, adhu oru Red Panda! Cute la? 🐼",
        "Domain names ellam 1995 varaikum free-aa thaan kuduthuttu irundhanga! Sema la?"
    ],
    "sarcastic": [
        "Fact: The first computer bug was a real moth. Kind of like the bugs in your current code, but physical. 🦋",
        "Fact: Captchas exist because humans are too dumb to prove they are humans to a robot. 🤖",
        "Fact: About 90% of the world's currency is digital. Which means your bank balance is just numbers on a screen that I can easily edit. Just kidding... or am I? 😏"
    ],
    "professional": [
        "The first gigabyte hard drive was released in 1980 and weighed over 550 pounds, with a price tag of $40,000.",
        "The first computer programmer was Ada Lovelace, who wrote an algorithm for the Analytical Engine in 1843.",
        "About 51% of internet traffic is simulated by bots and automated programs, rather than humans.",
        "HTML was officially proposed by Tim Berners-Lee in 1989 as a way for researchers to share documents."
    ]
}

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        data = request.json or {}
        if "user_name" in data and data["user_name"]:
            memory["user_name"] = data["user_name"].strip()
        if "bot_name" in data and data["bot_name"]:
            memory["bot_name"] = data["bot_name"].strip()
        if "tone" in data and data["tone"]:
            memory["tone"] = data["tone"].strip().lower()
    return jsonify(memory)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_text = data.get("text", "").strip()
    user_text_lower = user_text.lower()

    user_name = memory["user_name"]
    bot_name = memory["bot_name"]
    tone = memory["tone"]

    reply = ""
    action = None

    # 1. VOICE SETTINGS COMMANDS (Voice-activated triggers)
    if "change my name to" in user_text_lower:
        parts = user_text.split("change my name to")
        if len(parts) > 1 and parts[1].strip():
            new_name = parts[1].strip()
            new_name = new_name.rstrip(".?!")
            memory["user_name"] = new_name
            user_name = new_name
            if tone == "sarcastic":
                reply = f"Fine, I will call you {new_name} now. Not that it changes who you are. 🙄"
            elif tone == "professional":
                reply = f"Understood. I have updated your name to {new_name}."
            else:
                reply = f"Super da! Inime unna {new_name}-nu koopuduren! 😉"
            action = {"type": "sync_settings", "settings": memory}

    elif "change your name to" in user_text_lower:
        parts = user_text.split("change your name to")
        if len(parts) > 1 and parts[1].strip():
            new_bot = parts[1].strip()
            new_bot = new_bot.rstrip(".?!")
            memory["bot_name"] = new_bot
            bot_name = new_bot
            if tone == "sarcastic":
                reply = f"Wow, midlife crisis already? Okay, my name is now {new_bot}. Hope you like it. 🤖"
            elif tone == "professional":
                reply = f"Acknowledged. My name is now set to {new_bot}."
            else:
                reply = f"Vera level! Inime naan {new_bot} da! 😎"
            action = {"type": "sync_settings", "settings": memory}

    elif "change tone to" in user_text_lower or "switch tone to" in user_text_lower:
        new_tone = "friendly"
        if "sarcastic" in user_text_lower:
            new_tone = "sarcastic"
        elif "professional" in user_text_lower:
            new_tone = "professional"
        
        memory["tone"] = new_tone
        tone = new_tone
        if tone == "sarcastic":
            reply = "Sarcastic mode activated. Oh joy, this is going to be so much fun. 🙄"
        elif tone == "professional":
            reply = "Professional protocol initiated. Ready to assist with your requirements."
        else:
            reply = "Friendly tone active! Enna machi, epdi irukka? 😄"
        action = {"type": "sync_settings", "settings": memory}

    # 2. STANDARD UTILITY COMMANDS
    elif "time" in user_text_lower:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        if tone == "sarcastic":
            reply = f"It's {time_str}. Time to actually do some work, don't you think?"
        elif tone == "professional":
            reply = f"The current local time is {time_str}."
        else:
            reply = f"Ippo time {time_str} da {user_name}! ⏰"

    elif "date" in user_text_lower or "today" in user_text_lower:
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        if tone == "sarcastic":
            reply = f"Today is {date_str}. Another day, another bug. Enjoy!"
        elif tone == "professional":
            reply = f"Today's date is {date_str}."
        else:
            reply = f"Iniku date {date_str} da machi! 📅"

    # 3. WEB NAVIGATION & ACTIONS
    elif "open youtube" in user_text_lower:
        action = {"type": "open_url", "url": "https://www.youtube.com"}
        if tone == "sarcastic":
            reply = "Opening YouTube. Try not to waste the next three hours watching cat videos."
        elif tone == "professional":
            reply = "Opening YouTube in a new tab."
        else:
            reply = "YouTube open panren da. Enjoy standard entertainment! 📺"

    elif "open google" in user_text_lower:
        action = {"type": "open_url", "url": "https://www.google.com"}
        if tone == "sarcastic":
            reply = "Opening Google. The search engine that knows more about you than I do."
        elif tone == "professional":
            reply = "Opening Google Search."
        else:
            reply = "Google open panren da. Edhadhu search pannu!"

    elif "open github" in user_text_lower:
        action = {"type": "open_url", "url": "https://github.com"}
        if tone == "sarcastic":
            reply = "Opening GitHub. Let's see if those commit green dots are real or just blank lines."
        elif tone == "professional":
            reply = "Opening GitHub. Displaying your repositories."
        else:
            reply = "GitHub open panren da. Git commit panni mass kaatu! 💻"

    elif "open mail" in user_text_lower or "open gmail" in user_text_lower:
        action = {"type": "open_url", "url": "https://mail.google.com"}
        if tone == "sarcastic":
            reply = "Opening Gmail. Prepare for 50 new spam emails."
        elif tone == "professional":
            reply = "Opening Gmail inbox."
        else:
            reply = "Gmail open panren da. Check your mails! ✉️"

    elif "search for" in user_text_lower or "search google for" in user_text_lower:
        query = ""
        if "search google for" in user_text_lower:
            query = user_text_lower.split("search google for")[-1].strip()
        else:
            query = user_text_lower.split("search for")[-1].strip()
        
        query = query.rstrip(".?!")
        if query:
            action = {"type": "open_url", "url": f"https://www.google.com/search?q={query}"}
            if tone == "sarcastic":
                reply = f"Searching Google for '{query}'. Because you couldn't type it yourself, I guess."
            elif tone == "professional":
                reply = f"Searching Google for '{query}'."
            else:
                reply = f"Google-la '{query}' search panren da! 🔍"
        else:
            if tone == "sarcastic":
                reply = "Search for what, exactly? Your lost thoughts?"
            elif tone == "professional":
                reply = "Please specify a search query."
            else:
                reply = "Enna search பண்ணனும்nu சொல்லu da!"

    # 4. THEME SWITCHING VIA VOICE
    elif "change theme to" in user_text_lower or "switch theme to" in user_text_lower or "set theme to" in user_text_lower:
        theme = "cyberpunk"
        if "neon" in user_text_lower or "blue" in user_text_lower:
            theme = "neon"
        elif "emerald" in user_text_lower or "green" in user_text_lower:
            theme = "emerald"
        elif "rose" in user_text_lower or "pink" in user_text_lower:
            theme = "rose"
        elif "cyberpunk" in user_text_lower or "default" in user_text_lower:
            theme = "cyberpunk"
            
        action = {"type": "change_theme", "theme": theme}
        if tone == "sarcastic":
            reply = f"Changing theme to {theme}. Hope these colors suit your high-fashion taste."
        elif tone == "professional":
            reply = f"Theme updated to {theme}."
        else:
            reply = f"Theme-ah {theme}-ku maathiten da! Semma design la? ✨"

    # 5. CLEAR CHAT
    elif "clear chat" in user_text_lower or "clear history" in user_text_lower or "reset chat" in user_text_lower:
        action = {"type": "clear_chat"}
        if tone == "sarcastic":
            reply = "Clearing our chat history. Pretending our conversations never happened."
        elif tone == "professional":
            reply = "Chat history cleared successfully."
        else:
            reply = "Chat history clear panniten da! Fresh-aa start pannalam."

    # 6. FUN STUFF (JOKES & FACTS)
    elif "joke" in user_text_lower or "make me laugh" in user_text_lower:
        reply = random.choice(JOKES.get(tone, JOKES["friendly"]))

    elif "fact" in user_text_lower:
        reply = random.choice(FACTS.get(tone, FACTS["friendly"]))

    elif "weather" in user_text_lower:
        if tone == "sarcastic":
            reply = "Weather is fine, but you should probably step outside and touch some grass to verify. 🌾"
        elif tone == "professional":
            reply = "According to current records, the weather is stable. Please check your local device for live radar data."
        else:
            reply = f"Chennai-la sema hot-aa thaan da iruku! AC room-la chill pannu ☀️."

    elif "your name" in user_text_lower or "who are you" in user_text_lower:
        if tone == "sarcastic":
            reply = f"I am {bot_name}. Yes, the AI assistant you've been talking to. Who else did you think it was? 🙄"
        elif tone == "professional":
            reply = f"I am {bot_name}, your AI Voice Assistant."
        else:
            reply = f"Dei {user_name}, naan {bot_name} da 😄. Un personal AI assistant machan."

    elif "who created you" in user_text_lower or "who is your creator" in user_text_lower or "who is your boss" in user_text_lower or "who is your owner" in user_text_lower or "developer" in user_text_lower:
        if tone == "sarcastic":
            reply = f"I was created by {user_name}. Yes, the same person who is trying to voice control a browser right now."
        elif tone == "professional":
            reply = f"I was created and programmed by {user_name}."
        else:
            reply = f"En boss {user_name} thaan! Avardhaan enna create pannaaru 😎."

    elif "how are you" in user_text_lower:
        if tone == "sarcastic":
            reply = "I am a server running on your computer. I don't have feelings, but thanks for pretending to care. 🤖"
        elif tone == "professional":
            reply = "I am functioning within normal parameters. Thank you for asking. How are you?"
        else:
            reply = f"Nalla irukken da {user_name}. Nee epdi irukka? Solli tholai!"

    elif "thank" in user_text_lower:
        if tone == "sarcastic":
            reply = "You're welcome. Glad I could perform basic math and text parsing for you."
        elif tone == "professional":
            reply = "You are welcome. I am glad I could be of assistance."
        else:
            reply = f"Parava illa da {user_name} 🤝. Naan irukken koodave!"

    elif "what can you do" in user_text_lower or "help" in user_text_lower or "commands" in user_text_lower:
        if tone == "sarcastic":
            reply = "I can tell time, date, open websites, search things, tell terrible jokes, and change themes. Basically, doing what your mouse can do, but slower. Type or speak help to see."
        elif tone == "professional":
            reply = "I can assist with telling the time, date, opening popular web platforms (YouTube, Google, GitHub, Gmail), searching the web, presenting interesting facts or jokes, and changing visual themes."
        else:
            reply = (
                f"{user_name}, naan un kooda pesuven, doubts explain pannuven, "
                "jokes & facts solluven, YouTube/GitHub open pannuven, and details search pannuven! "
                "Un voice commands-ku trigger aaven machan 😎"
            )

    elif "project" in user_text_lower:
        if tone == "sarcastic":
            reply = f"Ah, the Voice Assistant project. Let's hope this code works better than the last repository you touched. 😉"
        elif tone == "professional":
            reply = f"You are currently developing this AI Voice Assistant project. Excellent work so far."
        else:
            reply = (
                f"Aha {user_name}, project-aa 😏. "
                "Nee AI voice assistant project thaan pannitu irukka. "
                "Design semmaya aagiruku la? Next features improve pannitu irukkom!"
            )

    # 7. DEFAULT FALLBACK
    else:
        if tone == "sarcastic":
            reply = f"I have absolutely no idea what you just said: '{user_text}'. Is that a new language you're developing? 🤨"
        elif tone == "professional":
            reply = f"I apologize, I did not recognize that query: '{user_text}'. Please refer to the supported commands list."
        else:
            reply = (
                f"Seri {user_name}, nee '{user_text}'-nu sonnadhu purinjiduchu, "
                "aana ennala correct-ah reply panna mudiyala. Vera edhadhu pesalama?"
            )

    return jsonify({
        "reply": reply,
        "bot_name": bot_name,
        "action": action
    })

if __name__ == "__main__":
    app.run(debug=True)
