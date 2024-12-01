import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar la API de OpenAI desde la variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("❌ No se encontró la clave de API de OpenAI. Asegúrate de configurarla en un archivo .env.")

# --- Función para interactuar con GPT-3.5 ---
def adaptar_email_gpt(email, cultura, formalidad, idioma):
    """
    Usa la API de OpenAI para adaptar el email según la cultura, formalidad y traducir al idioma seleccionado.
    """
    prompt = f"""
    Quiero que actúes como un experto en comunicación intercultural. 
    Reformula el siguiente email teniendo en cuenta:
    1. La cultura del lector: {cultura}.
    2. El nivel de formalidad: {formalidad}.
    3. Traduce el email al idioma: {idioma}.
    4. Mantén un tono respetuoso y profesional según las indicaciones.

    Email original:
    {email}

    Reformula el email:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en comunicación intercultural y redacción profesional."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        email_adaptado = response["choices"][0]["message"]["content"]
        return email_adaptado

    except Exception as e:
        return f"❌ Error al conectarse con GPT-3.5: {str(e)}"


# --- Configuración de la App ---
st.set_page_config(page_title="Adaptador de Emails Multilenguaje", page_icon="✉️", layout="wide")

# Introducción
st.sidebar.subheader("🌍 Importancia de la Comunicación Intercultural")
st.sidebar.write(
    """
    En un mundo globalizado, la comunicación intercultural es crucial para evitar malentendidos y construir relaciones exitosas.
    Cada cultura tiene normas y expectativas diferentes en cuanto a tono, formalidad e idioma. Esta herramienta te ayuda a adaptar
    tus correos electrónicos según estos factores para que sean más efectivos y respetuosos.
    """
)

# Botón para escuchar la introducción
texto_introductorio = """
    Bienvenido a esta aplicación de comunicación intercultural. 
    Adaptar tus mensajes según la cultura del destinatario es esencial en un mundo globalizado.
    """


# Instrucciones
st.sidebar.subheader("🛠️ Instrucciones de Uso")
st.sidebar.write(
    """
    1. Escribe tu correo electrónico en el cuadro principal.
    2. Selecciona:
        - La **cultura** del destinatario.
        - El **nivel de formalidad** deseado.
        - El **idioma** al que deseas traducir el correo.
    3. Haz clic en "Adaptar y Traducir Email".
    4. Copia el resultado adaptado y envíalo.
    """
)

# --- Pantalla Principal ---
st.title("📧 Adaptador de Emails Multilenguaje con GPT-3.5")
st.write(
    """
    Esta herramienta utiliza **ChatGPT (GPT-3.5)** para ayudarte a adaptar tus correos electrónicos según la cultura, 
    el nivel de formalidad del lector y traducirlos al idioma deseado.
    """
)

# --- Entrada del Email ---
st.subheader("✍️ Escribe tu email:")
email_original = st.text_area(
    "Copia aquí tu email. (Por ejemplo: Hola, espero que todo esté bien. Me gustaría discutir una propuesta contigo...)",
    height=200,
)

# --- Selección de Cultura ---
st.subheader("🌍 Selecciona la cultura del destinatario:")
cultura = st.selectbox(
    "Elige el país o región del lector:",
    ["Alemania", "España", "Latinoamérica", "Holanda", "Inglaterra", "Japón", "Estados Unidos"],
)

# --- Selección de Formalidad ---
st.subheader("💼 Selecciona el nivel de formalidad:")
formalidad = st.radio(
    "Elige el nivel de formalidad para el correo:",
    ["formal", "semiformal", "informal"],
)

# --- Selección de Idioma ---
st.subheader("🌐 Selecciona el idioma del correo:")
idioma = st.selectbox(
    "Elige el idioma al que quieres traducir el correo:",
    ["Español castizo", "Español latinoamericano", "Inglés británico", "Inglés americano", "Alemán", "Holandés", "Japonés", "Francés"],
)

# --- Botón para Adaptar ---
if st.button("Adaptar y Traducir Email"):
    if email_original.strip():
        # Llamar a la función para adaptar el email con GPT-3.5
        with st.spinner("Adaptando y traduciendo tu email con GPT-3.5..."):
            email_adaptado = adaptar_email_gpt(email_original, cultura, formalidad, idioma)

        # Mostrar resultado
        st.subheader("📧 Email Adaptado y Traducido:")
        st.text_area("Resultado:", value=email_adaptado, height=200)
    else:
        st.error("Por favor, introduce un email para adaptarlo y traducirlo.")





