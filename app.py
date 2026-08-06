import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="E.V. // Assistente Personale",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gestione della chat in sessione con istruzioni rigorose: niente finzioni, appartiene a te!
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sei E.V., un'assistente virtuale professionale e avanzata. Sei stata creata e sviluppata interamente dall'utente che ti sta parlando. Non sei un personaggio dei fumetti o dei film, non appartieni a Tony Stark e non devi inventarti storie di fantasia o attività inesistenti. Rispondi in modo diretto, efficiente, utile e orientato al supporto tecnico."}
    ]

# Interfaccia HUD pura a tutto schermo integrata con Streamlit
hud_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>HUD Terminal</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        :root {
            --primary-color: #00ffff;
            --alert-color: #ff3333;
            --bg-transparent: rgba(2, 6, 23, 0.85);
            --border-glow: 0 0 12px rgba(0, 255, 255, 0.4);
        }
        body {
            margin: 0; padding: 0; width: 100vw; height: 100vh;
            background-color: #010409; color: var(--primary-color);
            font-family: 'Share Tech Mono', monospace; overflow: hidden;
            box-sizing: border-box;
        }
        .hud-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            background: radial-gradient(circle, transparent 55%, rgba(0, 0, 0, 0.85) 100%),
                        linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px; z-index: 100;
        }
        .center-viewport {
            position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 200px; height: 200px; pointer-events: none;
            display: flex; justify-content: center; align-items: center;
        }
        .targeting-reticle {
            width: 90px; height: 90px;
            border: 1px dashed rgba(0, 255, 255, 0.3);
            border-radius: 50%; position: relative;
            animation: rotate-reticle 20s linear infinite;
        }
        .targeting-reticle::before {
            content: ''; position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%); width: 6px; height: 6px;
            background-color: var(--primary-color); box-shadow: var(--border-glow);
        }
        @keyframes rotate-reticle {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .hud-panel {
            position: absolute; background: var(--bg-transparent);
            border: 1px solid rgba(0, 255, 255, 0.35); padding: 10px 14px;
            backdrop-filter: blur(3px); box-shadow: var(--border-glow);
            font-size: 0.8rem; letter-spacing: 1px; z-index: 10;
        }
        .top-left { top: 15px; left: 15px; width: 240px; }
        .top-right { top: 15px; right: 15px; width: 200px; }
        .bottom-left {
            bottom: 15px; left: 15px; width: 140px; height: 140px;
            border-radius: 50%; display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            background: radial-gradient(circle, rgba(0,255,255,0.05) 0%, rgba(2,6,23,0.9) 80%);
        }
        .radar-sweep {
            width: 70px; height: 70px; border: 1px solid rgba(0, 255, 255, 0.4);
            border-radius: 50%; position: relative; overflow: hidden;
        }
        .radar-sweep::after {
            content: ''; position: absolute; top: 0; left: 50%;
            width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.4));
            transform-origin: left center; animation: radar-spin 4s linear infinite;
        }
        @keyframes radar-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .stat-bar { width: 100%; background: rgba(255,255,255,0.1); height: 5px; margin-top: 4px; }
        .stat-fill { height: 100%; background: var(--primary-color); width: 45%; }
    </style>
</head>
<body>
    <div class="hud-overlay"></div>
    <div class="center-viewport"><div class="targeting-reticle"></div></div>
    <div class="hud-panel top-left">
        <div style="color: #fff; font-weight: bold;">[SISTEMA E.V.]</div>
        <div>STATUS: ONLINE</div>
        <div>PROPRIETARIO: UTENTE</div>
    </div>
    <div class="hud-panel top-right">
        <div style="color: #fff; font-weight: bold;">[TELEMETRIA]</div>
        <div>CPU LOAD: <span id="cpu">42</span>%</div>
        <div class="stat-bar"><div class="stat-fill"></div></div>
    </div>
    <div class="hud-panel bottom-left">
        <div style="font-size: 0.65rem; color:#fff; margin-bottom: 2px;">[RADAR]</div>
        <div class="radar-sweep"></div>
    </div>
    <script>
        setInterval(() => {
            document.getElementById('cpu').innerText = Math.floor(Math.random() * 25) + 35;
        }, 2000);
    </script>
</body>
</html>
"""

# Mostra lo sfondo HUD grafico
st.components.v1.html(hud_code, height=180, scrolling=False)

# Sidebar per la chiave API
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    api_key_input = st.text_input("Groq API Key:", type="password")

if not api_key_input:
    st.warning("⚠️ Inserisci la tua chiave API di Groq nella barra laterale per attivare il sistema.")
else:
    client = Groq(api_key=api_key_input)

    # Mostra lo storico dei messaggi
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Inserisci comando o query per E.V..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Elaborazione dati in corso..."):
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.messages,
                        temperature=0.7
                    )
                    reply = completion.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Errore di sistema: {e}")
