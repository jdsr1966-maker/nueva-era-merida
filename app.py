import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Nueva Era Mérida Digital",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Archivo CSV local para almacenar las publicaciones de forma persistente
DATA_FILE = "articulos.csv"

# Inicializar archivo de datos con notas de prueba si no existe
if not os.path.exists(DATA_FILE):
    df_inicial = pd.DataFrame([
        {
            "Fecha": "2026-10-01",
            "Sección": "Política",
            "Título": "Avances en la gestión de servicios municipales en Mérida",
            "Contenido": "Durante las mesas de trabajo desarrolladas en el Municipio Libertador, se evaluaron los planes de optimización de servicios públicos, destacando la participación articulada de las comunidades organizadas y los gabinetes sectoriales para dar respuesta oportuna a las solicitudes vecinales."
        },
        {
            "Fecha": "2026-10-02",
            "Sección": "Memoria Viva",
            "Título": "Recordando el patrimonio histórico y cultural de nuestra ciudad",
            "Contenido": "Un recorrido por la historia urbana y arquitectónica de Mérida, resaltando el valor de los espacios coloniales, la conservación del centro histórico y la memoria de sus principales plazas y monumentos tradicionales."
        },
        {
            "Fecha": "2026-10-03",
            "Sección": "Cultura",
            "Título": "Gran éxito de la exposición artística en el centro cultural",
            "Contenido": "Con la participación de más de veinte artistas plásticos locales, se inauguró la muestra confluencias, convirtiéndose en un punto de encuentro para el talento merideño y la ciudadanía."
        },
        {
            "Fecha": "2026-10-05",
            "Sección": "Institucional",
            "Título": "Municipio Libertador instala Comisión Técnica para el Plan de Desarrollo Urbano",
            "Contenido": "Con el objetivo de actualizar los instrumentos de ordenamiento territorial y zonificación, las autoridades municipales y los consejos locales de planificación instalaron formalmente la Comisión Técnica encargada de revisar el marco normativo histórico y adaptarlo a las necesidades actuales del municipio."
        }
    ])
    df_inicial.to_csv(DATA_FILE, index=False)

# Cargar datos
@st.cache_data(ttl=0)
def cargar_datos():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Fecha", "Sección", "Título", "Contenido"])

df = cargar_datos()

# Sidebar / Navegación
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
        "🗂️ Base de Datos Completa"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("🌐 www.nuevaerameridadigital.com")

# 1. TABLERO DE REDACCIÓN
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
    st.subheader("📋 Resumen Reciente")
    if not df.empty:
        for idx, row in df.tail(5).iterrows():
            with st.expander(f"📌 [{row['Sección']}] {row['Título']} ({row['Fecha']})"):
                st.write(f"**Fecha:** {row['Fecha']}")
                st.write(f"**Sección:** {row['Sección']}")
                st.markdown("---")
                st.write(row['Contenido'])
    else:
        st.info("No hay publicaciones registradas todavía.")

# 2. REGISTRAR / CARGAR ARTÍCULO
elif menu == "✍️ Registrar / Cargar Artículo":
    st.title("✍️ Registrar / Cargar Nuevo Artículo")
    st.markdown("Ingrese los datos del nuevo artículo para publicarlo instantáneamente en el portal.")
    st.markdown("---")
    
    with st.form("form_articulo"):
        titulo = st.text_input("Título del Artículo / Nota")
        seccion = st.selectbox("Sección Editorial", ["Política", "Institucional", "Cultura", "Memoria Viva", "Comunidades", "Opinión", "Deportes", "Especiales"])
        fecha = st.date_input("Fecha de Publicación")
        contenido = st.text_area("Cuerpo / Contenido Completo del Artículo", height=200)
        
        submitted = st.form_submit_button("Publicar en la App")
        if submitted:
            if titulo.strip() and contenido.strip():
                nueva_fila = pd.DataFrame([{
                    "Fecha": str(fecha),
                    "Sección": seccion,
                    "Título": titulo,
                    "Contenido": contenido
                }])
                df_updated = pd.concat([df, nueva_fila], ignore_index=True)
                df_updated.to_csv(DATA_FILE, index=False)
                st.success("✅ ¡Artículo publicado exitosamente! Ya puedes visualizarlo en el Visor por Secciones y en la Base de Datos Completa.")
                st.balloons()
            else:
                st.error("⚠️ Por favor completa el título y el contenido del artículo.")

# 3. VISOR POR SECCIONES (CON LECTURA COMPLETA)
elif menu == "📂 Visor por Secciones":
    st.title("📂 Visor Organizado por Secciones")
    st.markdown("Filtra las publicaciones por categoría y lee el contenido completo de cada artículo.")
    st.markdown("---")
    
    if not df.empty:
        secciones_disponibles = df["Sección"].unique().tolist()
        seccion_seleccionada = st.selectbox("Filtrar contenido por sección:", secciones_disponibles)
        
        df_filtrado = df[df["Sección"] == seccion_seleccionada]
        st.markdown(f"### Se encontraron {len(df_filtrado)} publicaciones en la sección **{seccion_seleccionada}**:")
        
        # Selector de artículo para lectura detallada
        titulos_seccion = df_filtrado["Título"].tolist()
        articulo_elegido = st.selectbox("📖 Selecciona el artículo que deseas leer completo:", ["-- Elige una publicación --"] + titulos_seccion)
        
        st.markdown("---")
        if articulo_elegido != "-- Elige una publicación --":
            fila_articulo = df_filtrado[df_filtrado["Título"] == articulo_elegido].iloc[0]
            st.markdown(f"## 📰 {fila_articulo['Título']}")
            st.markdown(f"**📅 Fecha:** {fila_articulo['Fecha']} &nbsp;&nbsp;|&nbsp;&nbsp; **🏷️ Sección:** {fila_articulo['Sección']}")
            st.markdown("---")
            st.write(fila_articulo["Contenido"])
            st.markdown("---")
        
        # Mostrar tabla resumen debajo
        st.dataframe(df_filtrado[["Fecha", "Sección", "Título"]], use_container_width=True)
    else:
        st.info("No hay publicaciones registradas.")

# 4. BUSCAR EN EL ARCHIVO
elif menu == "🔍 Buscar en el Archivo":
    st.title("🔍 Búsqueda en el Archivo Editorial")
    st.markdown("Busca notas y artículos por palabras clave en el título o contenido.")
    st.markdown("---")
    
    busqueda = st.text_input("Ingrese término de búsqueda (ej. Libertador, Cultura, etc.):")
    if busqueda:
        resultado = df[df["Título"].str.contains(busqueda, case=False, na=False) | df["Contenido"].str.contains(busqueda, case=False, na=False)]
        st.markdown(f"### Resultados encontrados: {len(resultado)}")
        if not resultado.empty:
            for idx, row in resultado.iterrows():
                with st.expander(f"📌 [{row['Sección']}] {row['Título']} ({row['Fecha']})"):
                    st.write(f"**Fecha:** {row['Fecha']} | **Sección:** {row['Sección']}")
                    st.write(row['Contenido'])
        else:
            st.warning("No se encontraron artículos con ese término.")

# 5. BASE DE DATOS COMPLETA
elif menu == "🗂️ Base de Datos Completa":
    st.title("🗂️ Base de Datos Completa de Redacción")
    st.markdown("Registro general e histórico de todas las notas publicadas en el portal.")
    st.markdown("---")
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### 📖 Lector Rápido de Artículos")
        titulos_todos = df["Título"].tolist()
        articulo_db = st.selectbox("Seleccione un artículo de todo el archivo para leerlo:", ["-- Seleccionar --"] + titulos_todos)
        if articulo_db != "-- Seleccionar --":
            fila_db = df[df["Título"] == articulo_db].iloc[0]
            st.markdown(f"## 📰 {fila_db['Título']}")
            st.markdown(f"**📅 Fecha:** {fila_db['Fecha']} | **🏷️ Sección:** {fila_db['Sección']}")
            st.markdown("---")
            st.write(fila_db["Contenido"])
    else:
        st.info("La base de datos está vacía.")
