import streamlit as st
from duckduckgo_search import DDGS
import time

st.set_page_config(page_title="ChatBot POO", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #fef6f9;
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
        color: #333;
    }
    .user {
        background-color: #e0f7fa;
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
        background-color: #ff8fab;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stTextInput>div>input {
        border-radius: 10px;
        border: 1px solid #ffb6c1;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.image("robot_chatbot.png", width=120)

st.title("Chatbot POO para estudiantes de Java")
st.subheader("Pregúntame sobre clases, herencia, ejemplos de código en Java y más. ¡Estoy aquí para ayudarte!")

if "history" not in st.session_state:
    st.session_state.history = []

def buscar_respuesta_clara(pregunta):
    with DDGS() as ddgs:
        resultados = list(ddgs.text(keywords=pregunta, max_results=5))
        for r in resultados:
            texto = r["body"].strip()
            if any(palabra in texto.lower() for palabra in ["una clase", "java", "herencia", "polimorfismo", "interfaz"]):
                if len(texto) > 400:
                    texto = texto[:400] + "..."
                return f"**Respuesta**: {texto}"
        return "Lo siento, no encontré una respuesta clara. ¿Puedes reformular tu pregunta?"

user_input = st.text_input("Escribe tu mensaje:", "")

if st.button("Enviar") and user_input:
    st.session_state.history.append(("user", user_input))

    with st.spinner("Buscando la mejor respuesta en la web..."):
        time.sleep(1)
        respuesta = buscar_respuesta_clara(user_input)

    st.session_state.history.append(("bot", respuesta))

# Mostrar historial de chat
for autor, mensaje in st.session_state.history:
    clase = "user" if autor == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {clase}">{mensaje}</div>', unsafe_allow_html=True)

