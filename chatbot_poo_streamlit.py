import streamlit as st
import re

# Configura la página
st.set_page_config(page_title="Chatbot POO Java", layout="centered")

# Encabezado con imagen de robot (puedes cambiar el URL por otro PNG)
st.markdown("""
    <div style="text-align: center;">
        <img src="https://i.imgur.com/FNvV6xT.png" width="100"/>
        <h1 style="color: white; font-family: Arial;">Chatbot POO para estudiantes de Java</h1>
    </div>
""", unsafe_allow_html=True)

# Entrada del usuario
user_input = st.text_input("Haz una pregunta como '¿Qué es una clase?' o pega tu código en Java...")

# Función para procesar la entrada del usuario
def responder(pregunta):
    pregunta = pregunta.lower()

    # Explicador de conceptos
    if "qué es una clase" in pregunta:
        return "Concepto: Una clase es un molde para crear objetos. Contiene atributos (variables) y métodos (funciones)."
    if "herencia" in pregunta and "composición" in pregunta:
        return "Concepto: La herencia permite que una clase hija herede atributos y métodos de una clase padre. La composición implica que una clase contiene instancias de otras clases."
    if "polimorfismo" in pregunta:
        return "Concepto: El polimorfismo permite que distintas clases respondan al mismo método de manera diferente."

    # Generador de ejemplos
    if "ejemplo de código de herencia" in pregunta:
        return '''```java
class Animal {
    void hacerSonido() {
        System.out.println("Sonido genérico");
    }
}
class Perro extends Animal {
    void hacerSonido() {
        System.out.println("¡Guau!");
    }
}
```'''
    if "interfaz" in pregunta and "implemente" in pregunta:
        return '''```java
interface Volador {
    void volar();
}

class Pajaro implements Volador {
    public void volar() {
        System.out.println("El pájaro vuela");
    }
}
```'''

    # Análisis de código
    if "{" in pregunta and "class" in pregunta:
        return "**Análisis**: Parece que pegaste código. Este fragmento define una clase. Verifica sintaxis y estructura de métodos."

    return "No encontré información relevante sobre esa pregunta. Intenta escribir otra duda relacionada con POO."

# Mostrar respuesta
if user_input:
    st.markdown(responder(user_input))
