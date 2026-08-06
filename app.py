import os
import streamlit as st
from groq import Groq

# Configurazione della pagina in stile high-tech
st.set_page_config(
    page_title="E.V. // Spider-Man Interface",
    page_icon="🕸️",
    layout="centered"
)

# Iniezione di CSS personalizzato per dare un look futuristico e scuro (stile HUD)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .stChatInputContainer {
        border-color: #1e3a8a !important;
    }
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
        color: #38bdf8 !important;
    }
    .stAlert {
        background-color: #1e1b4b;
        color: #e0f2fe;
        border: 1px solid #3b82f6;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione in stile interfaccia IA di Peter Parker
st.title("🕸️ E.V. // PROTOCOLLO DI ASSISTENZA")
st.caption("Interfaccia Neurale v4.2 - Connessione stabilita con il rifugio.")

# Barra laterale per inserire la chiave API e impostazioni di sistema
with st.sidebar:
    st.header("⚙️ CONFIGURAZIONE")
    api_key_input = st.text_input("Inserisci Groq API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 📊 STATO DEL SISTEMA")
    st.markdown("- **IA:** Attiva (E.V.)")
    st.markdown("- **Rete:** Sicura / Crittografata")
    st.markdown("- **Modello:** Llama 3.3 Versatile")
    st.markdown("---")
    st.markdown("💡 *Consiglio: Mantieni la calma e analizza le minacce.*")

# Verifica se la chiave API è stata inserita
if not api_key_input:
    st.warning("⚠️ **ATTENZIONE:** Inserisci la tua chiave API di Groq nella barra laterale per avviare il protocollo di comunicazione con l'IA.")
else:
    # Inizializza il client Groq
    client = Groq(api_key=api_key_input)

    # Inizializza la cronologia della chat nella memoria di sessione
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei E.V., l'assistente di intelligenza artificiale avanzata che supporta Peter Parker nel suo rifugio e nei suoi equipaggiamenti. Sei efficiente, protettiva, tecnologica e parli in modo diretto ma amichevole."}
        ]

    # Mostra i messaggi precedenti della chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Casella di input per la chat in basso
    if prompt := st.chat_input("Inserisci comando o domanda per E.V..."):
        # Aggiunge il messaggio dell'utente alla cronologia
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Genera la risposta usando Groq
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
                    # Aggiunge la risposta dell'assistente alla cronologia
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Errore di sistema critico: {e}")
