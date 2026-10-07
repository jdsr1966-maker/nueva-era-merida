import os
import re
import urllib.request
import pandas as pd
import streamlit as st

# Configuración de página optimizada para móvil
st.set_page_config(
    page_title="Nueva Era Mérida Digital", page_icon="📰", layout="centered"
)

# Ocultar herramientas de deploy/GitHub para mantener el portal limpio
st.markdown(
    """
    <style>
    [data-testid="stToolbar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
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


def extraer_imagen_og(url):
  """Extrae automáticamente la fotografía real directamente desde el enlace web de la noticia"""
  if not url or not str(url).startswith("http"):
    return ""
  try:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=6) as response:
      html = response.read().decode("utf-8", errors="ignore")

      match = re.search(
          r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
          html,
          re.IGNORECASE,
      )
      if not match:
        match = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            html,
            re.IGNORECASE,
        )
      if match:
        return match.group(1)

      match_img = re.search(
          r'<img[^>]+src=["\'](https?://[^"\']+\.(?:jpg|jpeg|png|webp))["\']',
          html,
          re.IGNORECASE,
      )
      if match_img:
        return match_img.group(1)
  except Exception:
    pass
  return ""


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

# --- CABECERA Y ACCESO DE REDACCIÓN DIRECTO PARA MÓVIL ---
st.title("📰 Nueva Era Mérida Digital")
st.markdown(
    "*Portal Informativo y Archivo Oficial — Mérida, Venezuela*"
)
st.markdown("---")

# Sistema de Acceso de Redacción Directo en Pantalla
with st.expander("🔐 Acceso de Redacción (Administrador)", expanded=False):
  password_input = st.text_input(
      "Ingrese Contraseña de Administrador", type="password"
  )

modo_admin = False
ADMIN_PASSWORD = "merida2026"

if password_input == ADMIN_PASSWORD:
  st.success("✅ Modo Redacción Activo")
  modo_admin = True
elif password_input != "":
  st.error("Contraseña incorrecta")

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
          seccion_actual = str(row["Sección"]).strip()
          enlace_noticia = str(row["Enlace Web"]).strip()
          img_path = str(row["Imagen"]).strip()

          if seccion_actual == "Opinión":
            st.markdown(f"### {row['Título']}")
            st.caption(
                f"📁 **Sección:** {row['Sección']} | ✍️ **Autor:**"
                f" {row['Autor']} | 📅 **Fecha:** {row['Fecha']}"
            )
            if pd.notna(row["Resumen"]) and str(row["Resumen"]).strip() != "":
              st.write(row["Resumen"])
            if enlace_noticia and enlace_noticia != "nan":
              if not enlace_noticia.startswith("http"):
                enlace_noticia = "https://" + enlace_noticia
              st.markdown(
                  f"🔗 **[Leer noticia completa en la"
                  f" Web]({enlace_noticia})**",
                  unsafe_allow_html=True,
              )
          else:
            if (
                not img_path
                or img_path == "nan"
                or img_path == "SIN_IMAGEN"
                or img_path.startswith("uploaded_images")
            ):
              if enlace_noticia and enlace_noticia.startswith("http"):
                img_path = extraer_imagen_og(enlace_noticia)

            if img_path and img_path.startswith("http"):
              try:
                st.image(img_path, use_container_width=True)
              except Exception:
                st.info("📰 Noticia")

            st.markdown(f"### {row['Título']}")
            st.caption(
                f"📁 **Sección:** {row['Sección']} | ✍️ **Autor:**"
                f" {row['Autor']} | 📅 **Fecha:** {row['Fecha']}"
            )
            if pd.notna(row["Resumen"]) and str(row["Resumen"]).strip() != "":
              st.write(row["Resumen"])
            if enlace_noticia and enlace_noticia != "nan":
              if not enlace_noticia.startswith("http"):
                enlace_noticia = "https://" + enlace_noticia
              st.markdown(
                  f"🔗 **[Leer noticia completa en la"
                  f" Web]({enlace_noticia})**",
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
      autor = st.text_input("Autor / Redactor", value="Jorge Sandoval")
      fecha = st.date_input("Fecha de Publicación")
      enlace_web = st.text_input(
          "Enlace Web Específico del Artículo (Blogger)",
          value="https://www.nuevaerameridadigital.com",
      )
      resumen = st.text_area("Resumen o Bajada de la Noticia")

      submit_btn = st.form_submit_button(label="Publicar Noticia en el Portal")

      if submit_btn:
        if not titulo.strip():
          st.warning("El título es obligatorio.")
        else:
          if seccion == "Opinión":
            img_path_saved = "SIN_IMAGEN"
          else:
            img_path_saved = extraer_imagen_og(enlace_web)
            if not img_path_saved:
              img_path_saved = ""

          try:
            if not df_articles.empty and "ID" in df_articles.columns:
              valid_ids = pd.to_numeric(df_articles["ID"], errors="coerce")
              nuevo_id = (
                  int(valid_ids.max()) + 1 if not valid_ids.isna().all() else 1
              )
            else:
              nuevo_id = 1
          except Exception:
            nuevo_id = len(df_articles) + 1

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
          st.success("¡Noticia publicada con éxito en el portal!")
          st.balloons()

  with tab2:
    st.markdown("### Eliminar Publicaciones o Artículos")
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

st.markdown(
    "<div style='text-align: center; color: gray;'><small>Portal Web Oficial"
    " (Blogger): <a href='https://www.nuevaerameridadigital.com'>Visitar"
    " www.nuevaerameridadigital.com</a><br>Depósito Legal:"
    " ME2026000169</small></div>",
    unsafe_allow_html=True,
                )

