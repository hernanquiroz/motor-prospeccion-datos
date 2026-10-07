import streamlit as st
import pandas as pd
import os

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Radar de Leads: Datos & BI", page_icon="📡", layout="wide")

st.title("📡 Radar de Prospección: Análisis de Datos y BI")
st.markdown("Monitoreo automático de MIPYMES y Personas Naturales que requieren servicios de datos.")

# --- CARGAR DATOS ---
CSV_PATH = 'data/leads.csv'

if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    
    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.header("🎛️ Filtros de Búsqueda")
    
    # Filtro 1: Tipo de Cliente
    tipo_lead = st.sidebar.multiselect(
        "Tipo de Lead:", 
        options=df['Tipo'].unique(), 
        default=df['Tipo'].unique()
    )
    
    # Filtro 2: Búsqueda de texto
    texto_busqueda = st.sidebar.text_input("🔍 Buscar por necesidad o nombre:")

    # --- APLICAR FILTROS ---
    df_filtrado = df[df['Tipo'].isin(tipo_lead)]
    
    if texto_busqueda:
        df_filtrado = df_filtrado[
            df_filtrado['Necesidad_Detectada'].str.contains(texto_busqueda, case=False, na=False) |
            df_filtrado['Nombre_Persona'].str.contains(texto_busqueda, case=False, na=False) |
            df_filtrado['Nombre_Empresa'].str.contains(texto_busqueda, case=False, na=False)
        ]

    # --- MÉTRICAS RÁPIDAS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads", len(df))
    col2.metric("MIPYMES", len(df[df['Tipo'] == 'MIPYME']))
    col3.metric("Personas Nat.", len(df[df['Tipo'] == 'Persona Natural']))
    
    st.markdown("---")
    
    # --- MOSTRAR TABLA ---
    st.subheader(f"📋 Resultados ({len(df_filtrado)})")
    
    if not df_filtrado.empty:
        # Configurar columnas para que se vean bonito
        column_config = {
            "Tipo": st.column_config.TextColumn("Tipo", width="small"),
            "Nombre_Empresa": st.column_config.TextColumn("Empresa", width="medium"),
            "Nombre_Persona": st.column_config.TextColumn("Persona", width="medium"),
            "Contacto": st.column_config.LinkColumn("Enlace / Contacto", width="medium"),
            "Necesidad_Detectada": st.column_config.TextColumn("¿Qué necesitan?", width="large"),
            "Fecha": st.column_config.TextColumn("Fecha", width="small")
        }
        
        st.dataframe(
            df_filtrado, 
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )
        
        # Botón de descarga
        st.download_button(
            label="📥 Descargar Leads Filtrados (CSV)",
            data=df_filtrado.to_csv(index=False).encode('utf-8-sig'),
            file_name='leads_filtrados.csv',
            mime='text/csv'
        )
    else:
        st.warning("No hay leads que coincidan con los filtros.")

else:
    st.error("⚠️ No se ha encontrado `data/leads.csv`. Ejecuta el scraper o espera a la automatización.")
