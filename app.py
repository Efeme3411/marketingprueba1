import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------------------
st.set_page_config(
    page_title="Dashboard STP: Starbucks America",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# ESTILOS PERSONALIZADOS (ESTILO PREMIUM STARBUCKS)
# ----------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        color: #006241;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #1e3932;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }
    
    .card {
        background-color: #f2f0eb;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #006241;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-family: 'Outfit', sans-serif;
        color: #1e3932;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .metric-container {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #006241;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666666;
        text-transform: uppercase;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Título y encabezado principal
st.markdown('<div class="main-title">☕ Segmentación y Mercado Meta: Starbucks America</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Trabajo 2 - Marketing 2026 | Facultad de Ingeniería, Universidad de Concepción</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------------
@st.cache_data
def load_data():
    # Usar ruta relativa para que funcione en GitHub y Streamlit Cloud
    return pd.read_csv("clientes_segmentados.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'clientes_segmentados.csv' en la carpeta. Asegúrate de tener el archivo en el mismo repositorio de GitHub.")
    st.stop()

# ----------------------------------------------------
# SIDEBAR FILTERS (FILTROS LATERALES INTERACTIVOS)
# ----------------------------------------------------
st.sidebar.header("🔍 Filtros de Segmento")

# 1. Filtro por Región
regiones_disponibles = ["Todas"] + sorted(df["region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Seleccionar Región", regiones_disponibles)

# 2. Filtro por Género
generos_disponibles = ["Todos"] + sorted(df["customer_gender"].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Seleccionar Género", generos_disponibles)

# 3. Filtro por Rango de Edad
edades_disponibles = ["Todos"] + sorted(df["customer_age_group"].dropna().unique().tolist())
selected_age = st.sidebar.selectbox("Seleccionar Grupo de Edad", edades_disponibles)

# 4. Filtro por Miembro de Rewards
rewards_options = ["Todos", "Miembros Rewards", "No Miembros"]
selected_rewards = st.sidebar.selectbox("Membresía Rewards", rewards_options)

# Aplicar los filtros de forma consecutiva
filtered_df = df.copy()

if selected_region != "Todas":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if selected_gender != "Todos":
    filtered_df = filtered_df[filtered_df["customer_gender"] == selected_gender]

if selected_age != "Todos":
    filtered_df = filtered_df[filtered_df["customer_age_group"] == selected_age]

if selected_rewards == "Miembros Rewards":
    filtered_df = filtered_df[filtered_df["is_rewards_member"] == 1]
elif selected_rewards == "No Miembros":
    filtered_df = filtered_df[filtered_df["is_rewards_member"] == 0]

# ----------------------------------------------------
# SECCIÓN DE MÉTRICAS CLAVE (KPIs DINÁMICOS)
# ----------------------------------------------------
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.markdown(
        f'<div class="metric-container"><div class="metric-value">{len(filtered_df):,}</div><div class="metric-label">Clientes Únicos</div></div>', 
        unsafe_allow_html=True
    )
with col_kpi2:
    total_sales = filtered_df["Monetary"].sum()
    st.markdown(
        f'<div class="metric-container"><div class="metric-value">${total_sales:,.2f}</div><div class="metric-label">Ingresos Totales</div></div>', 
        unsafe_allow_html=True
    )
with col_kpi3:
    avg_ticket = filtered_df["Monetary"].mean()
    st.markdown(
        f'<div class="metric-container"><div class="metric-value">${avg_ticket:.2f}</div><div class="metric-label">Gasto Promedio</div></div>', 
        unsafe_allow_html=True
    )
with col_kpi4:
    avg_satisfaction = filtered_df["customer_satisfaction"].mean()
    st.markdown(
        f'<div class="metric-container"><div class="metric-value">{avg_satisfaction:.2f}/5</div><div class="metric-label">Satisfacción Promedio</div></div>', 
        unsafe_allow_html=True
    )
with col_kpi5:
    rewards_pct = (filtered_df["is_rewards_member"].sum() / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    st.markdown(
        f'<div class="metric-container"><div class="metric-value">{rewards_pct:.1f}%</div><div class="metric-label">% Rewards Members</div></div>', 
        unsafe_allow_html=True
    )

st.write("")

# ----------------------------------------------------
# NAVEGACIÓN POR PESTAÑAS (TABS)
# ----------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Datos y Contexto",
    "📊 Distribución de Segmentos",
    "👤 Perfiles e Interacción",
    "🎯 Propuesta Estratégica"
])

# ==========================================
# TAB 1: DATOS Y CONTEXTO
# ==========================================
with tab1:
    st.header("📋 Contexto del Desafío y Datos de Starbucks")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Objetivo del Inversionista</div>', unsafe_allow_html=True)
        st.write("""
        Un grupo de inversionistas está analizando la viabilidad de abrir **nuevas franquicias de Starbucks** en los Estados Unidos.
        El objetivo principal es identificar y priorizar aquellas regiones o perfiles de clientes con **alta actividad transaccional**.
        
        Para ello, procesamos el pipeline de datos consolidado a nivel de cliente único (`customer_id`), combinando:
        - **Variables Conductuales (RFM)**: Recencia (días desde la última compra), Frecuencia (número de órdenes únicas), Monetary (monto total gastado).
        - **Variables Sociodemográficas**: Edad, género, región, tipo de tienda, membresía de recompensas (`is_rewards_member`) y canal favorito.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Enfoques de Modelación Aplicados</div>', unsafe_allow_html=True)
        st.write("""
        El estudio aplicó dos metodologías de segmentación independientes:
        1. **Modelamiento Conjunto (K-Means)**: Agrupamiento geométrico de los hábitos de gasto, tamaño de carro y satisfacción del cliente.
        2. **Modelamiento Sociodemográfico (StepMix LCA)**: Clasificación basada en probabilidades usando características demográficas y de membresía.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.subheader("Base de Clientes Segmentada (Vista Filtrada)")
        st.write("Usa los filtros del menú izquierdo para explorar la base consolidada:")
        
        # Seleccionar columnas relevantes para mostrar
        cols_preview = ["customer_id", "Recency", "Frequency", "Monetary", "customer_age_group", "customer_gender", "region", "is_rewards_member", "KMeans_Segment", "LCA_Segment"]
        st.dataframe(filtered_df[cols_preview], use_container_width=True, height=320)
        st.caption(f"Mostrando {len(filtered_df):,} de {len(df):,} clientes únicos según los filtros activos.")

# ==========================================
# TAB 2: DISTRIBUCIÓN DE SEGMENTOS
# ==========================================
with tab2:
    st.header("📊 Distribución y Frecuencia de los Clústeres")
    st.write("A continuación se muestra el tamaño relativo de cada segmento bajo ambos modelos sobre la muestra seleccionada.")
    
    col_dist1, col_dist2 = st.columns(2, gap="large")
    
    with col_dist1:
        st.subheader("Segmentos K-Means (Modelo Conjunto)")
        if len(filtered_df) > 0:
            counts_km = filtered_df["KMeans_Segment"].value_counts().reset_index()
            counts_km.columns = ["Segmento", "Clientes"]
            counts_km["Segmento"] = counts_km["Segmento"].apply(lambda x: f"Cluster {x}")
            
            fig_km = px.bar(
                counts_km, 
                x="Segmento", 
                y="Clientes",
                labels={"Clientes": "Número de Clientes"},
                color_discrete_sequence=["#006241"],
                text_auto=True
            )
            fig_km.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Segmentos K-Means",
                yaxis_title="Cantidad de Clientes"
            )
            st.plotly_chart(fig_km, use_container_width=True)
        else:
            st.warning("No hay datos para mostrar con los filtros seleccionados.")
            
    with col_dist2:
        st.subheader("Clases Latentes LCA (StepMix Sociodemográfico)")
        if len(filtered_df) > 0:
            counts_lca = filtered_df["LCA_Segment"].value_counts().reset_index()
            counts_lca.columns = ["Segmento", "Clientes"]
            counts_lca["Segmento"] = counts_lca["Segmento"].apply(lambda x: f"Clase {x}")
            
            fig_lca = px.bar(
                counts_lca, 
                x="Segmento", 
                y="Clientes",
                labels={"Clientes": "Número de Clientes"},
                color_discrete_sequence=["#c29b38"],
                text_auto=True
            )
            fig_lca.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Clases Latentes LCA",
                yaxis_title="Cantidad de Clientes"
            )
            st.plotly_chart(fig_lca, use_container_width=True)
        else:
            st.warning("No hay datos para mostrar.")

# ==========================================
# TAB 3: PERFILES E INTERACCIÓN
# ==========================================
with tab3:
    st.header("👤 Análisis Interactivo de Perfiles por Segmento")
    st.write("Elige un modelo y un segmento específico para visualizar en detalle sus características sociodemográficas y hábitos transaccionales.")
    
    col_sel1, col_sel2 = st.columns(2)
    
    with col_sel1:
        tipo_modelo = st.radio("1. Elegir Tipo de Segmentación", ["K-Means (Conjunto)", "LCA (Sociodemográfico)"])
        
    with col_sel2:
        if tipo_modelo == "K-Means (Conjunto)":
            cluster_ids = sorted(df["KMeans_Segment"].unique().tolist())
            selected_cluster = st.selectbox("2. Elegir Clúster / Segmento", cluster_ids, format_func=lambda x: f"Cluster KMeans {x}")
            cluster_data = df[df["KMeans_Segment"] == selected_cluster]
        else:
            cluster_ids = sorted(df["LCA_Segment"].unique().tolist())
            selected_cluster = st.selectbox("2. Elegir Clúster / Segmento", cluster_ids, format_func=lambda x: f"Clase LCA {x}")
            cluster_data = df[df["LCA_Segment"] == selected_cluster]
            
    st.markdown("---")
    
    # KPIs específicos del Clúster seleccionado
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    
    with col_p1:
        st.metric("Clientes en este Clúster", f"{len(cluster_data):,}", f"{ (len(cluster_data)/len(df))*100:.1f}% del total")
    with col_p2:
        st.metric("Gasto Total Promedio (LTV)", f"${cluster_data['Monetary'].mean():.2f}")
    with col_p3:
        st.metric("Frecuencia Promedio", f"{cluster_data['Frequency'].mean():.1f} compras")
    with col_p4:
        st.metric("Recencia Promedio", f"{cluster_data['Recency'].mean():.1f} días")
        
    st.write("")
    
    # Gráficos de desglose demográfico del clúster seleccionado
    col_g1, col_g2, col_g3 = st.columns(3)
    
    with col_g1:
        st.subheader("Grupo de Edad")
        age_counts = cluster_data["customer_age_group"].value_counts().reset_index()
        age_counts.columns = ["Grupo", "Cantidad"]
        fig_age = px.pie(age_counts, names="Grupo", values="Cantidad", hole=0.4, color_discrete_sequence=px.colors.sequential.Sunset)
        fig_age.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280)
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col_g2:
        st.subheader("Género")
        gen_counts = cluster_data["customer_gender"].value_counts().reset_index()
        gen_counts.columns = ["Género", "Cantidad"]
        fig_gen = px.pie(gen_counts, names="Género", values="Cantidad", hole=0.4, color_discrete_sequence=px.colors.sequential.Burg)
        fig_gen.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280)
        st.plotly_chart(fig_gen, use_container_width=True)
        
    with col_g3:
        st.subheader("Canal de Pedido")
        chan_counts = cluster_data["order_channel"].value_counts().reset_index()
        chan_counts.columns = ["Canal", "Cantidad"]
        fig_chan = px.bar(chan_counts, x="Canal", y="Cantidad", color="Canal", color_discrete_sequence=px.colors.qualitative.Dark2)
        fig_chan.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=280, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_chan, use_container_width=True)

# ==========================================
# TAB 4: PROPUESTA ESTRATÉGICA
# ==========================================
with tab4:
    st.header("🎯 Validación del Modelo y Propuesta Estratégica")
    
    col_strat1, col_strat2 = st.columns([1.2, 1], gap="large")
    
    with col_strat1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🧪 Consistencia Cruzada e Independencia Técnica</div>', unsafe_allow_html=True)
        st.write("""
        Al realizar la validación cruzada entre ambos modelos empleando el **Índice de Rand Ajustado (ARI)**, se obtiene un valor de **0.007**.
        
        **¿Qué significa técnicamente este valor?**
        Un ARI cercano a 0 indica que la asignación de segmentos del modelo transaccional es **estadísticamente independiente** de las clases del modelo demográfico. 
        
        Esto demuestra de manera empírica que **las variables transaccionales de gasto y frecuencia no se correlacionan con perfiles sociodemográficos predefinidos**. En Starbucks, un cliente de alto valor transaccional no pertenece a un rango de edad exclusivo, ni a un único género o región geográfica. Los patrones de compra están gobernados por el **hábito transaccional situacional** y la conveniencia del canal de venta.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">💡 Estrategia de Expansión Recomendada para Starbucks</div>', unsafe_allow_html=True)
        st.write("""
        Recomendamos firmemente a los inversionistas **no basar la apertura de nuevas sucursales en factores demográficos tradicionales** (tales como buscar exclusivamente vecindarios con alta densidad de personas de 25-34 años, o niveles específicos de ingresos).
        
        En su lugar, se debe priorizar:
        1. **Densidad de Miembros Activos (Rewards Members)**: Buscar zonas con alta penetración de usuarios activos del programa de lealtad, ya que este es el principal predictor del valor a largo plazo (LTV).
        2. **Canales de Conveniencia**: Asegurar que los locales nuevos cuenten con infraestructura de alta conveniencia (como Drive-Thru y soporte avanzado para pedidos de la Mobile App), que son los disparadores principales de las transacciones frecuentes.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_strat2:
        st.subheader("Matriz de Coincidencia KMeans vs LCA")
        st.write("Frecuencia de coincidencia cruzada de clientes asignados a cada cluster:")
        
        # Generar crosstab
        ct = pd.crosstab(df["KMeans_Segment"], df["LCA_Segment"])
        
        # Heatmap con Plotly
        fig_heat = px.imshow(
            ct,
            labels=dict(x="LCA (Sociodemográfico)", y="K-Means (Conjunto)", color="Cantidad de Clientes"),
            x=[f"Clase {i}" for i in ct.columns],
            y=[f"Cluster {i}" for i in ct.index],
            color_continuous_scale="Blues",
            text_auto=True
        )
        fig_heat.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=340
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Mostrar el valor del ARI formal
        st.metric(
            label="Índice de Rand Ajustado (ARI)",
            value="0.007",
            help="El ARI mide la concordancia estadística entre dos segmentaciones. Un valor cercano a 0 indica independencia estadística."
        )

# Footer del Dashboard
st.markdown("---")
st.caption("Dashboard interactivo para presentación final. Desarrollado con Streamlit y Plotly Express.")
