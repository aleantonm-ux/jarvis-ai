import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="ARIA // Assistente Personale",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gestione della chat in sessione con identità corretta
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sei ARIA, un'assistente virtuale professionale e avanzata. Sei stata creata e sviluppata interamente dall'utente che ti sta parlando. Non sei un personaggio dei fumetti o dei film, non appartieni a Tony Stark e non devi inventarti storie di fantasia o attività inesistenti. Rispondi in modo diretto, efficiente, utile e orientato al supporto tecnico."}
    ]

# Interfaccia grafica HUD identica a quella del video, pulita e a tutto schermo
hud_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>ARIA HUD</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        :root {
            --accent-color: #ffb700;
            --bg-dark: #05070a;
            --panel-bg: rgba(8, 12, 20, 0.9);
            --border-glow: 0 0 10px rgba(255, 183, 0, 0.3);
        }
        body {
            margin: 0; padding: 0; width: 100vw; height: 100vh;
            background-color: var(--bg-dark); color: var(--accent-color);
            font-family: 'Share Tech Mono', monospace; overflow: hidden;
            box-sizing: border-box;
            background-image: linear-gradient(rgba(255,183,0,0.03) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(255,183,0,0.03) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        .top-bar {
            position: absolute; top: 15px; left: 20px; right: 20px;
            display: flex; justify-content: space-between; align-items: center;
            font-size: 0.85rem; letter-spacing: 2px; border-bottom: 1px solid rgba(255,183,0,0.2);
            padding-bottom: 8px; z-index: 10;
        }
        .center-core {
            position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 180px; height: 180px;
            display: flex; justify-content: center; align-items: center;
            pointer-events: none;
        }
        .ring {
            position: absolute; border-radius: 50%;
            border: 1px dashed rgba(255, 183, 0, 0.4);
            animation: spin 25s linear infinite;
        }
        .ring-1 { width: 160px; height: 160px; border-color: rgba(255, 183, 0, 0.6); }
        .ring-2 { width: 120px; height: 120px; animation-direction: reverse; animation-duration: 15s; }
        .core-center {
            width: 40px; height: 40px; background: radial-gradient(circle, var(--accent-color) 0%, #1a1200 80%);
            border-radius: 50%; box-shadow: 0 0 15px var(--accent-color);
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .hud-panel {
            position: absolute; background: var(--panel-bg);
            border: 1px solid rgba(255, 183, 0, 0.35); padding: 10px 14px;
            box-shadow: var(--border-glow); font-size: 0.75rem; width: 220px;
        }
        .left-panel { top: 70px; left: 20px; }
        .right-panel { top: 70px; right: 20px; }
        .stat-bar { width: 100%; background: rgba(255,255,255,0.1); height: 4px; margin-top: 4px; }
        .stat-fill { height: 100%; background: var(--accent-color); width: 65%; }
    </style>
</head>
<body>
    <div class="top-bar">
        <div>[ARIA v2.0]</div>
        <div style="font-weight: bold; color: #fff;">// SISTEMA ONLINE</div>
        <div>15:59:00</div>
    </div>
    
    <div class="center-core">
        <div class="ring ring-1"></div>
        <div class="ring ring-2"></div>
        <div class="core-center"></div>
    </div>

    <div class="hud-panel left-panel">
        <div style="color: #fff; margin-bottom: 5px; font-weight: bold;">[DIAGNOSTICA]</div>
        <div>CARICO NEURALE: 60%</div>
        <div class="stat-bar"><div class="stat-fill" style="width: 60%;"></div></div>
        <div style="margin-top: 6px;">INTEGRITÀ RETE: 94%</div>
    </div>

    <div class="hud-panel right-panel">
        <div style="color: #fff; margin-bottom: 5px; font-weight: bold;">[AMBIENTE]</div>
        <div>LATENZA RISPOSTA: 12ms</div>
        <div style="margin-top: 6px;">SICUREZZA CANALE: 98%</div>
    </div>
</body>
</html>
"""

# Mostra la grafica HUD con l'altezza corretta
st.components.v1.html(hud_code, height=280, scrolling=False)

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

    if prompt := st.chat_input("Scrivi un comando..."):
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
