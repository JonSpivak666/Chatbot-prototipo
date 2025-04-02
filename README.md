# Chatbot Álvaro Medina — Cotización de Licencias de Software

Este proyecto es un chatbot conversacional diseñado para simular atención al cliente vía WhatsApp, permitiendo a los usuarios consultar productos y generar cotizaciones de licencias de software de manera automatizada.

## Aplicación en Línea

Puedes probar el chatbot en Streamlit aquí:

[chatbot-prototipo.streamlit.app](https://chatbot-prototipo-hxtznrtudsa7qnbsrcqlpd.streamlit.app/)

---

## Funcionalidades principales

- Conversación en lenguaje natural (como WhatsApp).
- Consulta de productos disponibles (ej. “Software A” hasta “Software L”).
- Cotización automática con desglose y total.
- Captura de nombre del cliente para seguimiento.
- Mensaje final con atención personalizada.
- Soporte para integración con un modelo LLM (Hugging Face Mistral).
- Preparado para migrar a WhatsApp Business API.

---

## Tecnologías utilizadas

- Python 3.10+
- Streamlit
- pandas
- Hugging Face Inference API
- python-dotenv (uso local)
- st.secrets (para despliegue seguro en la nube)

---

## Instrucciones para ejecutar localmente

1. Clona el repositorio:

```bash
git clone https://github.com/JonSpivak666/Chatbot-prototipo.git
cd Chatbot-prototipo
