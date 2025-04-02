import streamlit as st
import pandas as pd
from logic.cotizador import generar_cotizacion
from logic.llm_responder import responder_llm

# Cargar productos
@st.cache_data
def cargar_productos():
    return pd.read_csv("data/productos.csv")

productos = cargar_productos()

# Inicializar estado de sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "fase" not in st.session_state:
    st.session_state.fase = "inicio"

if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "cotizacion_realizada" not in st.session_state:
    st.session_state.cotizacion_realizada = False

# Mostrar historial del chat
st.title("💬 Álvaro Medina")
st.markdown("Asistente conversacional de licencias de software")
for mensaje in st.session_state.chat_history:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu mensaje aquí...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    respuesta = ""

    if st.session_state.fase == "inicio":
        respuesta = (
            "Hola, soy Álvaro Medina. ¿En que puedo ayudarte "

        )
        st.session_state.fase = "esperando_producto"

    elif st.session_state.fase == "esperando_producto":
        # Intención: disponibilidad de productos
        if any(palabra in prompt.lower() for palabra in ["disponible", "tienen", "productos", "software", "hay"]):
            lista = "\n".join(f"- {nombre}" for nombre in productos["Nombre"])
            respuesta = (
                f"Estos son los productos que tengo disponibles:\n{lista}\n"
                "Puedes escribir el nombre de uno para cotizarlo."
            )
        else:
            # Buscar productos mencionados por nombre exacto
            seleccionados = [nombre for nombre in productos["Nombre"] if nombre.lower() in prompt.lower()]
            if seleccionados:
                st.session_state.seleccionados = seleccionados
                respuesta = (
                    f"He encontrado los siguientes productos: {', '.join(seleccionados)}. "
                    "¿Deseas generar la cotización ahora?"
                )
                st.session_state.fase = "confirmar_cotizacion"
            else:
                respuesta = (
                    "No encontré ese producto en mi catálogo. "
                    "Por favor, intenta con 'Software A' hasta 'Software L'."
                )

    elif st.session_state.fase == "confirmar_cotizacion":
        if "sí" in prompt.lower() or "si" in prompt.lower():
            df, total = generar_cotizacion(st.session_state.seleccionados)
            productos_str = "\n".join(f"- {row['Nombre']}: ${row['Precio (MXN)']}" for _, row in df.iterrows())
            respuesta = (
                f"Perfecto. Aquí está tu cotización:\n{productos_str}\n\n"
                f"Total: ${total:.2f} MXN. ¿Cuál es tu nombre completo para registrar esta cotización?"
            )
            st.session_state.fase = "solicitar_nombre"
        else:
            respuesta = "Está bien. ¿Quieres cotizar otro producto?"

    elif st.session_state.fase == "solicitar_nombre":
        st.session_state.nombre = prompt.strip()
        respuesta = (
            f"Gracias, {st.session_state.nombre}. "
            "Tu cotización ha sido registrada. Uno de nuestros colaboradores te atenderá a la brevedad."
        )
        st.session_state.cotizacion_realizada = True
        st.session_state.fase = "final"

    elif st.session_state.fase == "final":
        respuesta = "¿Deseas realizar otra consulta o cotización?"

    else:
        respuesta = responder_llm(prompt)

    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)

