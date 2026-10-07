import os
import pandas as pd
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Nueva Era Mérida Digital", page_icon="📰", layout="wide"
)

DATA_FILE = "articles.csv"
IMAGES_DIR = "uploaded_images"
os.makedirs(IMAGES_DIR, exist_ok=True)

SECCIONES_OFICIALES = [
    "Opinión",
    "Comunidades",
    "Institucional",
    "Cultura",
    "Memoria Viva",
    "Deportes",
    "Política",
]


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      df = pd.read_csv(DATA_FILE)
      expected_cols = [
          "ID",
          "Fecha",
          "Título",
          "Sección",
          "Autor",
          "Enlace Web",
          "Resumen",
          "Imagen",
      ]
      for col in expected_cols:
        if col not in df.columns:
          df[col] = ""
      return df
    except Exception:
      pass

  # Datos iniciales de ejemplo
  data_inicial = {
      "ID": [1, 2],
      "Fecha": ["2026-10-02", "2026-09-25"],
      "Título": [
          "Selección de delegados parroquiales y sectoriales del CLPP",
          (
              "Exposición 'Confluencias 2: Metamorfosis' en el Museo de Arte"
              " Colonial"
          ),
      ],
      "Sección": ["Institucional", "Cultura"],
      "Autor": ["Equipo Editorial", "Equipo Editorial"],
      "Enlace Web": [
          "https://www.nuevaerameridadigital.com",
          "https://www.nuevaerameridadigital.com",
      ],
      "Resumen": [
          (
              "Cobertura especial sobre la elección y selección de delegados"
              " para el Consejo Local de Planificación Pública en Mérida."
          ),
          (
              "Reporte cultural detallando la muestra colectiva de veintitrés"
              " artistas plásticos locales."
          ),
      ],
      "Imagen": ["", ""],
  }
  df = pd.DataFrame(data_inicial)
  df.to_csv(DATA_FILE, index=False)
  return df


def save_data(df):
  df.to_csv(DATA_FILE, index=False)


df_articles = load_data()

# --- BARRA LATERAL ---
st.sidebar.markdown("### 📰 Nueva Era Mérida Digital")

# Carga segura del logo principal
logo_file = "logo.jpg"
for fname in ["logo.jpg", "logo.png", "logo.jpeg", "Logo.png", "Logo.jpg"]:
  if os.path.exists(fname):
    logo_file = fname
    break

if os.path.exists(logo_file):
  try:
    st.sidebar.image(logo_file, use_container_width=True)
  except Exception:
    pass

st.sidebar.markdown("---")

# Sistema de Acceso de Redacción Protegido
st.sidebar.markdown("### 🔐 Acceso de Redacción")
modo_admin = False
password_input = st.sidebar.text_input(
    "Contraseña de Administrador", type="password"
)
ADMIN_PASSWORD = "merida2026"

if password_input == ADMIN_PASSWORD:
  st.sidebar.success("✅ Modo Redacción Activo")
  modo_admin = True
elif password_input != "":
  st.sidebar.error("Contraseña incorrecta")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Portal Web Oficial (Blogger):**\n[Visitar"
    " www.nuevaerameridadigital.com](https://www.nuevaerameridadigital.com)"
)
st.sidebar.markdown(
    "<small>Depósito Legal: ME2026000169</small>", unsafe_allow_html=True
)

# --- CUERPO PRINCIPAL ---
st.title("📰 Nueva Era Mérida Digital")
st.markdown(
    "*Portal Informativo y Archivo Oficial — Mérida, Venezuela*"
)
st.markdown("---")

if not modo_admin:
  # --- VISTA PÚBLICA (LECTORES) ---
  st.subheader("Últimas Publicaciones")

  if df_articles.empty:
    st.info("No hay publicaciones disponibles en este momento.")
  else:
    secciones_disponibles = ["Todas"] + SECCIONES_OFICIALES
    seccion_filtro = st.selectbox(
        "Filtrar por Sección Informativa", secciones_disponibles
    )

    if seccion_filtro != "Todas":
      df_filtered = df_articles[df_articles["Sección"] == seccion_filtro]
    else:
      df_filtered = df_articles

    if df_filtered.empty:
      st.info(f"No hay notas en la sección '{seccion_filtro}' todavía.")
    else:
      for index, row in df_filtered.iloc[::-1].iterrows():
        with st.container():
          col_img, col_txt = st.columns([1, 2])

          with col_img:
            img_path = str(row["Imagen"]).strip()
            if img_path and img_path != "nan":
              try:
                st.image(img_path, use_container_width=True)
              except Exception:
                st.info("📰 Nueva Era Mérida Digital")
            else:
              st.info("📰 Nueva Era Mérida Digital")

          with col_txt:
            st.markdown(f"### {row['Título']}")
            st.caption(
                f"📁 **Sección:** {row['Sección']} | ✍️ **Autor:**"
                f" {row['Autor']} | 📅 **Fecha:** {row['Fecha']}"
            )

            if pd.notna(row["Resumen"]) and str(row["Resumen"]).strip() != "":
              st.write(row["Resumen"])

            enlace = str(row["Enlace Web"]).strip()
            if enlace and enlace != "nan":
              if not enlace.startswith("http"):
                enlace = "https://" + enlace
              st.markdown(
                  f"🔗 **[Leer noticia completa en la"
                  f" Web]({enlace})**",
                  unsafe_allow_html=True,
              )

          st.markdown("---")

else:
  # --- VISTA DE ADMINISTRACIÓN (REDACCIÓN Y ELIMINACIÓN) ---
  st.subheader("🛠️ Panel de Control y Gestión Editorial")

  tab1, tab2 = st.tabs(
      ["✍️ Registrar Nueva Noticia", "🗑️ Gestionar y Eliminar Noticias"]
  )

  with tab1:
    with st.form("form_nueva_nota_admin", clear_on_submit=True):
      titulo = st.text_input("Título de la Noticia")
      seccion = st.selectbox("Sección", SECCIONES_OFICIALES)
      autor = st.text_input("Autor / Redactor", value="Equipo Editorial")
      fecha = st.date_input("Fecha de Publicación")
      enlace_web = st.text_input(
          "Enlace Web del Artículo (Blogger)",
          value="https://www.nuevaerameridadigital.com",
      )
      resumen = st.text_area("Resumen o Bajada de la Noticia")

      st.markdown("---")
      st.markdown("### 📷 Fotografía de la Noticia")
      imagen_url_input = st.text_input(
          "Pegar enlace directo de la imagen (URL de la foto en Blogger)"
      )
      imagen_subida = st.file_uploader(
          "O sube la foto desde tu dispositivo (Opcional)",
          type=["jpg", "jpeg", "png"],
      )

      submit_btn = st.form_submit_button(label="Publicar Noticia en el Portal")

      if submit_btn:
        if not titulo.strip():
          st.warning("El título es obligatorio.")
        else:
          img_path_saved = ""
          # 1. Si subió archivo local, tiene prioridad
          if imagen_subida is not None:
            img_path_saved = os.path.join(IMAGES_DIR, imagen_subida.name)
            with open(img_path_saved, "wb") as f:
              f.write(imagen_subida.getbuffer())
          # 2. Si pegó la URL de la imagen, usarla
          elif imagen_url_input.strip():
            img_path_saved = imagen_url_input.strip()

          nuevo_id = (
              int(df_articles["ID"].max()) + 1
              if not df_articles.empty and "ID" in df_articles.columns
              else 1
          )

          nueva_fila = pd.DataFrame(
              [{
                  "ID": nuevo_id,
                  "Fecha": str(fecha),
                  "Título": titulo,
                  "Sección": seccion,
                  "Autor": autor,
                  "Enlace Web": enlace_web,
                  "Resumen": resumen,
                  "Imagen": img_path_saved,
              }]
          )
          df_articles = pd.concat([df_articles, nueva_fila], ignore_index=True)
          save_data(df_articles)
          st.success("¡Noticia publicada con éxito con su respectiva foto!")
          st.balloons()

  with tab2:
    st.markdown(
        "### Eliminar Publicaciones Duplicadas o Fuera de Vigencia"
    )
    if df_articles.empty:
      st.info("No hay notas registradas para administrar.")
    else:
      for idx, row in df_articles.iterrows():
        col_a, col_b = st.columns([4, 1])
        with col_a:
          st.markdown(
              f"**[{row['Sección']}] {row['Título']}** ({row['Fecha']})"
          )
        with col_b:
          if st.button("🗑️ Eliminar", key=f"del_{row['ID']}_{idx}"):
            df_articles = df_articles.drop(idx).reset_index(drop=True)
            save_data(df_articles)
            st.success("Noticia eliminada correctamente.")
            st.rerun()
