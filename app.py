import os
import streamlit as st
from groq import Groq

# Configurazione della pagina
st.set_page_config(
    page_title="E.V. // Protocollo Neurale",
    page_icon="🕸️",
    layout="wide"
)

# CSS avanzato per un look high-tech / HUD cinematografico
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    .stApp {
        background-color: #020617;
        color: #38bdf8;
        font-family: 'Share Tech Mono', monospace;
    }

    h1, h2, h3, h4, span, p, label {
        font-family: 'Share Tech Mono', monospace !important;
        color: #38bdf8 !important;
    }

    h1 {
        font-size: 2.2rem !important;
        letter-spacing: 3px;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
        border-bottom: 1px solid rgba(56, 189, 248, 0.3);
        padding-bottom: 10px;
    }

    /* Stile della barra laterale */
    section[data-testid="stSidebar"] {
        background-color: #050b14;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }

    /* Campi di input */
    .stTextInput input, .stChatInputContainer input {
        background-color: #090d16 !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 2px;
        font-family: 'Share Tech Mono', monospace !important;
        box-shadow: inset 0 0 10px rgba(56, 189, 248, 0.1);
    }

    /* Messaggi della chat */
    .stChatMessage {
        background-color: #0a1120 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 4px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.05);
    }

    /* Pulsanti di avviso / box */
    .stAlert {
        background-color: #090d16 !important;
        border: 1px solid #f43f5e !important;
        color: #f43f5e !important;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione principale
st.title("🕸️ E.V. // INTERFACCIA NEURALE TATTICA")
st.caption("SISTEMA OPERATIVO DI SUPPORTO REMOTO - LIVELLO DI ACCESSO: 4")

# Barra laterale
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    api_key_input = st.text_input("Inserisci Groq API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 📊 STATO SISTEMA")
    st.markdown("- **IA:** E.V. [ONLINE]")
    st.markdown("- **Rete:** Criptata (AES-256)")
    st.markdown("- **Modello:** Llama 3.3 Versatile")
    st.markdown("---")
    st.markdown("💡 *Ricorda: Analizza sempre i dati prima di agire.*")

# Gestione della chat
if not api_key_input:
    st.warning("⚠️ ATTENZIONE: Inserisci la chiave API di Groq nella barra laterale per sbloccare i protocolli di comunicazione.")
else:
    client = Groq(api_key=api_key_input)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei E.V., l'assistente IA avanzata che supporta Peter Parker nel suo rifugio. Sei efficiente, protettiva, tecnologica e parli con un tono formale ma diretto."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Inserisci comando o query per E.V..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Decrittazione ed elaborazione in corso..."):
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
