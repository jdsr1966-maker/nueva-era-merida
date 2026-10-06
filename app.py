import streamlit as st
import pandas as pd
import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión Editorial - Nueva Era Mérida Digital",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOGOTIPO Y BARRA LATERAL ---
try:
    st.sidebar.image("logo.jpg", use_container_width=True)
except Exception:
    st.sidebar.title("📰 Nueva Era Mérida Digital")

st.sidebar.markdown("**Sistema de Gestión y Archivo Editorial**")
st.sidebar.markdown("[www.nuevaerameridadigital.com](https://www.nuevaerameridadigital.com)")
st.sidebar.markdown("---")

# Menú Principal de Redacción
menu = st.sidebar.radio(
    "Navegación de Redacción:",
    [
        "📊 Tablero de Redacción",
        "📝 Registrar / Cargar Artículo",
        "📰 Visor por Secciones",
        "🔍 Buscar en el Archivo",
        "📁 Base de Datos Completa"
    ]
)

# Secciones oficiales del periódico
secciones_oficiales = [
    "Opinión", 
    "Política", 
    "Institucional", 
    "Comunidades", 
    "Cultura", 
    "Deportes", 
    "Memoria Viva", 
    "Agenda Comunitaria y Servicios"
]

# Base de demostración interna para arrancar de inmediato
if "df_articulos" not in st.session_state:
    st.session_state.df_articulos = pd.DataFrame({
        "Fecha": ["2026-10-01", "2026-10-02", "2026-10-03"],
        "Sección": ["Política", "Memoria Viva", "Cultura"],
        "Título": [
            "Avances en la gestión de servicios municipales en Libertador", 
            "Recordando el patrimonio histórico y cultural de Mérida", 
            "Gran éxito de la exposición artística en el centro"
        ],
        "Autor": ["Jorge David Sandoval Rujano", "Redacción", "Cultura Mérida"],
        "Estado": ["Publicado", "Publicado", "Borrador"]
    })

df = st.session_state.df_articulos
sec_col = "Sección"
tit_col = "Título"

# ==========================================
# MÓDULO 1: TABLERO DE REDACCIÓN
# ==========================================
if menu == "📊 Tablero de Redacción":
    st.title("📊 Tablero General de Redacción")
    st.write("Control estadístico y métricas editoriales de **Nueva Era Mérida Digital**.")
    st.markdown("---")
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.metric("Total Artículos / Notas", f"{len(df):,}".replace(",", "."))
    with col_k2:
        st.metric("Secciones Editoriales", len(secciones_oficiales))
    with col_k3:
        st.metric("Medio", "Digital Web")
    with col_k4:
        st.metric("Dirección", "Jorge S. R.")
    
    st.markdown("---")
    
    c_ex1, c_ex2 = st.columns(2)
    with c_ex1:
        st.subheader("📈 Distribución de Artículos por Sección")
        res_sec = df.groupby(sec_col).size().reset_index(name="Cantidad").sort_values(by="Cantidad", ascending=False)
        st.dataframe(res_sec, use_container_width=True)
        
    with c_ex2:
        st.subheader("📋 Resumen de Secciones Activas")
        for sec in secciones_oficiales:
            st.markdown(f"- **{sec}**: Sección habilitada.")

# ==========================================
# MÓDULO 2: REGISTRAR / CARGAR ARTÍCULO
# ==========================================
elif menu == "📝 Registrar / Cargar Artículo":
    st.title("📝 Registro de Nuevo Contenido Editorial")
    st.markdown("---")
    
    with st.form("form_nuevo_articulo", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_titulo = st.text_input("Título del Artículo o Nota de Prensa")
            f_seccion = st.selectbox("Seleccione la Sección", secciones_oficiales)
            f_autor = st.text_input("Autor / Redactor", value="Jorge David Sandoval Rujano")
        with col_f2:
            f_fecha = st.date_input("Fecha de Publicación", datetime.date.today())
            f_estado = st.selectbox("Estado del Contenido", ["Publicado", "Borrador", "En revisión"])
            f_url = st.text_input("Enlace web (URL opcional)")
        
        f_resumen = st.text_area("Resumen o Párrafo de Entrada (Lead)")
        
        enviar_btn = st.form_submit_button("Guardar en el Sistema")
        if enviar_btn:
            if f_titulo:
                nuevo_registro = pd.DataFrame({
                    "Fecha": [str(f_fecha)],
                    "Sección": [f_seccion],
                    "Título": [f_titulo],
                    "Autor": [f_autor],
                    "Estado": [f_estado]
                })
                st.session_state.df_articulos = pd.concat([st.session_state.df_articulos, nuevo_registro], ignore_index=True)
                st.success(f"¡Artículo registrado con éxito en la sección **{f_seccion}**!")
            else:
                st.error("Por favor completa al menos el Título del artículo.")

# ==========================================
# MÓDULO 3: VISOR POR SECCIONES
# ==========================================
elif menu == "📰 Visor por Secciones":
    st.title("📰 Archivo Organizado por Secciones")
    st.markdown("---")
    
    sec_elegida = st.selectbox("Filtrar contenido por sección:", secciones_oficiales)
    temp_df = df.copy()
    temp_df["_sec_clean_"] = temp_df[sec_col].astype(str).str.strip().str.title()
    df_filtrado = temp_df[temp_df["_sec_clean_"] == sec_elegida.title()]
    
    if not df_filtrado.empty:
        st.success(f"Se encontraron {len(df_filtrado)} publicaciones en la sección **{sec_elegida}**:")
        st.dataframe(df_filtrado.drop(columns=["_sec_clean_"], errors="ignore"), use_container_width=True)
    else:
        st.info(f"No hay registros cargados actualmente para la sección {sec_elegida}.")

# ==========================================
# MÓDULO 4: BUSCAR EN EL ARCHIVO
# ==========================================
elif menu == "🔍 Buscar en el Archivo":
    st.title("🔍 Buscador General de Artículos")
    st.markdown("---")
    
    query = st.text_input("Ingrese palabra clave, título, autor o fecha a buscar:")
    if query:
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        resultado = df[mask]
        if not resultado.empty:
            st.success(f"¡Se encontraron {len(resultado)} coincidencia/s!")
            st.dataframe(resultado, use_container_width=True)
        else:
            st.warning("No se encontraron registros que coincidan con la búsqueda.")

# ==========================================
# MÓDULO 5: BASE DE DATOS COMPLETA
# ==========================================
elif menu == "📁 Base de Datos Completa":
    st.title("📁 Visor General del Archivo Editorial")
    st.markdown("---")
    st.dataframe(df, use_container_width=True)