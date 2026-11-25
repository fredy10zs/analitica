
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# Configuración
st.set_page_config(
    page_title="EA4 - Recarga de vehículos eléctricos",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Dashboard de recarga de vehículos eléctricos")
st.markdown(
    "Análisis del consumo energético por ciudad, "
    "hora y tipo de conector"
)

# Cargar datos
RUTA = Path("datos/ev_charging_telemetry.csv")

@st.cache_data
def cargar_datos():
    datos = pd.read_csv(RUTA)
    datos["timestamp"] = pd.to_datetime(
        datos["timestamp"], errors="coerce"
    )
    datos = datos.dropna(subset=["timestamp"]).copy()

    datos["hora"] = datos["timestamp"].dt.hour

    datos["potencia_media_observada_kw"] = (
        datos["energy_consumed_kwh"] /
        (datos["session_duration_mins"] / 60)
    )

    datos["ratio_potencia"] = (
        datos["potencia_media_observada_kw"] /
        datos["power_kw"]
    )

    return datos

df = cargar_datos()

# Filtros laterales
st.sidebar.header("Filtros")

ciudades = st.sidebar.multiselect(
    "Seleccionar ciudades",
    sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

conectores = st.sidebar.multiselect(
    "Seleccionar conectores",
    sorted(df["connector_type"].unique()),
    default=sorted(df["connector_type"].unique())
)

fecha_min = df["timestamp"].min().date()
fecha_max = df["timestamp"].max().date()

periodo = st.sidebar.date_input(
    "Seleccionar periodo",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

if len(periodo) == 2:
    inicio, fin = periodo

    filtrado = df[
        (df["city"].isin(ciudades)) &
        (df["connector_type"].isin(conectores)) &
        (df["timestamp"].dt.date >= inicio) &
        (df["timestamp"].dt.date <= fin)
    ].copy()
else:
    filtrado = df.iloc[0:0].copy()

if filtrado.empty:
    st.warning("No hay registros para los filtros seleccionados.")
    st.stop()

# Indicadores principales
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sesiones",
    f"{len(filtrado):,}"
)

col2.metric(
    "Energía total",
    f"{filtrado['energy_consumed_kwh'].sum():,.2f} kWh"
)

col3.metric(
    "Energía media",
    f"{filtrado['energy_consumed_kwh'].mean():.2f} kWh"
)

col4.metric(
    "Potencia media observada",
    f"{filtrado['potencia_media_observada_kw'].mean():.2f} kW"
)

st.divider()

# Gráficos
st.subheader("1. Sesiones por hora")

horario = (
    filtrado.groupby("hora")
    .size()
    .reset_index(name="numero_sesiones")
)

fig1 = px.bar(
    horario,
    x="hora",
    y="numero_sesiones",
    title="Número de sesiones por hora"
)

st.plotly_chart(fig1, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("2. Energía media por ciudad")

    ciudades_df = (
        filtrado.groupby("city")["energy_consumed_kwh"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        ciudades_df,
        x="city",
        y="energy_consumed_kwh",
        title="Energía media por ciudad"
    )

    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    st.subheader("3. Potencia por conector")

    conectores_df = (
        filtrado.groupby("connector_type")
        ["potencia_media_observada_kw"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        conectores_df,
        x="connector_type",
        y="potencia_media_observada_kw",
        title="Potencia media observada por conector"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Relación duración y energía
st.subheader("4. Duración y energía consumida")

fig4 = px.scatter(
    filtrado,
    x="session_duration_mins",
    y="energy_consumed_kwh",
    color="connector_type",
    title="Relación entre duración y energía"
)

st.plotly_chart(fig4, use_container_width=True)

# Tabla de datos
with st.expander("Consultar registros filtrados"):
    st.dataframe(filtrado, use_container_width=True)

st.caption(
    "Fuente: Global EV Charging Station Telemetry - Hugging Face"
)
