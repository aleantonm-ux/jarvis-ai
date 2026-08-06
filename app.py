import os
import streamlit as st
from groq import Groq

# Configurazione pagina
st.set_page_config(
    page_title="E.V. // Interfaccia Neurale",
    page_icon="🕸️",
    layout="centered"
)

# Grafica personalizzata HUD / Terminale
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #030712 0%, #0f172a 100%);
        color: #f8fafc;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
    .stChatInputContainer input {
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 4px;
    }
    section[data-testid="stSidebar"] {
        background-color: #050811;
        border-right: 1px solid #1e293b;
    }
    .stChatMessage {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione visiva
st.title("🕸️ E.V. // PROTOCOLLO NEURALE")
st.caption("Sistema di supporto tattico e analisi dati - Connessione attiva.")

# Barra laterale
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    api_key_input = st.text_input("Inserisci Groq API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 📊 STATO SISTEMA")
    st.markdown("- **IA:** E.V. (Online)")
    st.markdown("- **Crittografia:** Attiva")
    st.markdown("- **Modello:** Llama 3.3")

# Controllo chiave API e logica chat
if not api_key_input:
    st.warning("⚠️ **ATTENZIONE:** Inserisci la tua chiave API di Groq nella barra laterale per stabilire il collegamento con E.V.")
else:
    client = Groq(api_key=api_key_input)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei E.V., l'assistente IA avanzata che supporta Peter Parker nel suo rifugio e nelle sue missioni. Sei efficiente, protettiva, tecnologica e parli con un tono formale ma diretto."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Inserisci comando o domanda per E.V..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Elaborazione dati in corso..."):
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
                    st.error(f"Errore critico di sistema: {e}")
