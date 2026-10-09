import datetime
import requests
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Nueva Era Mérida Digital", page_icon="📰", layout="wide"
)

# Mostrar el logo del periódico (utiliza el archivo logo.jpg de su repositorio)
try:
  st.image("logo.jpg", width=220)
except Exception:
  pass

st.title("Nueva Era Mérida Digital")
st.markdown("---")

# URL de la API de Google Sheets
API_URL = "https://script.google.com/macros/s/AKfycbzlRR2RRkKdzC19WqVulEEB-0gyqu5XbwWRp-96K-JGAVhbeGAjFON1sVVzG8pUzWhV/exec"


# Función para consultar las noticias desde Google Sheets
def obtener_noticias():
  try:
    response = requests.get(API_URL)
    return response.json()
  except Exception as e:
    return []


# Panel lateral para publicar noticias de forma rápida
st.sidebar.header("✍️ Redacción y Publicación")
with st.sidebar.form("form_publicar"):
  st.write("Crear nueva nota")
  titulo = st.text_input("Título")
  seccion = st.selectbox(
      "Sección",
      [
          "Local",
          "Comunidad",
          "Opinión",
          "Cultura",
          "Deportes",
          "Memoria Histórica",
      ],
  )
  autor = st.text_input("Autor / Redacción", value="Redacción")
  fecha = st.date_input(
      "Fecha", value=datetime.date.today()
  ).strftime("%Y-%m-%d")
  resumen = st.text_area("Resumen o bajada")
  enlace = st.text_input("Enlace Web (opcional)")
  imagen = st.text_input("URL de Imagen (opcional)")

  submit_button = st.form_submit_button("Publicar Noticia")

  if submit_button:
    if titulo and resumen:
      payload = {
          "action": "add",
          "row": {
              "ID": str(datetime.datetime.now().timestamp()),
              "Fecha": fecha,
              "Título": titulo,
              "Sección": seccion,
              "Autor": autor,
              "Enlace Web": enlace,
              "Resumen": resumen,
              "Imagen": imagen,
          },
      }
      try:
        requests.post(API_URL, json=payload)
        st.sidebar.success(
            "¡Nota enviada! Recargue la página en unos segundos."
        )
      except Exception as ex:
        st.sidebar.error(f"No se pudo publicar: {ex}")
    else:
        st.sidebar.warning("Por favor complete al menos el título y el resumen.")

# Sección principal: Visualizar noticias publicadas
st.subheader("📋 Edición Actual - Últimas Noticias")

noticias = obtener_noticias()

if noticias and isinstance(noticias, list):
  for noticia in noticias:
    st.markdown(f"### {noticia.get('Título', 'Sin título')}")
    st.write(
        f"**Sección:** {noticia.get('Sección', 'General')} | **Autor:**"
        f" {noticia.get('Autor', 'Equipo')} | **Fecha:**"
        f" {noticia.get('Fecha', '')}"
    )
    if noticia.get("Resumen"):
      st.write(noticia.get("Resumen"))
    if noticia.get("Enlace Web"):
      st.markdown(f"[Leer artículo completo]({noticia.get('Enlace Web')})")
    st.markdown("---")
else:
  st.info(
      "Aún no hay noticias registradas. Puede agregar su primera nota usando el"
      " panel de la izquierda."
  )
    
