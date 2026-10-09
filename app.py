import datetime
import requests
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Nueva Era Mérida Digital", page_icon="📰", layout="centered"
)

# Ocultar elementos predeterminados de Streamlit para un diseño limpio
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Logotipo oficial centrado y proporcionado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  try:
    st.image("logo.jpg", use_container_width=True)
  except Exception:
    st.title("📰 Nueva Era Mérida Digital")

st.markdown(
    "<hr style='margin: 15px 0px; border: 1px solid #ddd;'>",
    unsafe_allow_html=True,
)

# URL de la API de Google Sheets
API_URL = "https://script.google.com/macros/s/AKfycbzlRR2RRkKdzC19WqVulEEB-0gyqu5XbwWRp-96K-JGAVhbeGAjFON1sVVzG8pUzWhV/exec"


# Función para consultar noticias
def obtener_noticias():
  try:
    res = requests.get(API_URL)
    return res.json()
  except Exception:
    return []


# Panel de Redacción en un menú desplegable súper cómodo para celulares
with st.expander("✍️ Panel de Redacción (Publicar Noticia)", expanded=False):
  with st.form("form_noticia"):
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
    resumen = st.text_area("Resumen o cuerpo de la noticia")
    enlace = st.text_input("Enlace Web (opcional)")
    imagen = st.text_input("URL de la Imagen (opcional)")

    btn_publicar = st.form_submit_button("Publicar Noticia")

    if btn_publicar:
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
          st.success("¡Noticia publicada con éxito! Recargue en unos segundos.")
        except Exception as e:
          st.error(f"Error al conectar: {e}")
      else:
        st.warning("Por favor complete al menos el título y el resumen.")

st.markdown("### 📋 Últimas Publicaciones")

noticias = obtener_noticias()

if noticias and isinstance(noticias, list):
  for noticia in noticias:
    img = noticia.get("Imagen")
    if img and str(img).startswith("http"):
      try:
        st.image(img, use_container_width=True)
      except Exception:
        pass

    st.markdown(f"## {noticia.get('Título', 'Sin título')}")

    autor = str(noticia.get("Autor", "Redacción")).replace("*", "").strip()
    seccion = str(noticia.get("Sección", "General")).replace("*", "").strip()
    fecha = str(noticia.get("Fecha", "")).split("T")[0]

    st.caption(f"Sección: **{seccion}** | Autor: **{autor}** | Fecha: {fecha}")

    if noticia.get("Resumen"):
      st.write(noticia.get("Resumen"))

    if noticia.get("Enlace Web"):
      st.markdown(f"[🔗 Leer artículo completo]({noticia.get('Enlace Web')})")

    st.markdown("---")
else:
  st.info(
      "Aún no hay noticias registradas. Despliegue el panel de redacción arriba"
      " para publicar la primera."
)
    
