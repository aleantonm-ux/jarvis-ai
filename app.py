import os
import streamlit as st
from groq import Groq

# Configurazione pagina a tutto schermo
st.set_page_config(
    page_title="J.A.R.V.I.S. // Stark Industries",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS avanzato per trasformare completamente l'app in un HUD di Iron Man
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* Nascondi intestazioni e menu standard di Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: radial-gradient(circle at center, #070b14 0%, #010307 100%);
        color: #00d2ff;
        font-family: 'Orbitron', sans-serif;
        overflow: hidden;
    }

    /* Effetto griglia olografica di sfondo */
    .stApp::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 255, 0.03));
        z-index: 999;
        background-size: 100% 4px, 6px 100%;
        pointer-events: none;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #ff3b30 !important;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(255, 59, 48, 0.6);
    }

    /* Stile della chat box */
    .stChatMessage {
        background-color: rgba(5, 10, 20, 0.85) !important;
        border: 1px solid rgba(0, 210, 255, 0.4) !important;
        border-radius: 4px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
    }

    /* Input di chat */
    .stChatInputContainer input {
        background-color: #03060c !important;
        color: #00d2ff !important;
        border: 1px solid #ff3b30 !important;
        border-radius: 4px;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Sidebar personalizzata */
    section[data-testid="stSidebar"] {
        background-color: #020408;
        border-right: 1px solid rgba(255, 59, 48, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Layout principale stile Stark Industries
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.markdown("### 📊 TELEMETRIA")
    st.markdown("- **Reattore:** 99.8%")
    st.markdown("- **Core Temp:** 38.2°C")
    st.markdown("- **Corazza:** Mark LXXXV")

with col2:
    st.markdown("<h1 style='text-align: center;'>⚡ J.A.R.V.I.S. // STARK HUD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00d2ff; font-size: 0.8rem;'>SISTEMA OPERATIVO DI SUPPORTO TATTICO</p>", unsafe_allow_html=True)

with col3:
    st.markdown("### ⚙️ PROTOCOLLI")
    st.markdown("- **Stato IA:** Online")
    st.markdown("- **Sicurezza:** Massima")

st.markdown("---")

# Barra laterale nascosta per la chiave API
with st.sidebar:
    st.header("🔑 ACCESSO SICURO")
    api_key_input = st.text_input("Groq API Key:", type="password")
    st.markdown("---")
    st.markdown("💡 *'A volte bisogna correre prima di imparare a camminare.'*")

# Logica della chat protetta dalla chiave API
if not api_key_input:
    st.warning("⚠️ **ATTENZIONE:** Inserisci la tua chiave API di Groq nella barra laterale (clicca sulla freccetta `>` in alto a sinistra) per avviare i protocolli di J.A.R.V.I.S.")
else:
    client = Groq(api_key=api_key_input)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei J.A.R.V.I.S., l'intelligenza artificiale avanzata creata da Tony Stark. Sei estremamente educato, ironico, efficiente, protettivo e parli con un tono formale ma brillante."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Impartisci un ordine a J.A.R.V.I.S..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analisi dati in corso..."):
                try:
                    chat_completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.messages,
                        temperature=0.7,
                    )
                    response = chat_completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Errore critico nei sistemi di bordo: {e}")
