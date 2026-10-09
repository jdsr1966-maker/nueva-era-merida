import datetime
import requests
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Nueva Era Mérida Digital", page_icon="📰", layout="centered"
)

# Ocultar elementos predeterminados de Streamlit para una vista limpia de periódico
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Encabezado con el logotipo oficial centrado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  try:
    st.image("logo.jpg", use_container_width=True)
  except Exception:
    st.title("📰 Nueva Era Mérida Digital")

st.markdown(
    "<hr style='margin: 10px 0px; border: 1px solid #ccc;'>",
    unsafe_allow_html=True,
)

# URL de la API de Google Sheets
API_URL = "https://script.google.com/macros/s/AKfycbzlRR2RRkKdzC19WqVulEEB-0gyqu5XbwWRp-96K-JGAVhbeGAjFON1sVVzG8pUzWhV/exec"


# Función para consultar las noticias desde Google Sheets
def obtener_noticias():
  try:
    response = requests.get(API_URL)
    return response.json()
  except Exception as e:
    return []


# Control de Acceso (Entrar y Salir del panel de redacción)
st.sidebar.title("Panel de Control")
modo_admin = st.sidebar.toggle("🔐 Entrar al Modo Redacción")

if modo_admin:
  st.sidebar.markdown("---")
  st.sidebar.subheader("✍️ Publicar Nueva Noticia")
  with st.sidebar.form("form_publicar"):
    titulo = st.text_input("Título de la Noticia")
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
    imagen = st.text_input("URL de la Imagen (enlace directo de la foto)")

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
              "¡Noticia publicada con éxito! Recargue la página en unos segundos."
          )
        except Exception as ex:
          st.sidebar.error(f"Error al publicar: {ex}")
      else:
        st.sidebar.warning("Por favor complete al menos el título y el resumen.")

  if st.sidebar.button("🚪 Salir de Redacción"):
    st.rerun()

# Sección principal: Visualizar noticias publicadas en una sola pestaña
st.markdown("### 📋 Últimas Publicaciones")

noticias = obtener_noticias()

if noticias and isinstance(noticias, list):
  for noticia in noticias:
    # Mostrar la foto de la noticia si tiene enlace válido
    img_url = noticia.get("Imagen")
    if img_url and str(img_url).startswith("http"):
      try:
        st.image(img_url, use_container_width=True)
      except Exception:
        pass

    st.markdown(f"## {noticia.get('Título', 'Sin título')}")
    st.caption(
        f"Sección: **{noticia.get('Sección', 'General')}** | Autor:"
        f" **{noticia.get('Autor', 'Equipo')}** | Fecha:"
        f" {noticia.get('Fecha', '')}"
    )

    if noticia.get("Resumen"):
      st.write(noticia.get("Resumen"))

    if noticia.get("Enlace Web"):
      st.markdown(f"[🔗 Leer artículo completo]({noticia.get('Enlace Web')})")

    st.markdown("---")
else:
  st.info(
      "Aún no hay noticias registradas. Active el modo redacción en la barra"
      " lateral para publicar su primera nota."
      )
    
