import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Nueva Era Mérida Digital",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "articulos.csv"

@st.cache_data(ttl=0)
def cargar_datos():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        columnas_necesarias = ["Fecha", "Sección", "Título", "Contenido", "Enlace"]
        for col in columnas_necesarias:
            if col not in df.columns:
                df[col] = ""
        return df.fillna("")
    else:
        df_inicial = pd.DataFrame(columns=["Fecha", "Sección", "Título", "Contenido", "Enlace"])
        df_inicial.to_csv(DATA_FILE, index=False)
        return df_inicial

df = cargar_datos()

st.sidebar.title("Nueva Era Mérida Digital")
st.sidebar.markdown("**Sistema de Gestión y Archivo Editorial**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegación de Redacción:",
    [
        "📊 Tablero de Redacción",
        "✍️ Registrar / Cargar Artículo",
        "📂 Visor por Secciones",
        "🔍 Buscar en el Archivo",
        "🗂️️ Base de Datos Completa"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("🌐 www.nuevaerameridadigital.com")

if menu == "📊 Tablero de Redacción":
    st.title("📊 Tablero General de Redacción")
    st.markdown("Control estadístico y métricas editoriales de **Nueva Era Mérida Digital**.")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Artículos / Notas", len(df))
    with col2:
        secciones_unicas = df["Sección"].nunique() if not df.empty else 0
        st.metric("Secciones Editoriales", secciones_unicas)
    with col3:
        st.metric("Medio", "Digital Web")
        
    st.markdown("---")
    st.subheader("📋 Resumen Reciente de Publicaciones")
    if not df.empty:
        for idx, row in df.tail(5).iterrows():
            with st.expander(f"📌 [{row['Sección']}] {row['Título']} ({row['Fecha']})"):
                st.write(f"**Fecha:** {row['Fecha']}")
                st.write(f"**Sección:** {row['Sección']}")
                st.markdown("---")
                contenido_texto = str(row['Contenido']).strip()
                if contenido_texto:
                    st.write(contenido_texto)
                
                enlace = str(row.get('Enlace', '')).strip()
                if enlace and enlace.startswith("http"):
                    st.markdown("---")
                    st.link_button("🌐 Ver publicación completa en el Portal Web", enlace)
    else:
        st.info("No hay publicaciones registradas todavía. Comienza a registrar tus notas en la opción de la izquierda.")

elif menu == "✍️ Registrar / Cargar Artículo":
    st.title("✍️ Registrar / Cargar Nuevo Artículo y Enlace Web")
    st.markdown("Ingrese los datos de la nota y el enlace directo al portal para que los lectores puedan visitarla.")
    st.markdown("---")
    
    with st.form("form_articulo"):
        titulo = st.text_input("Título del Artículo / Nota")
        seccion = st.selectbox("Sección Editorial", ["Política", "Institucional", "Cultura", "Memoria Viva", "Comunidades", "Opinión", "Deportes", "Especiales"])
        fecha = st.date_input("Fecha de Publicación")
        contenido = st.text_area("Cuerpo / Resumen del Artículo", height=150)
        enlace_web = st.text_input("Enlace URL del Portal Web (opcional)", placeholder="https://www.nuevaerameridadigital.com/noticia...")
        
        submitted = st.form_submit_button("Publicar en la App")
        if submitted:
            if titulo.strip():
                nueva_fila = pd.DataFrame([{
                    "Fecha": str(fecha),
                    "Sección": seccion,
                    "Título": titulo,
                    "Contenido": contenido,
                    "Enlace": enlace_web
                }])
                df_updated = pd.concat([df, nueva_fila], ignore_index=True)
                df_updated.to_csv(DATA_FILE, index=False)
                st.success("✅ ¡Publicación registrada exitosamente en el sistema y vinculada al portal web!")
                st.balloons()
            else:
                st.error("⚠️ Por favor ingresa al menos el título del artículo.")

elif menu == "📂 Visor por Secciones":
    st.title("📂 Visor Organizado por Secciones")
    st.markdown("Filtra las publicaciones por categoría y accede directamente al contenido o al portal web.")
    st.markdown("---")
    
    if not df.empty and "Sección" in df.columns:
        secciones_disponibles = df["Sección"].unique().tolist()
        seccion_seleccionada = st.selectbox("Filtrar contenido por sección:", secciones_disponibles)
        
        df_filtrado = df[df["Sección"] == seccion_seleccionada]
        st.markdown(f"### Se encontraron {len(df_filtrado)} publicaciones en la sección **{seccion_seleccionada}**:")
        
        titulos_seccion = df_filtrado["Título"].tolist()
        articulo_elegido = st.selectbox("📖 Selecciona el artículo que deseas leer:", ["-- Elige una publicación --"] + titulos_seccion)
        
        st.markdown("---")
        if articulo_elegido != "-- Elige una publicación --":
            fila_articulo = df_filtrado[df_filtrado["Título"] == articulo_elegido].iloc[0]
            st.markdown(f"## 📰 {fila_articulo['Título']}")
            st.markdown(f"**📅 Fecha:** {fila_articulo['Fecha']} &nbsp;&nbsp;|&nbsp;&nbsp; **🏷️ Sección:** {fila_articulo['Sección']}")
            st.markdown("---")
            
            contenido_texto = str(fila_articulo["Contenido"]).strip()
            if contenido_texto:
                st.write(contenido_texto)
            
            enlace = str(fila_articulo.get("Enlace", "")).strip()
            if enlace and enlace.startswith("http"):
                st.markdown("---")
                st.link_button("🌐 Ir a ver la publicación directo en el Portal Web", enlace)
            
            st.markdown("---")
        
        st.dataframe(df_filtrado[["Fecha", "Sección", "Título"]], use_container_width=True)
    else:
        st.info("No hay publicaciones registradas todavía.")

elif menu == "🔍 Buscar en el Archivo":
    st.title("🔍 Búsqueda en el Archivo Editorial")
    st.markdown("Busca notas y artículos por palabras clave.")
    st.markdown("---")
    
    busqueda = st.text_input("Ingrese término de búsqueda:")
    if busqueda:
        resultado = df[df["Título"].str.contains(busqueda, case=False, na=False) | df["Contenido"].str.contains(busqueda, case=False, na=False)]
        st.markdown(f"### Resultados encontrados: {len(resultado)}")
        if not resultado.empty:
            for idx, row in resultado.iterrows():
                with st.expander(f"📌 [{row['Sección']}] {row['Título']} ({row['Fecha']})"):
                    st.write(f"**Fecha:** {row['Fecha']} | **Sección:** {row['Sección']}")
                    contenido_texto = str(row['Contenido']).strip()
                    if contenido_texto:
                        st.write(contenido_texto)
                    enlace = str(row.get('Enlace', '')).strip()
                    if enlace and enlace.startswith("http"):
                        st.link_button("🌐 Ver en el Portal Web", enlace)
        else:
            st.warning("No se encontraron artículos con ese término.")

elif menu == "🗂️ Base de Datos Completa":
    st.title("🗂️ Base de Datos Completa de Redacción")
    st.markdown("Registro general e histórico de todas las notas.")
    st.markdown("---")
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### 📖 Lector Rápido y Enlaces Web")
        titulos_todos = df["Título"].tolist()
        articulo_db = st.selectbox("Seleccione un artículo para ver sus detalles:", ["-- Seleccionar --"] + titulos_todos)
        if articulo_db != "-- Seleccionar --":
            fila_db = df[df["Título"] == articulo_db].iloc[0]
            st.markdown(f"## 📰 {fila_db['Título']}")
            st.markdown(f"**📅 Fecha:** {fila_db['Fecha']} | **🏷️ Sección:** {fila_db['Sección']}")
            st.markdown("---")
            contenido_texto = str(fila_db["Contenido"]).strip()
            if contenido_texto:
                st.write(contenido_texto)
            
            enlace = str(fila_db.get("Enlace", "")).strip()
            if enlace and enlace.startswith("http"):
                st.markdown("---")
                st.link_button("🌐 Ver publicación completa en el Portal Web", enlace)
    else:
        st.info("La base de datos está vacía.")
