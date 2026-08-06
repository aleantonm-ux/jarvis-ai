import os
import streamlit as st
from groq import Groq

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Jarvis - Assistente Personale")
st.write("Il tuo assistente intelligente basato su Groq.")

# Barra laterale per inserire la chiave API
with st.sidebar:
    st.header("🔑 Configurazione")
    api_key_input = st.text_input("Inserisci la tua Groq API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 💡 Come iniziare")
    st.markdown("1. Inserisci la chiave API di Groq qui sopra.")
    st.markdown("2. Inizia a chattare con Jarvis qui a destra!")

# Verifica se la chiave API è stata inserita
if not api_key_input:
    st.warning("⚠️ Per favore, inserisci la tua API Key di Groq nella barra laterale per attivare Jarvis.")
else:
    # Inizializza il client Groq con la chiave inserita
    client = Groq(api_key=api_key_input)

    # Inizializza la cronologia della chat nella memoria di sessione
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Sei Jarvis, un assistente IA avanzato, efficiente, formale ma amichevole, ispirato all'universo di Iron Man."}
        ]

    # Mostra i messaggi precedenti della chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Casella di input per la chat in basso
    if prompt := st.chat_input("Come posso aiutarti, Signore?"):
        # Aggiunge il messaggio dell'utente alla cronologia
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Genera la risposta usando Groq
        with st.chat_message("assistant"):
            with st.spinner("Elaborazione in corso..."):
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
                    st.error(f"Errore durante la comunicazione con l'API: {e}")
