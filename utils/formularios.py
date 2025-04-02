import streamlit as st

def formulario_cliente():
    """
    Muestra el formulario de captura de datos del cliente y devuelve un diccionario
    con los datos si están completos. Si no, devuelve None.
    """
    st.markdown("### Por favor ingresa tus datos")

    nombre = st.text_input("Nombre completo")
    correo = st.text_input("Correo electrónico")
    telefono = st.text_input("Teléfono")

    if st.button("Finalizar cotización"):
        if nombre and correo and telefono:
            return {
                "nombre": nombre.strip(),
                "correo": correo.strip(),
                "telefono": telefono.strip()
            }
        else:
            st.warning("Por favor completa todos los campos antes de continuar.")

    return None
