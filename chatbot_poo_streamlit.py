import streamlit as st
from duckduckgo_search import DDGS
import time

st.set_page_config(page_title="ChatBot POO", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #f7f2fa;
    }
    .main {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-bubble {
        border-radius: 15px;
        padding: 10px 20px;
        margin: 10px 0;
        max-width: 80%;
        font-size: 16px;
    }
    .user {
        background-color: #d3cce3;
        align-self: flex-end;
        text-align: right;
        margin-left: auto;
    }
    .bot {
        background-color: #cfe2f3;
        align-self: flex-start;
        text-align: left;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Asistente de POO con Java")
st.subheader("Hazme preguntas sobre programación orientada a objetos, clases, herencia, ejemplos en Java y más.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Escribe tu mensaje:", "")

if st.button("Enviar") and user_input:
    st.session_state.history.append(("user", user_input))
    
    # Simular búsqueda inteligente
    respuesta = "Estoy buscando la mejor respuesta..."
    with st.spinner("Pensando..."):
        time.sleep(1.5)
        try:
            with DDGS() as ddgs:
                resultados = list(ddgs.text(keywords=user_input, max_results=1))
                if resultados:
                    respuesta = resultados[0]["body"]
                else:
                    respuesta = "Lo siento, no encontré una respuesta clara. ¿Puedes reformular tu pregunta?"
        except Exception as e:
            respuesta = f"Ocurrió un error al buscar información: {str(e)}"

    st.session_state.history.append(("bot", respuesta))

# Mostrar historial de chat
for autor, mensaje in st.session_state.history:
    clase = "user" if autor == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {clase}">{mensaje}</div>', unsafe_allow_html=True)

