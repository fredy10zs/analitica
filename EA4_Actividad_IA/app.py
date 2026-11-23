
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 1. CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Análisis de recarga de vehículos eléctricos",
    page_icon="🔋",
    layout="wide"
)

RUTA_DATOS = (
    Path(__file__).resolve().parent
    / "datos"
    / "ev_charging_telemetry.csv"
)


# --------------------------------------------------
# 2. CARGA Y PREPARACIÓN DE DATOS
# --------------------------------------------------

@st.cache_data
def cargar_datos(ruta):

    df = pd.read_csv(ruta)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    df = df.dropna(subset=["timestamp"]).copy()

    # Variables temporales
    df["hora"] = df["timestamp"].dt.hour
    df["fecha"] = df["timestamp"].dt.date

    # Potencia media observada a partir de energía y duración
    df["potencia_media_observada_kw"] = np.where(
        (df["session_duration_mins"] > 0)
        & (df["energy_consumed_kwh"] >= 0),
        df["energy_consumed_kwh"]
        / (df["session_duration_mins"] / 60),
        np.nan
    )

    # Relación entre potencia observada y potencia nominal
    df["ratio_potencia"] = np.where(
        df["power_kw"] > 0,
        df["potencia_media_observada_kw"] / df["power_kw"],
        np.nan
    )

    # Indicador de registros que requieren revisión
    df["posible_anomalia"] = df["ratio_potencia"] > 1

    return df


# --------------------------------------------------
# 3. VALIDACIÓN DEL ARCHIVO
# --------------------------------------------------

st.title("🔋 Transición Energética y Recarga de Vehículos Eléctricos")

st.markdown(
    """
    **Dashboard interactivo de análisis de sesiones de recarga**

    Exploración de la energía consumida y la potencia media observada
    según la hora, la ciudad y el tipo de conector.
    """
)

if not RUTA_DATOS.exists():

    st.error(
        "No se encontró el archivo de datos. "
        "Comprueba que ev_charging_telemetry.csv "
        "esté dentro de la carpeta datos."
    )

    st.stop()


df = cargar_datos(RUTA_DATOS)


# --------------------------------------------------
# 4. FILTROS INTERACTIVOS
# --------------------------------------------------

st.sidebar.header("Filtros de análisis")

fecha_min = df["timestamp"].min().date()
fecha_max = df["timestamp"].max().date()

rango_fechas = st.sidebar.date_input(
    "Periodo de análisis",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

ciudades = sorted(df["city"].dropna().unique())

ciudades_seleccionadas = st.sidebar.multiselect(
    "Seleccionar ciudades",
    options=ciudades,
    default=ciudades
)

conectores = sorted(df["connector_type"].dropna().unique())

conectores_seleccionados = st.sidebar.multiselect(
    "Seleccionar conectores",
    options=conectores,
    default=conectores
)

horas = sorted(df["hora"].dropna().unique())

horas_seleccionadas = st.sidebar.multiselect(
    "Seleccionar horas",
    options=horas,
    default=horas
)


# --------------------------------------------------
# 5. APLICACIÓN DE FILTROS
# --------------------------------------------------

if len(rango_fechas) == 2:

    fecha_inicio, fecha_fin = rango_fechas

else:

    fecha_inicio = fecha_min
    fecha_fin = fecha_max


df_filtrado = df[
    (df["timestamp"].dt.date >= fecha_inicio)
    & (df["timestamp"].dt.date <= fecha_fin)
    & (df["city"].isin(ciudades_seleccionadas))
    & (df["connector_type"].isin(conectores_seleccionados))
    & (df["hora"].isin(horas_seleccionadas))
].copy()


if df_filtrado.empty:

    st.warning(
        "No existen registros para los filtros seleccionados."
    )

    st.stop()


# --------------------------------------------------
# 6. INDICADORES KPI
# --------------------------------------------------

st.subheader("Indicadores principales")

total_sesiones = len(df_filtrado)

energia_total = df_filtrado[
    "energy_consumed_kwh"
].sum()

energia_media = df_filtrado[
    "energy_consumed_kwh"
].mean()

potencia_media = df_filtrado[
    "potencia_media_observada_kw"
].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Sesiones de recarga",
    f"{total_sesiones:,}"
)

col2.metric(
    "Energía total",
    f"{energia_total:,.2f} kWh"
)

col3.metric(
    "Energía media por sesión",
    f"{energia_media:.2f} kWh"
)

col4.metric(
    "Potencia media observada",
    f"{potencia_media:.2f} kW"
)


# --------------------------------------------------
# 7. ANÁLISIS TEMPORAL
# --------------------------------------------------

st.subheader("Actividad según la hora del día")

analisis_horario = (
    df_filtrado
    .groupby("hora")
    .agg(
        sesiones=("energy_consumed_kwh", "count"),
        energia_media=("energy_consumed_kwh", "mean"),
        energia_total=("energy_consumed_kwh", "sum")
    )
    .reset_index()
)

fig_horario = px.bar(
    analisis_horario,
    x="hora",
    y="sesiones",
    title="Número de sesiones por hora",
    labels={
        "hora": "Hora del día",
        "sesiones": "Número de sesiones"
    },
    text_auto=True
)

st.plotly_chart(
    fig_horario,
    use_container_width=True
)


# --------------------------------------------------
# 8. ANÁLISIS POR CIUDAD
# --------------------------------------------------

st.subheader("Comparación entre ciudades")

analisis_ciudades = (
    df_filtrado
    .groupby("city")
    .agg(
        sesiones=("energy_consumed_kwh", "count"),
        energia_media=("energy_consumed_kwh", "mean"),
        energia_total=("energy_consumed_kwh", "sum"),
        potencia_media=("potencia_media_observada_kw", "mean")
    )
    .reset_index()
)

fig_ciudades = px.bar(
    analisis_ciudades,
    x="city",
    y="energia_media",
    title="Energía media consumida por ciudad",
    labels={
        "city": "Ciudad",
        "energia_media": "Energía media (kWh)"
    },
    text_auto=".2f"
)

st.plotly_chart(
    fig_ciudades,
    use_container_width=True
)


# --------------------------------------------------
# 9. ANÁLISIS POR TIPO DE CONECTOR
# --------------------------------------------------

st.subheader("Comportamiento según el tipo de conector")

analisis_conectores = (
    df_filtrado
    .groupby("connector_type")
    .agg(
        sesiones=("energy_consumed_kwh", "count"),
        energia_media=("energy_consumed_kwh", "mean"),
        potencia_media=("potencia_media_observada_kw", "mean")
    )
    .reset_index()
)

fig_conectores = px.bar(
    analisis_conectores,
    x="connector_type",
    y="potencia_media",
    title="Potencia media observada por conector",
    labels={
        "connector_type": "Tipo de conector",
        "potencia_media": "Potencia media observada (kW)"
    },
    text_auto=".2f"
)

st.plotly_chart(
    fig_conectores,
    use_container_width=True
)


# --------------------------------------------------
# 10. RELACIÓN ENTRE DURACIÓN Y ENERGÍA
# --------------------------------------------------

st.subheader("Relación entre duración y energía consumida")

fig_relacion = px.scatter(
    df_filtrado,
    x="session_duration_mins",
    y="energy_consumed_kwh",
    color="connector_type",
    hover_data=["city", "power_kw"],
    title="Duración de la sesión frente a energía consumida",
    labels={
        "session_duration_mins": "Duración (minutos)",
        "energy_consumed_kwh": "Energía consumida (kWh)",
        "connector_type": "Tipo de conector"
    }
)

st.plotly_chart(
    fig_relacion,
    use_container_width=True
)


# --------------------------------------------------
# 11. REVISIÓN DE POSIBLES ANOMALÍAS
# --------------------------------------------------

st.subheader("Registros que requieren revisión")

total_anomalias = int(
    df_filtrado["posible_anomalia"].sum()
)

porcentaje_anomalias = (
    total_anomalias / total_sesiones * 100
)

col1, col2 = st.columns(2)

col1.metric(
    "Registros con ratio superior a 1",
    f"{total_anomalias:,}"
)

col2.metric(
    "Porcentaje sobre sesiones filtradas",
    f"{porcentaje_anomalias:.2f}%"
)

st.caption(
    "Estos registros presentan una potencia media observada superior "
    "a la potencia nominal registrada. Se consideran casos que "
    "requieren revisión, no errores confirmados."
)

anomalias = df_filtrado[
    df_filtrado["posible_anomalia"]
]

st.dataframe(
    anomalias[
        [
            "timestamp",
            "city",
            "connector_type",
            "power_kw",
            "potencia_media_observada_kw",
            "ratio_potencia"
        ]
    ],
    use_container_width=True
)


# --------------------------------------------------
# 12. TABLA DE DATOS
# --------------------------------------------------

with st.expander("Consultar registros del análisis"):

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )

    st.download_button(
        label="Descargar datos filtrados en CSV",
        data=df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="sesiones_recarga_filtradas.csv",
        mime="text/csv"
    )


st.markdown("---")

st.caption(
    "Proyecto académico — Actividad 4 | "
    "Fuente: Global EV Charging Station Telemetry "
    "de Hugging Face."
)
