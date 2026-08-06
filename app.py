import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="E.V. // HUD Interface",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Codice HTML/CSS/JS dell'interfaccia HUD in stile Spider-Man / Stark Tech
hud_html = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E.V. // HUD</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        :root {
            --primary-color: #00ffff;
            --alert-color: #ff3333;
            --bg-transparent: rgba(2, 6, 23, 0.75);
            --border-glow: 0 0 10px rgba(0, 255, 255, 0.4);
        }

        body {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            background-color: #010409;
            color: var(--primary-color);
            font-family: 'Share Tech Mono', monospace;
            overflow: hidden;
            box-sizing: border-box;
        }

        .hud-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            background: radial-gradient(circle, transparent 60%, rgba(0, 0, 0, 0.85) 100%),
                        linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
            z-index: 100;
        }

        .center-viewport {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 300px; height: 300px;
            pointer-events: none;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .targeting-reticle {
            width: 100px; height: 100px;
            border: 1px dashed rgba(0, 255, 255, 0.3);
            border-radius: 50%;
            position: relative;
            animation: rotate-reticle 20s linear infinite;
        }
        .targeting-reticle::before {
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 6px; height: 6px;
            background-color: var(--primary-color);
            box-shadow: var(--border-glow);
        }
        @keyframes rotate-reticle {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .hud-panel {
            position: absolute;
            background: var(--bg-transparent);
            border: 1px solid rgba(0, 255, 255, 0.3);
            padding: 12px 16px;
            backdrop-filter: blur(3px);
            box-shadow: var(--border-glow);
            font-size: 0.85rem;
            letter-spacing: 1px;
            z-index: 10;
        }

        .top-left { top: 20px; left: 20px; width: 260px; }
        .top-right { top: 20px; right: 20px; width: 220px; }
        
        .bottom-left {
            bottom: 20px; left: 20px;
            width: 160px; height: 160px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle, rgba(0,255,255,0.05) 0%, rgba(2,6,23,0.85) 80%);
        }
        .radar-sweep {
            width: 90px; height: 90px;
            border: 1px solid rgba(0, 255, 255, 0.4);
            border-radius: 50%;
            position: relative;
            overflow: hidden;
        }
        .radar-sweep::after {
            content: '';
            position: absolute;
            top: 0; left: 50%;
            width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3));
            transform-origin: left center;
            animation: radar-spin 4s linear infinite;
        }
        @keyframes radar-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .bottom-right {
            bottom: 20px; right: 20px;
            width: 360px; height: 220px;
            display: flex;
            flex-direction: column;
        }
        .chat-log {
            flex: 1;
            overflow-y: auto;
            font-size: 0.8rem;
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding-right: 5px;
        }
        .chat-msg.user { color: #a5f3fc; }
        .chat-msg.ai { color: var(--primary-color); }

        .bottom-input-bar {
            position: absolute;
            bottom: 20px; left: 50%;
            transform: translateX(-50%);
            width: 420px;
            background: var(--bg-transparent);
            border: 1px solid rgba(0, 255, 255, 0.4);
            padding: 8px 12px;
            display: flex;
            gap: 8px;
            z-index: 20;
            box-shadow: var(--border-glow);
        }
        .bottom-input-bar input {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--primary-color);
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.9rem;
            outline: none;
        }
        .bottom-input-bar button {
            background: rgba(0, 255, 255, 0.2);
            border: 1px solid var(--primary-color);
            color: var(--primary-color);
            padding: 4px 12px;
            cursor: pointer;
            font-family: 'Share Tech Mono', monospace;
        }
        .bottom-input-bar button:hover {
            background: var(--primary-color);
            color: #010409;
        }

        .stat-bar-container {
            width: 100%;
            background: rgba(255,255,255,0.1);
            height: 6px;
            margin-top: 4px;
        }
        .stat-bar-fill {
            height: 100%;
            background: var(--primary-color);
            width: 42%;
            box-shadow: var(--border-glow);
        }
    </style>
</head>
<body>

    <div class="hud-overlay"></div>

    <div class="center-viewport">
        <div class="targeting-reticle"></div>
    </div>

    <div class="hud-panel top-left">
        <div style="color: #fff; font-weight: bold; margin-bottom: 4px;">[SISTEMA E.V.]</div>
        <div>STATUS: <span style="color:#00ffff;">ONLINE</span></div>
        <div>SEC-LEVEL: 4</div>
    </div>

    <div class="hud-panel top-right">
        <div style="color: #fff; font-weight: bold; margin-bottom: 4px;">[TELEMETRIA]</div>
        <div>CPU LOAD: <span id="cpuLoad">42</span>%</div>
        <div class="stat-bar-container"><div class="stat-bar-fill"></div></div>
        <div style="margin-top: 4px;">MODEL: LLAMA-3.3</div>
    </div>

    <div class="hud-panel bottom-left">
        <div style="font-size: 0.7rem; margin-bottom: 4px; color:#fff;">[RADAR TATTICO]</div>
        <div class="radar-sweep"></div>
    </div>

    <div class="hud-panel bottom-right">
        <div style="color: #fff; font-weight: bold; margin-bottom: 4px;">[CANALE COMUNICAZIONE]</div>
        <div class="chat-log" id="chatLog">
            <div class="chat-msg ai">> E.V. inizializzata. Inserisci comando o query.</div>
        </div>
    </div>

    <div class="bottom-input-bar">
        <input type="text" id="userInput" placeholder="Inserisci comando..." autocomplete="off">
        <button onclick="triggerMessage()">INVIA</button>
    </div>

    <script>
        setInterval(() => {
            document.getElementById('cpuLoad').innerText = Math.floor(Math.random() * 25) + 35;
        }, 2500);

        function triggerMessage() {
            const input = document.getElementById('userInput');
            const log = document.getElementById('chatLog');
            if(!input.value.trim()) return;

            const text = input.value;
            log.innerHTML += `<div class="chat-msg user">> Tu: ${text}</div>`;
            input.value = '';
            log.scrollTop = log.scrollHeight;

            // Invia evento al parent di Streamlit
            window.parent.postMessage({ type: 'streamlit_chat', text: text }, '*');
        }

        window.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'ai_response') {
                const log = document.getElementById('chatLog');
                log.innerHTML += `<div class="chat-msg ai">> E.V.: ${event.data.text}</div>`;
                log.scrollTop = log.scrollHeight;
            }
        });

        document.getElementById('userInput').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') triggerMessage();
        });
    </script>
</body>
</html>
"""

# Gestione chiave API tramite sidebar di Streamlit nativa
with st.sidebar:
    st.markdown("### ⚙️ CONFIGURAZIONE")
    api_key_input = st.text_input("Inserisci Groq API Key:", type="password")

# Se non c'è la chiave API
if not api_key_input:
    st.warning("⚠️ Inserisci la tua chiave API di Groq nella barra laterale (clicca sulla freccetta `>` in alto a sinistra) per attivare E.V.")
else:
    client = Groq(api_key=api_key_input)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei E.V., l'assistente IA avanzata che supporta Peter Parker. Parla in modo efficiente, tecnologico, formale ma diretto, tipico di una FUI di supporto tattico."}
        ]

# Mostra l'interfaccia HUD a tutto schermo
st.components.v1.html(hud_html, height=750, scrolling=False)
