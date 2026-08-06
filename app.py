import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="J.A.R.V.I.S. // Stark Industries",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS per pulire completamente l'interfaccia e darle un look olografico totale
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: radial-gradient(circle at center, #050b18 0%, #010306 100%);
        color: #00d2ff;
        font-family: 'Orbitron', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #ff3b30 !important;
        letter-spacing: 2px;
        text-shadow: 0 0 12px rgba(255, 59, 48, 0.7);
    }

    /* Stile dei messaggi */
    .stChatMessage {
        background-color: rgba(3, 8, 18, 0.8) !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 6px;
    }

    /* Casella di input personalizzata stile Stark */
    .stTextInput input {
        background-color: rgba(2, 5, 12, 0.9) !important;
        color: #00d2ff !important;
        border: 1px solid rgba(0, 210, 255, 0.5) !important;
        border-radius: 6px !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
    }

    section[data-testid="stSidebar"] {
        background-color: #020408;
        border-right: 1px solid rgba(255, 59, 48, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione superiore in stile HUD
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.markdown("### 📊 TELEMETRIA")
    st.markdown("- **Reattore:** 99.8%")
    st.markdown("- **Core Temp:** 38.2°C")

with col2:
    st.markdown("<h1 style='text-align: center;'>⚡ J.A.R.V.I.S. // STARK HUD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00d2ff; font-size: 0.75rem;'>SISTEMA OPERATIVO DI SUPPORTO TATTICO</p>", unsafe_allow_html=True)

with col3:
    st.markdown("### ⚙️ PROTOCOLLI")
    st.markdown("- **Stato IA:** Online")
    st.markdown("- **Sicurezza:** Massima")

st.markdown("---")

with st.sidebar:
    st.header("🔑 ACCESSO SICURO")
    api_key_input = st.text_input("Groq API Key:", type="password")

if not api_key_input:
    st.warning("⚠️ **ATTENZIONE:** Inserisci la tua chiave API di Groq nella barra laterale (clicca sulla freccetta `>` in alto a sinistra) per avviare J.A.R.V.I.S.")
else:
    client = Groq(api_key=api_key_input)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei J.A.R.V.I.S., l'intelligenza artificiale avanzata creata da Tony Stark. Sei estremamente educato, ironico, efficiente, protettivo e parli con un tono formale ma brillante."}
        ]

    # Mostra i messaggi precedenti
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Spostiamo l'input in un form centrale pulito usando st.text_input al posto del componente fisso in basso
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            prompt = st.text_input("Impartisci un ordine a J.A.R.V.I.S...", label_visibility="collapsed", placeholder="Impartisci un ordine a J.A.R.V.I.S...")
        with col_btn:
            submit_button = st.form_submit_button(label="INVIA")

    if submit_button and prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Analisi dati in corso..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                response = chat_completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                st.error(f"Errore critico nei sistemi di bordo: {e}")
