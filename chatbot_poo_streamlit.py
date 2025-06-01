import streamlit as st
import openai

# Configura la clave de la API de OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Título y diseño
st.set_page_config(page_title="Chatbot POO Java", layout="centered")
st.image("https://raw.githubusercontent.com/LidaN03/chatbot-poo-java/main/robot_chatbot.png", width=100)
st.markdown("<h2 style='text-align: center;'>🤖 Chatbot POO para estudiantes de Java</h2>", unsafe_allow_html=True)
st.markdown("---")

# Estado del chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Entrada de usuario
user_input = st.text_input("Tú:")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    # Consulta a OpenAI
    with st.spinner("Pensando..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Responde como un profesor experto en Java POO. Explica de forma clara y breve. Incluye ejemplos en código si se solicita."},
                    *st.session_state.chat
                ]
            )
            reply = response.choices[0].message.content
            st.session_state.chat.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error al contactar OpenAI: {e}")
            reply = "Lo siento, ocurrió un error."

# Mostrar el historial del chat
for i, mensaje in enumerate(st.session_state.chat):
    if mensaje["role"] == "user":
        st.markdown(f"**🧑 Tú:** {mensaje['content']}")
    else:
        st.markdown(f"**🤖 Chatbot:** {mensaje['content']}")

