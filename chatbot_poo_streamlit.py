import streamlit as st
import re
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Chatbot POO Java", layout="centered")

# Imagen del robot (debe estar en la misma carpeta con el nombre correcto)
st.image("https://raw.githubusercontent.com/LidaN03/chatbot-poo-java/main/robot_chatbot.png", width=100)
st.markdown("<h2 style='text-align: center;'>Chatbot POO para estudiantes de Java</h2>", unsafe_allow_html=True)
st.markdown("---")

if "chat" not in st.session_state:
    st.session_state.chat = []

def buscar_en_web(pregunta):
    try:
        query = pregunta.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        resultados = soup.select("div.BNeawe.s3v9rd.AP7Wnd")
        if resultados:
            return resultados[0].text
        else:
            return "No encontré información relevante en la web."
    except Exception as e:
        return f"Ocurrió un error al buscar en la web: {e}"

def responder(mensaje):
    texto = mensaje.lower().strip()

    conceptos = {
        "clase": {
            "definicion": "📘 **Concepto**: Una clase es un molde para crear objetos. Contiene atributos (variables) y métodos (funciones).",
            "codigo": '''public class Persona {
    private String nombre;
    public void setNombre(String n) {
        this.nombre = n;
    }
    public String getNombre() {
        return nombre;
    }
}'''
        },
        "herencia": {
            "definicion": "📘 **Concepto**: La herencia permite que una clase hija adquiera atributos y métodos de una clase padre.",
            "codigo": '''class Animal {
    void hacerSonido() {
        System.out.println("Sonido genérico");
    }
}
class Perro extends Animal {
    void hacerSonido() {
        System.out.println("Guau!");
    }
}'''
        },
        "polimorfismo": {
            "definicion": "📘 **Concepto**: El polimorfismo permite usar una misma interfaz con distintas implementaciones.",
            "codigo": '''class Animal {
    void hacerSonido() {
        System.out.println("Sonido genérico");
    }
}
class Gato extends Animal {
    void hacerSonido() {
        System.out.println("¡Miau!");
    }
}
public class Main {
    public static void main(String[] args) {
        Animal a = new Gato();
        a.hacerSonido();
    }
}'''
        }
    }

    for tema, datos in conceptos.items():
        if tema in texto:
            return datos["definicion"], datos["codigo"]

    if "class" in texto or "void main" in texto:
        resultado = []
        if "class" in texto:
            clases = re.findall(r'class\\s+(\\w+)', texto)
            if clases:
                resultado.append(f"🔍 Clases detectadas: {', '.join(clases)}")
        if "extends" in texto:
            resultado.append("🧬 Se detectó herencia.")
        if "main" in texto:
            resultado.append("🧩 Método main() encontrado.")
        if resultado:
            return "🔎 Análisis de código:", "\\n".join(resultado)
        else:
            return "⚠️ Código no reconocido.", "No se detectaron patrones Java comunes."

    return buscar_en_web(texto), None

# Entrada del usuario
user_input = st.text_input("Tú:", placeholder="Haz una pregunta como '¿Qué es una clase?' o pega tu código...")

if user_input:
    st.session_state.chat.append(("Tú", user_input))
    respuesta, codigo = responder(user_input)
    st.session_state.chat.append(("Chatbot", respuesta))
    if codigo:
        st.session_state.chat.append(("Código", codigo))

# Mostrar mensajes tipo chat
for remitente, mensaje in st.session_state.chat:
    if remitente == "Tú":
        st.markdown(
            f"<div style='text-align: right; background-color: #1e88e5; color: white; padding: 10px; border-radius: 10px; margin: 5px;'>"
            f"{mensaje}</div>", unsafe_allow_html=True)
    elif remitente == "Chatbot":
        st.markdown(
            f"<div style='text-align: left; background-color: #e8f5e9; color: black; padding: 10px; border-radius: 10px; margin: 5px;'>"
            f"{mensaje}</div>", unsafe_allow_html=True)
    elif remitente == "Código":
        st.code(mensaje, language="java")

