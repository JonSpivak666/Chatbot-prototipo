import streamlit as st
import pandas as pd
import csv
import os

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

if "no_disponibles" not in st.session_state:
    st.session_state.no_disponibles = []

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "correo" not in st.session_state:
    st.session_state.correo = ""

# Mostrar historial del chat
st.title("Álvaro Medina")
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
            "Hola, soy Álvaro Medina. ¿Qué producto de software te interesa? "
            "Puedes preguntarme por disponibilidad o mencionar directamente el nombre."
        )
        st.session_state.fase = "esperando_producto"

    elif st.session_state.fase == "esperando_producto":
        disponibilidad_detectada = any(p in prompt.lower() for p in ["disponible", "disponibilidad", "qué tienen", "productos", "software", "ofrecen", "hay"])
        seleccionados = [nombre for nombre in productos["Nombre"] if nombre.lower() in prompt.lower()]

        if disponibilidad_detectada:
            lista = "\n".join(f"- {row['Nombre']} ({row['Disponibilidad']})" for _, row in productos.iterrows())
            respuesta = f"Estos son los productos y su disponibilidad:\n{lista}\nPuedes escribir el nombre de uno para continuar."

        elif seleccionados:
            disponibles = productos[productos["Nombre"].isin(seleccionados) & (productos["Disponibilidad"] == "Sí")]
            no_disponibles = productos[productos["Nombre"].isin(seleccionados) & (productos["Disponibilidad"] == "No")]

            if not disponibles.empty:
                st.session_state.seleccionados = disponibles["Nombre"].tolist()
                respuesta = (
                    f"La licencia de {', '.join(st.session_state.seleccionados)} está disponible. "
                    "¿Deseas solicitar una cotización formal?"
                )
                st.session_state.fase = "confirmar_cotizacion"
            elif not no_disponibles.empty:
                st.session_state.no_disponibles = no_disponibles["Nombre"].tolist()
                respuesta = (
                    f"Lamentablemente la licencia de {', '.join(st.session_state.no_disponibles)} no está disponible en este momento. "
                    "¿Podrías dejarme tu nombre completo para notificarte cuando vuelva a estar disponible?"
                )
                st.session_state.fase = "espera_nombre"
            else:
                respuesta = "No reconocí ese producto. Intenta con 'Software A' hasta 'Software L'."

        else:
            respuesta = (
                "No reconocí ningún producto. Intenta con nombres como 'Software A' hasta 'Software L', "
                "o pregunta por disponibilidad."
            )

    elif st.session_state.fase == "confirmar_cotizacion":
        if "sí" in prompt.lower() or "si" in prompt.lower():
            respuesta = "Perfecto. Por favor, proporcióname tu nombre completo."
            st.session_state.fase = "solicitar_nombre"
        else:
            respuesta = "De acuerdo. Si deseas solicitar otra licencia, dime cuál."

    elif st.session_state.fase == "solicitar_nombre":
        st.session_state.nombre = prompt.strip()
        respuesta = "Gracias. Ahora, ¿podrías proporcionarme tu correo electrónico para que un colaborador te contacte?"
        st.session_state.fase = "solicitar_correo"

    elif st.session_state.fase == "solicitar_correo":
        st.session_state.correo = prompt.strip()

        # Guardar en solicitudes.csv
        csv_path = "data/solicitudes.csv"
        encabezados = ["Nombre", "Correo", "Licencias"]
        fila = {
            "Nombre": st.session_state.nombre,
            "Correo": st.session_state.correo,
            "Licencias": ", ".join(st.session_state.seleccionados)
        }

        existe = os.path.isfile(csv_path)
        with open(csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=encabezados)
            if not existe:
                writer.writeheader()
            writer.writerow(fila)

        respuesta = (
            f"Gracias, {st.session_state.nombre}. Hemos registrado tu solicitud. "
            "Uno de nuestros colaboradores se pondrá en contacto contigo pronto. Hasta luego."
        )
        st.session_state.fase = "final"

    elif st.session_state.fase == "espera_nombre":
        st.session_state.nombre = prompt.strip()
        respuesta = "Gracias. Ahora, ¿podrías proporcionarme tu correo electrónico para notificarte cuando esté disponible?"
        st.session_state.fase = "espera_correo"

    elif st.session_state.fase == "espera_correo":
        st.session_state.correo = prompt.strip()

        # Guardar en espera.csv
        csv_path = "data/espera.csv"
        encabezados = ["Nombre", "Correo", "Producto en espera"]
        fila = {
            "Nombre": st.session_state.nombre,
            "Correo": st.session_state.correo,
            "Producto en espera": ", ".join(st.session_state.no_disponibles)
        }

        existe = os.path.isfile(csv_path)
        with open(csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=encabezados)
            if not existe:
                writer.writeheader()
            writer.writerow(fila)

        respuesta = (
            f"Gracias, {st.session_state.nombre}. Te avisaremos cuando la licencia esté disponible. Hasta luego."
        )
        st.session_state.fase = "final"

    elif st.session_state.fase == "final":
        respuesta = "¿Deseas realizar otra consulta o solicitud?"

    else:
        respuesta = "No entendí tu mensaje. Intenta nuevamente."

    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)


