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

# Ejemplos predefinidos de código Java
codigos_java = {
    "herencia": """java
class Animal {
    void hacerSonido() {
        System.out.println("Sonido genérico");
    }
}

class Perro extends Animal {
    void hacerSonido() {
        System.out.println("Guau!");
    }
}
""",
    "interfaz": """java
interface Vehiculo {
    void conducir();
}

class Coche implements Vehiculo {
    public void conducir() {
        System.out.println("El coche está en marcha.");
    }
}
""",
    "clase abstracta": """java
abstract class Figura {
    abstract void dibujar();
}

class Circulo extends Figura {
    void dibujar() {
        System.out.println("Dibujando un círculo");
    }
}
""",
    "sobrecarga": """java
class Calculadora {
    int sumar(int a, int b) {
        return a + b;
    }

    double sumar(double a, double b) {
        return a + b;
    }
}
""",
    "main": """java
public class Principal {
    public static void main(String[] args) {
        System.out.println("Hola Mundo");
    }
}
"""
}

def generar_codigo_java_local(pregunta):
    for clave in codigos_java:
        if clave in pregunta.lower():
            return codigos_java[clave]
    return None

def buscar_respuesta_clara(pregunta):
    if "ejemplo" in pregunta.lower() or "programa" in pregunta.lower():
        codigo = generar_codigo_java_local(pregunta)
        if codigo:
            return f"*Ejemplo de código generado:*\n{codigo}"
        else:
            return "Lo siento, no tengo un ejemplo para eso aún. Prueba con 'herencia' o 'interfaz'."

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
                    return f"*Respuesta*: {respuesta}\n\nFuente: [{url}]({url})"

    with DDGS() as ddgs:
        resultados = list(ddgs.text(keywords=pregunta, max_results=5))
        for r in resultados:
            url = r.get("href", "")
            texto = r.get("body", "").strip()
            if any(palabra in texto.lower() for palabra in ["una clase", "java", "herencia", "polimorfismo", "interfaz"]):
                if len(texto) > 1000:
                    texto = texto[:1000].rsplit(".", 1)[0] + "."
                return f"*Respuesta*: {texto}\n\nFuente: [{url}]({url})"
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

