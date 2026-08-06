import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="E.V. // HUD Interface",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inizializza la cronologia della chat nella sessione se non esiste
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sei E.V., l'assistente IA avanzata che supporta Peter Parker. Parla in modo efficiente, tecnologico, formale ma diretto, tipico di una FUI di supporto tattico."}
    ]

# Gestione della chiave API nella sidebar (nascosta ma accessibile)
with st.sidebar:
    st.markdown("### ⚙️ CONFIGURAZIONE")
    api_key_input = st.text_input("Inserisci Groq API Key:", type="password")

# Intercetta se l'utente ha inviato un messaggio tramite query string o parametri
# Per farlo in modo pulito in Streamlit, usiamo un input nativo nascosto o gestito tramite form, 
# oppure rendiamo l'input HTML in grado di interagire con Streamlit.
# Sfruttiamo un approccio pulito: inserimento tramite input Streamlit sotto l'HUD o gestito via session_state.

# Per mantenere l'HUD pulito e visibile a tutto schermo, creiamo una chat nativa di Streamlit integrata nello stile HUD
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    .stApp {
        background-color: #010409;
        color: #00ffff;
        font-family: 'Share Tech Mono', monospace;
    }
    .stChatMessage {
        background-color: rgba(2, 6, 23, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        color: #00ffff !important;
    }
    .stChatInputContainer input {
        background-color: #020617 !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕸️ E.V. // PROTOCOLLO NEURALE")

if not api_key_input:
    st.warning("⚠️ Inserisci la tua chiave API di Groq nella barra laterale (clicca sulla freccetta `>` in alto a sinistra) per attivare i protocolli.")
else:
    client = Groq(api_key=api_key_input)

    # Mostra i messaggi della chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input della chat
    if prompt := st.chat_input("Inserisci comando o query per E.V..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Decrittazione ed elaborazione in corso..."):
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
