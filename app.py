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

# Logotipo oficial centrado
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
    data = res.json()
    return data if isinstance(data, list) else []
  except Exception:
    return []


# Secciones oficiales solicitadas
SECCIONES = [
    "Todas",
    "Opinión",
    "Institucional",
    "Memoria viva",
    "Cultura",
    "Deportes",
    "Comunidades",
    "Política",
]

# --- PANEL DE ACCESO RESTRINGIDO (SOLO ADMINISTRADOR) ---
with st.expander("🔒 Acceso Administrador (Publicar / Borrar)", expanded=False):
  password = st.text_input(
      "Ingrese contraseña de administrador", type="password"
  )

  if password == "1234":
    st.success("Acceso concedido. Panel de Redacción activo.")
    tab_pub, tab_ges = st.tabs(["Publicar Noticia", "Gestionar / Borrar"])

    with tab_pub:
      with st.form("form_noticia", clear_on_submit=True):
        titulo = st.text_input("Título de la Noticia")
        seccion = st.selectbox("Sección", SECCIONES[1:])
        autor = st.text_input("Autor / Redacción", value="Redacción")
        fecha = st.date_input(
            "Fecha", value=datetime.date.today()
        ).strftime("%Y-%m-%d")
        resumen = st.text_area("Contenido o bajada de la noticia")
        enlace = st.text_input("Enlace Web (opcional)")

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
                    "Imagen": "",
                },
            }
            try:
              requests.post(API_URL, json=payload)
              st.success(
                  "¡Noticia publicada con éxito! Ya puede verla en la sección"
                  " correspondiente."
              )
            except Exception as e:
              st.error(f"Error al conectar: {e}")
          else:
            st.warning("Por favor complete al menos el título y el contenido.")

    with tab_ges:
      st.write("Listado de noticias publicadas para eliminar:")
      noticias_actuales = obtener_noticias()
      if noticias_actuales:
        for i, n in enumerate(noticias_actuales):
          c1, c2 = st.columns([3, 1])
          with c1:
            st.text(
                f"[{n.get('Sección', 'General')}] {n.get('Título', 'Sin título')}"
            )
          with c2:
            row_index_sheet = i + 2
            titulo_nota = n.get("Título", "")
            if st.button("🗑️ Borrar", key=f"del_{i}_{row_index_sheet}"):
              try:
                payload_del = {
                    "action": "delete",
                    "rowIndex": row_index_sheet,
                    "titulo": titulo_nota,
                }
                requests.post(API_URL, json=payload_del)
                st.success("Noticia eliminada. Recargue la página.")
                st.rerun()
              except Exception as e:
                st.error(f"No se pudo borrar: {e}")
      else:
        st.info("No hay noticias registradas.")
  elif password:
    st.error("Contraseña incorrecta.")
  else:
    st.info(
        "Ingrese su contraseña de administrador para administrar el periódico."
    )

# --- NAVEGACIÓN POR CARPETAS (SECCIONES) ---
st.markdown("### 🗂️ Explorar Secciones")
seccion_seleccionada = st.selectbox(
    "Seleccione una sección:", SECCIONES, label_visibility="collapsed"
)

noticias = obtener_noticias()

# Filtrar según la sección seleccionada
if seccion_seleccionada != "Todas":
  noticias_filtradas = [
      n for n in noticias if n.get("Sección") == seccion_seleccionada
  ]
else:
  noticias_filtradas = noticias

st.markdown("---")
st.subheader(f"📋 {seccion_seleccionada} (Últimas publicaciones)")

if noticias_filtradas:
  # Mostrar máximo 10 noticias en la vista principal de la sección
  for noticia in noticias_filtradas[:10]:
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
  st.info(f"No hay noticias registradas en la sección '{seccion_seleccionada}'.")
