import os
from flask import Flask, render_template_string, request, jsonify
from google import genai

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#10131a">
    <title>KF AI</title>
    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            background: #10131a;
            color: #f5f7fb;
            font-family: Arial, sans-serif;
            min-height: 100vh;
        }

        header {
            padding: 18px;
            border-bottom: 1px solid #292e3a;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo {
            background: linear-gradient(135deg, #6d5dfc, #00c9a7);
            color: white;
            font-weight: bold;
            font-size: 21px;
            padding: 11px;
            border-radius: 13px;
        }

        .brand { font-size: 23px; font-weight: bold; }

        .subtitle {
            color: #9da6b8;
            font-size: 12px;
            margin-top: 4px;
        }

        main {
            max-width: 850px;
            margin: auto;
            padding: 25px 16px 150px;
        }

        .welcome {
            text-align: center;
            margin: 55px 0 35px;
        }

        .welcome h1 {
            font-size: clamp(29px, 7vw, 43px);
            margin-bottom: 12px;
        }

        .welcome p { color: #aab2c2; line-height: 1.6; }

        #messages {
            display: flex;
            flex-direction: column;
            gap: 18px;
        }

        .message {
            padding: 15px 17px;
            border-radius: 17px;
            line-height: 1.65;
            overflow-wrap: anywhere;
            white-space: pre-wrap;
        }

        .user {
            background: #292f40;
            align-self: flex-end;
            max-width: 90%;
        }

        .assistant {
            background: #191e29;
            border: 1px solid #2b3140;
            align-self: stretch;
        }

        .composer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 15px;
            background: linear-gradient(transparent, #10131a 20%);
        }

        .composer-inner {
            max-width: 820px;
            margin: auto;
            background: #1b202c;
            border: 1px solid #343b4b;
            border-radius: 20px;
            padding: 10px;
            display: flex;
            gap: 10px;
            align-items: flex-end;
        }

        textarea {
            flex: 1;
            min-width: 0;
            resize: none;
            max-height: 130px;
            border: 0;
            outline: none;
            background: transparent;
            color: white;
            font-size: 16px;
            padding: 10px;
            font-family: inherit;
        }

        button {
            border: 0;
            cursor: pointer;
            border-radius: 13px;
            padding: 12px 15px;
            font-size: 15px;
            font-weight: bold;
        }

        #send { background: #7165f5; color: white; }
        #send:disabled { opacity: .5; }

        .note {
            text-align: center;
            font-size: 11px;
            color: #8992a5;
            margin-top: 10px;
        }

        @media (max-width: 480px) {
            main { padding-left: 12px; padding-right: 12px; }
            .welcome { margin-top: 40px; }
            .message { font-size: 15px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">KF</div>
        <div>
            <div class="brand">KF AI</div>
            <div class="subtitle">La plus grande commence ici</div>
        </div>
    </header>

    <main>
        <section class="welcome" id="welcome">
            <h1>Que pouvons-nous explorer ?</h1>
            <p>Pose une question, découvre un concept ou imagine quelque chose de nouveau.</p>
        </section>
        <section id="messages" aria-live="polite"></section>
    </main>

    <section class="composer">
        <form id="chat-form" class="composer-inner">
            <textarea id="prompt"
                placeholder="Pose ta question à KF AI..."
                rows="1" required></textarea>
            <button id="send" type="submit">➤</button>
        </form>
        <div class="note">
            KF AI peut commettre des erreurs. Vérifie les informations importantes.
        </div>
    </section>

    <script>
        const form = document.getElementById("chat-form");
        const promptBox = document.getElementById("prompt");
        const messages = document.getElementById("messages");
        const sendButton = document.getElementById("send");
        const welcome = document.getElementById("welcome");

        function addMessage(text, role) {
            const div = document.createElement("div");
            div.className = "message " + role;
            div.textContent = text;
            messages.appendChild(div);
            div.scrollIntoView({ behavior: "smooth", block: "end" });
            return div;
        }

        promptBox.addEventListener("input", () => {
            promptBox.style.height = "auto";
            promptBox.style.height =
                Math.min(promptBox.scrollHeight, 130) + "px";
        });

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const text = promptBox.value.trim();
            if (!text) return;

            welcome.style.display = "none";
            addMessage(text, "user");
            promptBox.value = "";
            promptBox.style.height = "auto";
            sendButton.disabled = true;

            const waiting = addMessage(
                "KF AI réfléchit...",
                "assistant"
            );

            try {
                const response = await fetch("/api/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: text})
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Erreur inconnue.");
                }

                waiting.textContent = data.reply;
            } catch (error) {
                waiting.textContent = "Erreur : " + error.message;
            } finally {
                sendButton.disabled = false;
                promptBox.focus();
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Écris d'abord un message."}), 400

    if not client:
        return jsonify({
            "error": "La clé GEMINI_API_KEY n'est pas configurée dans Render."
        }), 500

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )

        answer = response.text

        if not answer:
            answer = "Je n'ai pas pu générer de réponse. Réessaie."

        return jsonify({"reply": answer})

    except Exception as error:
        app.logger.exception("Erreur lors de l'appel à Gemini")
        return jsonify({
            "error": "Impossible d'obtenir une réponse de Gemini. Vérifie les paramètres de l'API et réessaie."
        }), 502


if __name__ == "__main__":
    app.run()
