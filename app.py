import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from groq import Groq

app = FastAPI()

# HTML e CSS integrato con stile HUD futuristico e linee neon blu/rosse
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E.V. // Interfaccia Neurale</title>
    <style>
        :root {
            --bg-color: #030712;
            --panel-bg: #0f172a;
            --accent-blue: #38bdf8;
            --accent-red: #f43f5e;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --border-glow: rgba(56, 189, 248, 0.3);
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }

        header {
            background: var(--panel-bg);
            border-bottom: 2px solid var(--accent-blue);
            padding: 15px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 0 15px var(--border-glow);
        }

        header h1 {
            margin: 0;
            font-size: 1.2rem;
            color: var(--accent-blue);
            letter-spacing: 2px;
        }

        .status {
            font-size: 0.8rem;
            color: var(--accent-red);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .main-container {
            display: flex;
            flex: 1;
            overflow: hidden;
        }

        sidebar {
            width: 300px;
            background: #090d16;
            border-right: 1px solid #1e293b;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        sidebar label {
            font-size: 0.85rem;
            color: var(--text-dim);
        }

        sidebar input {
            background: var(--panel-bg);
            border: 1px solid var(--accent-blue);
            color: var(--text-main);
            padding: 8px;
            font-family: monospace;
            border-radius: 4px;
        }

        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: radial-gradient(circle at center, #0f172a 0%, #030712 100%);
        }

        .messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .message {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 0.95rem;
            line-height: 1.4;
        }

        .message.user {
            background: #1e293b;
            border-left: 3px solid var(--accent-red);
            align-self: flex-end;
        }

        .message.assistant {
            background: #0b1329;
            border-left: 3px solid var(--accent-blue);
            align-self: flex-start;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.1);
        }

        .input-bar {
            padding: 20px;
            background: var(--panel-bg);
            border-top: 1px solid #1e293b;
            display: flex;
            gap: 10px;
        }

        .input-bar input {
            flex: 1;
            background: var(--bg-color);
            border: 1px solid var(--accent-blue);
            color: var(--text-main);
            padding: 12px;
            font-family: monospace;
            border-radius: 4px;
        }

        .input-bar button {
            background: var(--accent-blue);
            color: #030712;
            border: none;
            padding: 0 25px;
            font-weight: bold;
            font-family: monospace;
            cursor: pointer;
            border-radius: 4px;
            transition: 0.2s;
        }

        .input-bar button:hover {
            background: #7dd3fc;
            box-shadow: 0 0 10px var(--accent-blue);
        }
    </style>
</head>
<body>

    <header>
        <h1>🕸️ E.V. // SISTEMA DI SUPPORTO NEURALE</h1>
        <div class="status">● LIVELLO SICUREZZA: ALTO</div>
    </header>

    <div class="main-container">
        <sidebar>
            <form method="post" action="/config">
                <label>CHIAVE API GROQ:</label><br><br>
                <input type="password" name="api_key" value="{{ api_key }}" placeholder="Inserisci chiave..." style="width: 90%;">
                <br><br>
                <button type="submit" style="background:#1e293b; color:#38bdf8; border:1px solid #38bdf8; padding:6px 12px; cursor:pointer; font-family:monospace;">Aggiorna</button>
            </form>
            <hr style="border-color:#1e293b; width:100%;">
            <div style="font-size:0.8rem; color:var(--text-dim);">
                <p><b>Protocollo:</b> Attivo</p>
                <p><b>Modello:</b> Llama 3.3</p>
            </div>
        </sidebar>

        <div class="chat-area">
            <div class="messages">
                {% if not api_key %}
                <div class="message assistant">
                    <b>E.V.:</b> Configurazione iniziale richiesta. Inserisci la tua chiave API di Groq nella barra laterale per stabilire il collegamento neurale.
                </div>
                {% endif %}
                
                {% for msg in history %}
                <div class="message {{ msg.role }}">
                    <b>{{ 'Tu' if msg.role == 'user' else 'E.V.' }}:</b> {{ msg.content }}
                </div>
                {% endfor %}
            </div>

            <form class="input-bar" method="post" action="/chat">
                <input type="text" name="prompt" placeholder="Inserisci comando o domanda per E.V...." autocomplete="off" required>
                <button type="submit">INVIA</button>
            </form>
        </div>
    </div>

</body>
</html>
"""

# Memoria temporanea della chat e della chiave
chat_history = []
current_api_key = ""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE.replace("{{ api_key }}", current_api_key).replace('{% for msg in history %}{% endfor %}', "")

@app.post("/config")
async def set_config(api_key: str = Form(...)):
    global current_api_key
    current_api_key = api_key
    return HTML_RESPONSE_RENDER()

@app.post("/chat", response_class=HTMLResponse)
async def chat(prompt: str = Form(...)):
    global current_api_key, chat_history
    
    if current_api_key:
        chat_history.append({"role": "user", "content": prompt})
        try:
            client = Groq(api_key=current_api_key)
            messages_payload = [{"role": "system", "content": "Sei E.V., l'assistente IA avanzata che supporta Peter Parker. Sei formale, tecnologica, efficiente e protettiva."}] + chat_history
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_payload,
                temperature=0.7
            )
            reply = completion.choices[0].message.content
            chat_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            chat_history.append({"role": "assistant", "content": f"Errore di sistema: {e}"})

    return HTML_RESPONSE_RENDER()

def HTML_RESPONSE_RENDER():
    history_html = ""
    for msg in chat_history:
        history_html += f'<div class="message {msg["role"]}"><b>{"Tu" if msg["role"] == "user" else "E.V."}:</b> {msg["content"]}</div>'
    
    page = HTML_TEMPLATE.replace("{{ api_key }}", current_api_key)
    # Sostituisce il blocco del loop con l'HTML generato dei messaggi
    start_tag = "{% for msg in history %}"
    end_tag = "{% endfor %}"
    if start_tag in page:
        parts = page.split(start_tag)
        page = parts[0] + history_html + parts[1].split(end_tag)[1]
    return HTMLResponse(content=page)
