import streamlit as st
import requests

st.set_page_config(page_title="ChatBot POO", layout="centered")
st.markdown("""
    <style>
    body, .stApp {
        font-family: 'Arial Rounded MT Bold', sans-serif;
        background-color: #f1f1f1;
    }
    .chat-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }
    .user-msg {
        background-color: #d0e8ff;
        padding: 8px;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .bot-msg {
        background-color: #eeeeee;
        padding: 8px;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.image("robot_chatbot.png", width=100)
st.title("🤖 ChatBot de POO y más")

# Historial de mensajes si no existe
def iniciar_historial():
    if "historial" not in st.session_state:
        st.session_state.historial = []

def buscar_duckduckgo(pregunta):
    try:
        url = f"https://api.duckduckgo.com/?q={pregunta}&format=json&no_redirect=1"
        respuesta = requests.get(url)
        datos = respuesta.json()
        texto = datos.get("Abstract")
        if texto:
            return texto
        else:
            return "No encontré una respuesta directa, intenta reformular tu pregunta."
    except Exception as e:
        return f"Ocurrió un error al buscar: {e}"

# Lógica general del chatbot
def responder(pregunta):
    pregunta = pregunta.lower()
    respuesta = buscar_duckduckgo(pregunta)
    return respuesta

# Inicia historial
iniciar_historial()

# Mostrar historial
st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for i, (usuario, bot) in enumerate(st.session_state.historial):
    st.markdown(f'<div class="user-msg">👤 Tú: {usuario}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">🤖 Bot: {bot}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Campo de entrada
pregunta = st.text_input("Escribe tu pregunta sobre POO o cualquier tema:")
if st.button("Enviar") and pregunta:
    respuesta = responder(pregunta)
    st.session_state.historial.append((pregunta, respuesta))
    st.experimental_rerun()

