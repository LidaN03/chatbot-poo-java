import streamlit as st
import requests
from duckduckgo_search import DDGS
import time
import spacy
import es_core_news_sm  # Importamos el modelo como módulo

# Cargar el modelo directamente
nlp = es_core_news_sm.load()

st.set_page_config(page_title="ChatBot POO", layout="centered")


# Estilo visual básico (puedes personalizarlo)
st.markdown("""<style>
.chat-bubble {padding: 10px; border-radius: 10px; margin-bottom: 10px;}
.chat-bubble.user {background-color: #DCF8C6; text-align: right;}
.chat-bubble.bot {background-color: #F1F0F0; text-align: left;}
</style>""", unsafe_allow_html=True)

st.image("robot_chatbot.png", width=120)

st.title("Chatbot POO para estudiantes de Java")
st.subheader("Pregúntame sobre clases, herencia, ejemplos de código en Java y más. ¡Estoy aquí para ayudarte!")

if "history" not in st.session_state:
    st.session_state.history = []

# Diccionario de conceptos
conceptos_directos = {
    "herencia": "La herencia en POO permite que una clase herede atributos y métodos de otra.",
    "polimorfismo": "El polimorfismo permite que objetos de distintas clases sean tratados como uno solo.",
    "encapsulamiento": "El encapsulamiento oculta el estado interno de un objeto y expone solo lo necesario.",
    "abstracción": "La abstracción permite centrarse en los aspectos esenciales de un objeto."
}

# Diccionario de ejemplos de código
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
    int sumar(int a, int b) { return a + b; }
    double sumar(double a, double b) { return a + b; }
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

# FUNCIONES DE PLN

def obtener_palabras_clave(pregunta):
    doc = nlp(pregunta.lower())
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

def entender_tema_usuario(pregunta):
    palabras_clave = obtener_palabras_clave(pregunta)
    mejor_tema = None
    mayor_coincidencias = 0

    for tema in conceptos_directos:
        coincidencias = sum(1 for palabra in palabras_clave if palabra in tema.lower())
        if coincidencias > mayor_coincidencias:
            mejor_tema = tema
            mayor_coincidencias = coincidencias

    return mejor_tema

def detectar_intencion(pregunta):
    pregunta = pregunta.lower()
    if any(p in pregunta for p in ["ejemplo", "código", "programa"]):
        return "codigo"
    if any(p in pregunta for p in ["qué es", "define", "explica", "significa"]):
        return "definicion"
    return "otro"

def buscar_respuesta_clara(pregunta):
    tema = entender_tema_usuario(pregunta)
    intencion = detectar_intencion(pregunta)

    if intencion == "codigo":
        if tema and tema in codigos_java:
            return f"*Ejemplo de código Java sobre {tema}:*\n{codigos_java[tema]}"
        else:
            return "Lo siento, no tengo un ejemplo específico para eso. Prueba con 'interfaz' o 'sobrecarga'."

    if intencion == "definicion":
        if tema and tema in conceptos_directos:
            respuesta = conceptos_directos[tema]
            with DDGS() as ddgs:
                resultados = list(ddgs.text(keywords=f"{tema} programación orientada a objetos", max_results=3))
                for r in resultados:
                    url = r.get("href", "")
                    if url:
                        return f"*Respuesta*: {respuesta}\n\nFuente: [{url}]({url})"

    # Último recurso: búsqueda general
    with DDGS() as ddgs:
        resultados = list(ddgs.text(keywords=pregunta, max_results=5))
        for r in resultados:
            url = r.get("href", "")
            texto = r.get("body", "").strip()
            if any(k in texto.lower() for k in conceptos_directos.keys()):
                return f"*Respuesta*: {texto[:800]}...\n\nFuente: [{url}]({url})"

    return "Lo siento, no encontré una respuesta clara. ¿Puedes reformular tu pregunta?"

# INTERFAZ DEL USUARIO

user_input = st.text_input("Escribe tu mensaje:", "")

if st.button("Enviar") and user_input:
    st.session_state.history.append(("user", user_input))
    with st.spinner("Analizando tu mensaje..."):
        time.sleep(1)
        respuesta = buscar_respuesta_clara(user_input)
    st.session_state.history.append(("bot", respuesta))

# Mostrar conversación
for autor, mensaje in st.session_state.history:
    clase = "user" if autor == "user" else "bot"
    st.markdown(f'<div class="chat-bubble {clase}">{mensaje}</div>', unsafe_allow_html=True)
