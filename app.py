import os
from flask import Flask, render_template_string, request, jsonify
from google import genai

app = Flask(__name__)

# CONNEXION À GEMINI
API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


# INTERFACE KF AI
HTML = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>KF AI — Assistant intelligent</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    --bg: #101114;
    --panel: #191a20;
    --panel2: #22232b;
    --text: #f4f4f6;
    --muted: #9b9ca8;
    --accent: #8b5cf6;
    --accent2: #6d45dc;
    --border: #30313b;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100dvh;
    overflow: hidden;
}

.app {
    height: 100%;
    display: flex;
    flex-direction: column;
}

/* EN-TÊTE */

header {
    height: 70px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    border-bottom: 1px solid var(--border);
    background: rgba(25, 26, 32, 0.96);
}

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
}

.logo {
    width: 43px;
    height: 43px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #a78bfa, #6d28d9);
    font-size: 17px;
    font-weight: 900;
    box-shadow: 0 4px 18px #8b5cf633;
}

.brand-name {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.6px;
}

.brand-name span {
    color: #a78bfa;
}

.status {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    color: var(--muted);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #42d392;
}

/* BOUTONS */

button {
    font-family: inherit;
    cursor: pointer;
    border: none;
}

.new-chat {
    padding: 10px 13px;
    border: 1px solid var(--border);
    background: var(--panel2);
    color: var(--text);
    border-radius: 11px;
    font-size: 12px;
    font-weight: 600;
}

.new-chat:hover {
    background: #30313b;
}

/* ZONE DE CONVERSATION */

main {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    scroll-behavior: smooth;
}

.content {
    width: 100%;
    max-width: 820px;
    margin: 0 auto;
    padding: 30px 20px 25px;
}

.welcome {
    min-height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 35px 0 50px;
}

.welcome-icon {
    width: 76px;
    height: 76px;
    border-radius: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #8b5cf6, #4f46e5);
    font-size: 34px;
    margin-bottom: 25px;
    box-shadow: 0 10px 40px #8b5cf633;
}

.welcome h1 {
    font-size: clamp(27px, 5vw, 39px);
    line-height: 1.2;
    margin-bottom: 13px;
    letter-spacing: -1.2px;
}

.gradient {
    background: linear-gradient(90deg, #c4b5fd, #818cf8);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.welcome p {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.7;
    max-width: 390px;
}

.suggestions {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    margin-top: 34px;
}

.suggestion {
    text-align: left;
    padding: 17px;
    min-height: 94px;
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--text);
    border-radius: 16px;
    transition: 0.2s;
}

.suggestion:hover {
    border-color: #8b5cf6;
    transform: translateY(-2px);
}

.suggestion .emoji {
    font-size: 21px;
    display: block;
    margin-bottom: 10px;
}

.suggestion strong {
    font-size: 13px;
    display: block;
    margin-bottom: 5px;
}

.suggestion small {
    color: var(--muted);
    font-size: 11px;
    line-height: 1.5;
}

/* MESSAGES */

.message {
    display: flex;
    gap: 12px;
    margin-bottom: 27px;
    align-items: flex-start;
}

.avatar {
    width: 35px;
    height: 35px;
    flex-shrink: 0;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
}

.user-avatar {
    background: #343541;
    border: 1px solid #454652;
}

.ai-avatar {
    background: linear-gradient(135deg, #8b5cf6, #4f46e5);
}

.message-body {
    min-width: 0;
    flex: 1;
    padding-top: 3px;
}

.message-label {
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 9px;
}

.message-text {
    font-size: 14px;
    line-height: 1.8;
    overflow-wrap: anywhere;
    white-space: pre-wrap;
}

.user-message .message-text {
    display: inline-block;
    background: var(--panel2);
    border: 1px solid var(--border);
    padding: 12px 15px;
    border-radius: 5px 16px 16px 16px;
}

.message-text strong {
    font-weight: 750;
}

.message-text code {
    background: #292a34;
    padding: 3px 6px;
    border-radius: 5px;
    font-family: monospace;
}

.message-text pre {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    background: #0c0d11;
    border: 1px solid var(--border);
    padding: 14px;
    margin: 10px 0;
    border-radius: 12px;
    font-size: 12px;
    overflow-x: auto;
}

.typing {
    color: var(--muted);
    font-size: 13px;
    animation: pulse 1.2s infinite;
}

@keyframes pulse {
    50% { opacity: 0.45; }
}

/* ZONE DE SAISIE */

footer {
    flex-shrink: 0;
    padding: 12px 18px 10px;
    border-top: 1px solid var(--border);
    background: var(--bg);
}

.composer {
    max-width: 820px;
    margin: 0 auto;
}

.input-box {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    padding: 10px;
    border: 1px solid #41414e;
    background: var(--panel);
    border-radius: 18px;
    transition: border-color 0.2s;
}

.input-box:focus-within {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px #8b5cf615;
}

textarea {
    flex: 1;
    width: 100%;
    min-width: 0;
    max-height: 150px;
    resize: none;
    outline: none;
    border: none;
    background: transparent;
    color: var(--text);
    font-family: inherit;
    font-size: 14px;
    line-height: 1.6;
    padding: 7px 5px;
}

textarea::placeholder {
    color: #777886;
}

.send-btn {
    width: 43px;
    height: 43px;
    flex-shrink: 0;
    border-radius: 13px;
    background: var(--accent);
    color: white;
    font-size: 19px;
    font-weight: bold;
    transition: 0.2s;
}

.send-btn:hover {
    background: var(--accent2);
}

.send-btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
}

.footer-note {
    text-align: center;
    font-size: 10px;
    color: #747581;
    margin-top: 10px;
    line-height: 1.5;
}

/* PETITS ÉCRANS */

@media (max-width: 500px) {
    header {
        height: 63px;
        padding: 0 13px;
    }

    .logo {
        width: 38px;
        height: 38px;
        border-radius: 12px;
    }

    .brand-name {
        font-size: 19px;
    }

    .content {
        padding: 18px 14px 22px;
    }

    .welcome {
        padding: 25px 0;
    }

    .welcome-icon {
        width: 65px;
        height: 65px;
        border-radius: 21px;
        font-size: 29px;
        margin-bottom: 20px;
    }

    .welcome p {
        font-size: 13px;
    }

    .suggestions {
        gap: 9px;
        margin-top: 27px;
    }

    .suggestion {
        padding: 13px;
        min-height: 100px;
        border-radius: 14px;
    }

    .suggestion strong {
        font-size: 12px;
    }

    .suggestion small {
        font-size: 10px;
    }

    footer {
        padding: 10px 10px 8px;
    }

    .message {
        gap: 9px;
        margin-bottom: 23px;
    }

    .avatar {
        width: 31px;
        height: 31px;
        border-radius: 10px;
    }

    .message-text {
        font-size: 13px;
    }

    .new-chat {
        padding: 9px 10px;
    }
}

@media (max-width: 350px) {
    .status {
        display: none;
    }

    .suggestions {
        grid-template-columns: 1fr;
    }
}
</style>
</head>

<body>
<div class="app">

    <header>
        <div class="brand">
            <div class="logo">KF</div>
            <div class="brand-name">KF <span>AI</span></div>
        </div>

        <div class="status">
            <span class="status-dot"></span>
            Assistant IA
        </div>

        <button class="new-chat" onclick="newChat()">
            ＋ Nouveau
        </button>
    </header>

    <main id="main">
        <div class="content" id="content">

            <section class="welcome" id="welcome">
                <div class="welcome-icon">✦</div>

                <h1>
                    Bonjour, bienvenue sur<br>
                    <span class="gradient">KF AI.</span>
                </h1>

                <p>
                    Ton assistant intelligent pour apprendre,
                    créer, programmer et explorer de nouvelles idées.
                </p>

                <div class="suggestions">

                    <button class="suggestion"
                    onclick="askSuggestion('Explique-moi un concept scientifique simplement.')">
                        <span class="emoji">🧠</span>
                        <strong>Apprendre</strong>
                        <small>Comprendre des concepts complexes</small>
                    </button>

                    <button class="suggestion"
                    onclick="askSuggestion('Aide-moi à écrire un programme informatique.')">
                        <span class="emoji">💻</span>
                        <strong>Programmer</strong>
                        <small>Créer et corriger du code</small>
                    </button>

                    <button class="suggestion"
                    onclick="askSuggestion('Aide-moi à apprendre l’anglais avec des exemples.')">
                        <span class="emoji">🌍</span>
                        <strong>Apprendre les langues</strong>
                        <small>Vocabulaire, grammaire et traduction</small>
                    </button>

                    <button class="suggestion"
                    onclick="askSuggestion('Propose-moi des idées originales pour un projet.')">
                        <span class="emoji">✨</span>
                        <strong>Créer</strong>
                        <small>Développer de nouvelles idées</small>
                    </button>

                </div>
            </section>

            <div id="messages"></div>

        </div>
    </main>

    <footer>
        <div class="composer">

            <div class="input-box">
                <textarea
                    id="input"
                    rows="1"
                    maxlength="12000"
                    placeholder="Pose ta question à KF AI..."
                    aria-label="Ton message"
                ></textarea>

                <button
                    id="send"
                    class="send-btn"
                    onclick="sendMessage()"
                    aria-label="Envoyer le message"
                >↑</button>
            </div>

            <div class="footer-note">
                KF AI peut parfois se tromper.
                Vérifie les informations importantes.
            </div>

        </div>
    </footer>

</div>

<script>
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const messages = document.getElementById("messages");
const main = document.getElementById("main");

let history = [];
let busy = false;

function escapeHTML(text) {
    return String(text).replace(/[&<>"']/g, function(c) {
        return {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        }[c];
    });
}

/* Mise en forme simple et sécurisée des réponses */
function formatText(text) {
    let safe = escapeHTML(text);

    safe = safe.replace(
        /```(?:[a-zA-Z0-9_-]+)?\n?([\s\S]*?)```/g,
        function(_, code) {
            return "<pre><code>" + code + "</code></pre>";
        }
    );

    safe = safe.replace(
        /`([^`\n]+)`/g,
        "<code>$1</code>"
    );

    safe = safe.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );

    return safe;
}

function addMessage(role, text, id = "") {
    const row = document.createElement("div");

    row.className = "message " +
        (role === "user" ? "user-message" : "ai-message");

    if (id) row.id = id;

    const avatar = document.createElement("div");
    avatar.className = "avatar " +
        (role === "user" ? "user-avatar" : "ai-avatar");

    avatar.textContent = role === "user" ? "Toi" : "KF";

    const body = document.createElement("div");
    body.className = "message-body";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = role === "user" ? "Toi" : "KF AI";

    const content = document.createElement("div");
    content.className = "message-text";

    if (text) {
        content.innerHTML = formatText(text);
    }

    body.appendChild(label);
    body.appendChild(content);

    row.appendChild(avatar);
    row.appendChild(body);

    messages.appendChild(row);

    main.scrollTop = main.scrollHeight;

    return content;
}

function askSuggestion(text) {
    input.value = text;
    sendMessage();
}

async function sendMessage() {
    const message = input.value.trim();

    if (!message || busy) return;

    busy = true;
    sendBtn.disabled = true;

    document.getElementById("welcome").style.display = "none";

    addMessage("user", message);

    input.value = "";
    input.style.height = "auto";

    const loading = addMessage(
        "assistant",
        "KF AI prépare sa réponse...",
        "loading"
    );

    loading.classList.add("typing");

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                history: history.slice(-12)
            })
        });

        const data = await response.json();

        document.getElementById("loading").remove();

        if (!response.ok) {
            throw new Error(data.error || "Une erreur est survenue.");
        }

        const answer = data.response;

        addMessage("assistant", answer);

        history.push(
            {role: "user", text: message},
            {role: "assistant", text: answer}
        );

        history = history.slice(-20);

    } catch (error) {
        const loadingElement = document.getElementById("loading");

        if (loadingElement) loadingElement.remove();

        addMessage(
            "assistant",
            "⚠️ " + (error.message ||
            "Impossible d'obtenir une réponse. Réessaie plus tard.")
        );
    }

    busy = false;
    sendBtn.disabled = false;
    input.focus();
}

function newChat() {
    history = [];
    messages.innerHTML = "";

    document.getElementById("welcome").style.display = "flex";

    input.value = "";
    input.focus();
}

input.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 150) + "px";
});

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
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
    if not client:
        return jsonify({
            "error": "La clé Gemini n'est pas configurée dans Render."
        }), 500

    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return jsonify({
            "error": "Écris un message avant de l'envoyer."
        }), 400

    if len(message) > 12000:
        return jsonify({
            "error": "Ton message est trop long."
        }), 400

    # Conserver le contexte récent de la conversation
    contents = []

    for item in history[-12:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        text = item.get("text", "")

        if role not in ("user", "assistant"):
            continue

        if not isinstance(text, str) or not text.strip():
            continue

        contents.append({
            "role": "model" if role == "assistant" else "user",
            "parts": [{"text": text[:12000]}]
        })

    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=contents
        )

        answer = response.text

        if not answer:
            return jsonify({
                "error": "Gemini n'a pas renvoyé de réponse. Réessaie."
            }), 502

        return jsonify({"response": answer})

        except Exception as e:
        app.logger.exception("Erreur lors de l'appel à Gemini")

        erreur = str(e)
        app.logger.error("Détail Gemini : %s", erreur)

        if "503" in erreur or "UNAVAILABLE" in erreur:
            message_erreur = (
                "Google est temporairement surchargé. "
                "Réessaie dans quelques secondes."
            )
        elif "429" in erreur or "RESOURCE_EXHAUSTED" in erreur:
            message_erreur = (
                "La limite de requêtes Google est atteinte. "
                "Attends un peu avant de réessayer."
            )
        elif "404" in erreur or "NOT_FOUND" in erreur:
            message_erreur = (
                "Le modèle Gemini demandé est indisponible. "
                "Vérifie le nom du modèle dans app.py."
            )
        elif "403" in erreur or "PERMISSION_DENIED" in erreur:
            message_erreur = (
                "Google refuse la requête. Vérifie la clé API "
                "et les autorisations dans Google AI Studio."
            )
        else:
            message_erreur = (
                "Erreur Gemini : " + erreur[:250]
            )

        return jsonify({"error": message_erreur}), 502
