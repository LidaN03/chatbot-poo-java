import streamlit as st
from duckduckgo_search import DDGS
import time

st.set_page_config(page_title="ChatBot POO", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #fff0f5;
    }
    .main {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .chat-bubble {
        border-radius: 15px;
        padding: 10px 20px;
        margin: 10px 0;
        max-width: 80%;
        font-size: 16px;
        color: #333;
    }
    .user {
        background-color: #d0f0fd;
        align-self: flex-end;
        text-align: right;
        margin-left: auto;
    }
    .bot {
        background-color: #ffe6f2;
        align-self: flex-start;
        text-align: left;
        margin-right: auto;
    }
    .stButton>button {
        background-color: #ffb6c1;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stTextInput>div>input {
        border-radius: 10px;
        border: 1px solid #ffc0cb;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.image("robot_chatbot.png", width=100)

st.title("💬 Chatbot POO para estudiantes de Java")
st.subheader("Pregúntame sobre clases, herencia, ejemplos de código en Java y más. ¡Estoy aquí para ayudarte!")

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

