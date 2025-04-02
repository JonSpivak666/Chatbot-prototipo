def inicializar_flujo(session_state):
    """Inicializa los valores por defecto del flujo si no existen en la sesión."""
    session_state.setdefault("paso", "inicio")
    session_state.setdefault("seleccionados", [])
    session_state.setdefault("datos_cliente", {})

def avanzar(session_state, siguiente_paso):
    """Cambia el estado del flujo al siguiente paso."""
    session_state.paso = siguiente_paso

def reiniciar(session_state):
    """Reinicia el flujo del chatbot."""
    claves = list(session_state.keys())
    for clave in claves:
        del session_state[clave]
