import os
import pandas as pd
import streamlit as st

# Buscar el logo oficial para usarlo como icono de la aplicación (favicon en móvil y laptop)
logo_file = "logo.jpg"
for fname in ["logo.jpg", "logo.png", "logo.jpeg", "Logo.png", "Logo.jpg"]:
  if os.path.exists(fname):
    logo_file = fname
    break

# Configuración general de la página
st.set_page_config(
    page_title="Nueva Era Mérida Digital",
    page_icon=logo_file if os.path.exists(logo_file) else "📰",
    layout="wide",
)

# Archivo local para persistir los artículos y notas
DATA_FILE = "articles.csv"

# Secciones oficiales solicitadas
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
      # Sanitización automática de URLs malformadas de raíz
      if "Enlace Web" in df.columns:
        df["Enlace Web"] = df["Enlace Web"].astype(str)
        # Corregir si se duplicó https:// o contiene errores de tipeo
        df.loc[
            df["Enlace Web"].str.contains("https://.*https://"), "Enlace Web"
        ] = "https://www.nuevaerameridadigital.com"
        df["Enlace Web"] = df["Enlace Web"].replace(
            "nan", "https://www.nuevaerameridadigital.com"
        )
      return df
    except Exception:
      pass

  # Notas iniciales limpias y correctas
  data_inicial = {
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
  }
  df = pd.DataFrame(data_inicial)
  df.to_csv(DATA_FILE, index=False)
  return df


def save_data(df):
  df.to_csv(DATA_FILE, index=False)


# Cargar base de datos sanitizada
df_articles = load_data()

# --- BARRA LATERAL ---
st.sidebar.markdown("### 📰 Nueva Era Mérida Digital")

# Carga segura del logo en la barra lateral
if os.path.exists(logo_file):
  try:
    st.sidebar.image(logo_file, use_container_width=True)
  except Exception:
    st.sidebar.info("Panel de Redacción y Archivo")
else:
  st.sidebar.info("Panel de Redacción y Archivo")

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Menú de Navegación", ["📖 Ver Archivo de Notas", "✍️ Registrar Nueva Nota"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Portal Web Oficial (Blogger):**\n[Visitar"
    " www.nuevaerameridadigital.com](https://www.nuevaerameridadigital.com)"
)
st.sidebar.markdown(
    "<small>Depósito Legal: ME2026000169</small>", unsafe_allow_html=True
)

# Herramienta de mantenimiento de raíz en la barra lateral
with st.sidebar.expander("⚙️ Mantenimiento"):
  if st.button("🔄 Reiniciar Archivo de Notas"):
    if os.path.exists(DATA_FILE):
      os.remove(DATA_FILE)
    st.rerun()

# --- CUERPO PRINCIPAL DE LA APLICACIÓN ---
st.title("📰 Nueva Era Mérida Digital")
st.markdown(
    "*Sistema de Gestión Editorial y Archivo Informativo — Mérida, Venezuela*"
)
st.markdown("---")

if menu == "📖 Ver Archivo de Notas":
  st.subheader("Archivo de Publicaciones y Enlaces Web")

  if df_articles.empty:
    st.info("No hay notas registradas todavía.")
  else:
    secciones_disponibles = ["Todas"] + SECCIONES_OFICIALES
    seccion_filtro = st.selectbox("Filtrar por Sección", secciones_disponibles)

    if seccion_filtro != "Todas":
      df_filtered = df_articles[df_articles["Sección"] == seccion_filtro]
    else:
      df_filtered = df_articles

    st.markdown(f"**Registros encontrados:** {len(df_filtered)}")
    st.markdown("---")

    if df_filtered.empty:
      st.info(f"No hay notas registradas en la sección '{seccion_filtro}' aún.")
    else:
      for index, row in df_filtered.iterrows():
        with st.container():
          st.markdown(f"### {row['Título']}")

          col1, col2, col3 = st.columns(3)
          with col1:
            st.markdown(f"**Sección:** {row['Sección']}")
          with col2:
            st.markdown(f"**Autor:** {row['Autor']}")
          with col3:
            st.markdown(f"**Fecha:** {row['Fecha']}")

          if pd.notna(row["Resumen"]) and str(row["Resumen"]).strip() != "":
            st.markdown(f"*{row['Resumen']}*")

          if pd.notna(row["Enlace Web"]) and str(row["Enlace Web"]).strip() != "":
            st.markdown(f"🔗 **[Abrir enlace en la Web]({row['Enlace Web']})**")

          st.markdown("---")

elif menu == "✍️ Registrar Nueva Nota":
  st.subheader("Registrar Nueva Nota o Enlace")

  with st.form("form_nueva_nota"):
    titulo = st.text_input("Título de la Nota / Artículo")
    seccion = st.selectbox("Sección", SECCIONES_OFICIALES)
    autor = st.text_input("Autor / Redactor", value="Equipo Editorial")
    fecha = st.date_input("Fecha de Publicación")
    enlace_web = st.text_input(
        "Enlace Web (URL del artículo en Blogger)",
        value="https://www.nuevaerameridadigital.com",
    )
    resumen = st.text_area("Resumen o Bajada de la Nota")

    submit_button = st.form_submit_button(
        label="Guardar y Publicar en el Archivo"
    )

    if submit_button:
      if titulo.strip() == "":
        st.warning("Por favor, ingresa al menos el título de la nota.")
      else:
        # Validación automática para prevenir el error de tipeo en la URL
        enlace_limpio = enlace_web.strip()
        if (
            not enlace_limpio.startswith("http://")
            and not enlace_limpio.startswith("https://")
        ):
          enlace_limpio = "https://" + enlace_limpio

        nueva_fila = pd.DataFrame(
            [{
                "Fecha": str(fecha),
                "Título": titulo,
                "Sección": seccion,
                "Autor": autor,
                "Enlace Web": enlace_limpio,
                "Resumen": resumen,
            }]
        )
        df_articles = pd.concat([df_articles, nueva_fila], ignore_index=True)
        save_data(df_articles)
        st.success("¡Nota guardada y registrada con éxito en el archivo!")
        st.balloons()
