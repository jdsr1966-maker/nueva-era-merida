import requests
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Nueva Era Mérida Digital", page_icon="📰", layout="wide"
)

# URL de la API de Google Sheets
API_URL = "https://script.google.com/macros/s/AKfycbzlRR2RRkKdzC19WqVulEEB-0gyqu5XbwWRp-96K-JGAVhbeGAjFON1sVVzG8pUzWhV/exec"

st.title("📰 Nueva Era Mérida Digital")
st.write(
    "Sistema de gestión y visualización de noticias en la nube conectado a"
    " Google Sheets."
)
st.markdown("---")


# Función para consultar las noticias desde Google Sheets
def obtener_noticias():
  try:
    response = requests.get(API_URL)
    return response.json()
  except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    return []


# Sección principal: Visualizar noticias
st.subheader("📋 Últimas Publicaciones")

noticias = obtener_noticias()

if noticias:
  for noticia in noticias:
    st.markdown(f"### {noticia.get('Título', 'Sin título')}")
    st.write(
        f"**Sección:** {noticia.get('Sección', 'General')} | **Autor:**"
        f" {noticia.get('Autor', 'Equipo')} | **Fecha:**"
        f" {noticia.get('Fecha', '')}"
    )
    st.write(noticia.get("Resumen", ""))
    if noticia.get("Enlace Web"):
      st.markdown(f"[Leer artículo completo]({noticia.get('Enlace Web')})")
    st.markdown("---")
else:
  st.info(
      "Aún no hay noticias registradas en la hoja de cálculo o estamos"
      " esperando el primer registro."
  )
    
