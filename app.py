import os
import streamlit as st
from groq import Groq

# Configurazione pagina in stile Stark Tech
st.set_page_config(
    page_title="J.A.R.V.I.S. // Stark Industries",
    page_icon="⚡",
    layout="wide"
)

# Iniezione CSS avanzato: tema rosso/oro/blu stile HUD di Iron Man
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #0a0f1d 0%, #020408 100%);
        color: #00d2ff;
        font-family: 'Orbitron', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        color: #ff3b30 !important;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(255, 59, 48, 0.5);
    }

    /* Stile della chat in stile olografico */
    .stChatMessage {
        background-color: rgba(10, 15, 29, 0.9) !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 4px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
    }

    /* Barra laterale tecnologica */
    section[data-testid="stSidebar"] {
        background-color: #050811;
        border-right: 1px solid rgba(255, 59, 48, 0.3);
    }

    /* Casella di input stile terminale Stark */
    .stChatInputContainer input {
        background-color: #050811 !important;
        color: #00d2ff !important;
        border: 1px solid #ff3b30 !important;
        border-radius: 4px;
        font-family: 'Orbitron', sans-serif !important;
    }

    .stAlert {
        background-color: rgba(255, 59, 48, 0.1);
        border: 1px solid #ff3b30;
        color: #ff3b30;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione in stile olografico di Stark Industries
st.title("⚡ J.A.R.V.I.S. // STARK INDUSTRIES HUD")
st.caption("SISTEMA OPERATIVO DI SUPPORTO TATTICO AVANZATO - v9.4")

# Barra laterale per configurazione e telemetria
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    api_key_input = st.text_input("Inserisci Groq API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 📊 STATO REATTORE")
    st.markdown("- **Stato IA:** Online")
    st.markdown("- **Integrità Corazza:** 100%")
    st.markdown("- **Protocollo:** Casa Sicura")
    st.markdown("---")
    st.markdown("💡 *'A volte bisogna correre prima di imparare a camminare.'*")

# Controllo chiave API e logica chat
if not api_key_input:
    st.warning("⚠️ **ATTENZIONE:** Inserisci la tua chiave API di Groq nella barra laterale per avviare i protocolli di J.A.R.V.I.S.")
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
                    st.error(f"Errore critico nei sistemi di bordo: {e}")
