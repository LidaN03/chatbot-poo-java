import streamlit as st
import re

st.set_page_config(page_title="Chatbot POO Java", layout="centered")

st.markdown("<h2 style='text-align: center;'>🤖 Chatbot POO para estudiantes de Java</h2>", unsafe_allow_html=True)
st.markdown("---")

# Sesión para mantener el historial del chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Diccionario de conceptos
conceptos_java = {
    "clase": "📘 **Concepto**: Una clase en Java es un molde para crear objetos. Contiene atributos (variables) y métodos (funciones).",
    "herencia": "📘 **Concepto**: La herencia permite que una clase hija adquiera atributos y métodos de una clase padre.",
    "polimorfismo": "📘 **Concepto**: El polimorfismo permite usar una misma interfaz con distintas implementaciones.",
    "encapsulacion": "📘 **Concepto**: La encapsulación oculta los detalles internos del objeto y expone solo lo necesario mediante métodos públicos."
}

# Ejemplos por tema (corregido)
ejemplos_codigo = {
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

def analizar_codigo(codigo):
    resultado = []
    if "class" in codigo:
        clases = re.findall(r'class\s+(\w+)', codigo)
        if clases:
            resultado.append(f"🔍 Clases detectadas: {', '.join(clases)}")
    if "extends" in codigo:
        resultado.append("🧬 Se detectó herencia entre clases.")
    if "main" in codigo and "void" in codigo:
        resultado.append("🧩 Método principal 'main()' encontrado.")
    if not resultado:
        resultado.append("⚠️ No se detectaron elementos clave. Verifica la sintaxis.")
    return "\n".join(resultado)

# Procesar entrada del usuario
def responder(mensaje):
    texto = mensaje.lower().strip()

    for concepto in conceptos_java:
        if concepto in texto:
            return conceptos_java[concepto] + "\n\n¿Deseas un ejemplo de código?"

    if "ejemplo" in texto or "código" in texto:
        for tema in ejemplos_codigo:
            if tema in texto:
                return ("🧾 Ejemplo de código en Java:", ejemplos_codigo[tema])

    if "class" in texto or "public static void main" in texto:
        return ("🔎 Análisis de código Java:", analizar_codigo(texto))

    return "🤔 No entendí tu mensaje. Puedes preguntarme sobre clases, herencia, polimorfismo o pegar código Java."

# Entrada tipo chat
user_input = st.text_input("Tú:", placeholder="Escribe tu pregunta o código aquí...")

if user_input:
    st.session_state.chat.append(("Tú", user_input))
    respuesta = responder(user_input)
    if isinstance(respuesta, tuple):
        st.session_state.chat.append(("Chatbot", respuesta[0]))
        st.session_state.chat.append(("Código", respuesta[1]))
    else:
        st.session_state.chat.append(("Chatbot", respuesta))

# Mostrar la conversación estilo chat
for emisor, mensaje in st.session_state.chat:
    if emisor == "Tú":
        st.markdown(f"<div style='color:blue'><strong>👤 Tú:</strong> {mensaje}</div>", unsafe_allow_html=True)
    elif emisor == "Chatbot":
        st.markdown(f"<div style='color:green'><strong>🤖 Chatbot:</strong> {mensaje}</div>", unsafe_allow_html=True)
    elif emisor == "Código":
        st.code(mensaje, language="java")

       if __name__ == '__main__':
           import os
           os.system("streamlit run " + __file__)
