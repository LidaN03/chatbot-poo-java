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
        background-color: #cfe8fc;
        align-self: flex-end;
        text-align: right;
        margin-left: auto;
    }
    .bot {
        background-color: #ffe6f0;
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
st.subheader("Hazme preguntas sobre programación orientada a objetos en Java, y generaré respuestas confiables y ejemplos de código.")

if "history" not in st.session_state:
    st.session_state.history = []

# Sitios permitidos para búsqueda web
sitios_permitidos = [
    "campusmvp.es",
    "genbeta.com",
    "alianza.bunam.unam.mx",
    "webdesigncusco.com"
]

# Función para buscar en sitios específicos
def buscar_respuesta_web(pregunta):
    with DDGS() as ddgs:
        resultados = list(ddgs.text(keywords=pregunta, max_results=10))
        for r in resultados:
            url = r.get("href", "")
            texto = r.get("body", "").strip()
            if any(sitio in url for sitio in sitios_permitidos):
                if any(palabra in texto.lower() for palabra in ["clase", "herencia", "interfaz", "java", "polimorfismo", "atributos"]):
                    return f"**Respuesta**: {texto[:1000]}...\n\n🌐 Fuente: {url}"
        return "Lo siento, no encontré una respuesta clara en sitios confiables. ¿Puedes reformular tu pregunta?"

# Función local simulada para generar código (puedes conectarlo a GPT si quieres)
def generar_codigo_ejemplo(pregunta):
    if "herencia" in pregunta.lower():
        return """```java
class Animal {
    void hacerSonido() {
        System.out.println("Sonido genérico");
    }
}

class Perro extends Animal {
    void hacerSonido() {
        System.out.println("Guau");
    }
}
```"""
    if "interfaz" in pregunta.lower():
        return """```java
interface Volador {
    void volar();
}

class Pajaro implements Volador {
    public void volar() {
        System.out.println("El pájaro vuela");
    }
}
```"""
    return None

user_input = st.text_input("Escribe tu mensaje:", "")

if st.button("Enviar") and user_input:
    st.session_state.history.append(("user", user_input))

    # Ver si se trata de una solicitud de ejemplo de código
    codigo = generar_codigo_ejemplo(user_input)
    if codigo:
        respuesta = f"**Aquí tienes un ejemplo en Java:**\n\n{codigo}"
    else:
        # Buscar solo en sitios confiables
        with st.spinner("Buscando la mejor respuesta en sitios confiables..."):
            time.sleep(1)
            respuesta = buscar_respuesta_web(user_input)

    st.session_state.history.append(("bot", respuesta))

# Mostrar historial de chat
for autor, mensaje in st.session_state.history:
    clase = "user" if autor == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {clase}">{mensaje}</div>', unsafe_allow_html=True)

