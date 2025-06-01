import streamlit as st
import requests
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
        background-color: #d0f0f3;
        align-self: flex-end;
        text-align: right;
        margin-left: auto;
    }
    .bot {
        background-color: #fce6ef;
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

def generar_codigo_java(prompt_usuario):
    url = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono"
    headers = {"Authorization": "Bearerhf_hCmOlkvxErtZsTmCcNSlAtuhQkQQdPzOGg "}  # Reemplaza con tu token válido

    # Verifica disponibilidad del modelo
    estado = requests.get(url, headers=headers)
    if estado.status_code != 200:
        return f"Error {estado.status_code}: El modelo de Hugging Face no está disponible. Intenta más tarde."

    prompt = f"// Java\n// {prompt_usuario}\npublic class "

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.2,
            "top_p": 0.95,
            "do_sample": True,
            "return_full_text": False
        }
    }

    respuesta = requests.post(url, headers=headers, json=payload)

    if respuesta.status_code == 200:
        resultado = respuesta.json()
        try:
            generated = resultado[0]["generated_text"]
            return generated.strip()
        except (KeyError, IndexError):
            return "Lo siento, no pude generar un código válido en este momento."
    else:
        return f"Error {respuesta.status_code}: no se pudo contactar al modelo de Hugging Face."

        }
    }

    respuesta = requests.post(url, headers=headers, json=payload)

    if respuesta.status_code == 200:
        resultado = respuesta.json()
        try:
            generated = resultado[0]["generated_text"]
            return generated.strip()
        except (KeyError, IndexError):
            return "Lo siento, no pude generar un código válido en este momento."
    else:
        return f"Error {respuesta.status_code}: no se pudo contactar al modelo de Hugging Face."

def buscar_respuesta_clara(pregunta):
    if "ejemplo" in pregunta.lower() or "programa" in pregunta.lower():
        codigo = generar_codigo_java(pregunta)
        return f"**Ejemplo de código generado:**\n```java\n{codigo}\n```"

    conceptos_directos = {
        "herencia": "La herencia en programación orientada a objetos permite que una clase herede atributos y métodos de otra clase.",
        "polimorfismo": "El polimorfismo permite que objetos de diferentes clases sean tratados como objetos de una clase común.",
        "encapsulamiento": "El encapsulamiento consiste en ocultar los detalles internos de un objeto y exponer solo lo necesario a través de métodos públicos.",
        "abstracción": "La abstracción permite centrarse en los aspectos esenciales del objeto, ocultando los detalles no relevantes."
    }

    concepto = None
    for clave in conceptos_directos:
        if clave in pregunta.lower():
            concepto = clave
            break

    if concepto:
        respuesta = conceptos_directos[concepto]
        with DDGS() as ddgs:
            resultados = list(ddgs.text(keywords=f"{concepto} programación orientada a objetos", max_results=3))
            for r in resultados:
                url = r.get("href", "")
                if url:
                    return f" {respuesta}\n\nFuente: [{url}]({url})"

    with DDGS() as ddgs:
        resultados = list(ddgs.text(keywords=pregunta, max_results=5))
        for r in resultados:
            url = r.get("href", "")
            texto = r.get("body", "").strip()
            if any(palabra in texto.lower() for palabra in ["una clase", "java", "herencia", "polimorfismo", "interfaz"]):
                if len(texto) > 1000:
                    texto = texto[:1000].rsplit(".", 1)[0] + "."
                return f"{texto}\n\nFuente: [{url}]({url})"
        return "Lo siento, no encontré una respuesta clara en sitios confiables. ¿Puedes reformular tu pregunta?"

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

