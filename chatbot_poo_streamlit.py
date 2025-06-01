import streamlit as st
import re
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Chatbot POO Java", layout="centered")

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
        return f"Ocurrió un error al intentar buscar en la web: {e}"

def responder(mensaje):
    texto = mensaje.lower().strip()

    temas = {
        "clase": "📘 **Concepto**: Una clase en Java es una plantilla para crear objetos. Puede contener atributos y métodos.",
        "herencia": "📘 **Concepto**: La herencia permite que una clase hija adquiera atributos y métodos de una clase padre.",
        "polimorfismo": "📘 **Concepto**: El polimorfismo permite usar una misma interfaz con distintas implementaciones.",
        "encapsulacion": "📘 **Concepto**: La encapsulación oculta los detalles internos del objeto y expone solo lo necesario."
    }

    for clave, explicacion in temas.items():
        if clave in texto:
            return explicacion

    if "ejemplo" in texto:
        ejemplos = {
            "herencia": """class Animal {
    void hacerSonido() {
        System.out.println("Sonido genérico");
    }
}
class Perro extends Animal {
    void hacerSonido() {
        System.out.println("Guau!");
    }
}""",
            "clase": """public class Persona {
    private String nombre;
    public void setNombre(String n) {
        this.nombre = n;
    }
    public String getNombre() {
        return nombre;
    }
}""",
            "polimorfismo": """class Animal {
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
}"""
        }
        for clave, codigo in ejemplos.items():
            if clave in texto:
                return codigo

    if "class" in texto or "void main" in texto:
        resultado = []
        if "class" in texto:
            clases = re.findall(r'class\s+(\w+)', texto)
            if clases:
                resultado.append(f"🔍 Clases detectadas: {', '.join(clases)}")
        if "extends" in texto:
            resultado.append("🧬 Herencia detectada.")
        if "main" in texto and "void" in texto:
            resultado.append("🧩 Método main() encontrado.")
        if resultado:
            return "\n".join(resultado)
        else:
            return "⚠️ No detecté estructuras clave en tu código."

    return buscar_en_web(texto)

# Entrada de usuario
with st.container():
    user_input = st.text_input("Tú:", placeholder="Haz una pregunta o pega tu código Java")

if user_input:
    st.session_state.chat.append(("Tú", user_input))
    respuesta = responder(user_input)
    st.session_state.chat.append(("Chatbot", respuesta))

# Mostrar conversación estilo chat
for remitente, mensaje in st.session_state.chat:
    if remitente == "Tú":
        st.markdown(
            f"<div style='text-align: right; background-color: #1e88e5; color: white; padding: 10px; border-radius: 10px; margin: 5px;'>"
            f"{mensaje}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #e0f7fa; color: black; padding: 10px; border-radius: 10px; margin: 5px;'>"
            f"{mensaje}</div>", unsafe_allow_html=True)


