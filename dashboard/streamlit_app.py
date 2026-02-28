import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Pertanian", layout="wide")
st.title("Dashboard Smart Farming")
st.write("Monitoring Sensor IoT - Tugas 2")

try:
    df = pd.read_csv("outputs/cleaned_data.csv")
except:
    st.error("Data tidak terbaca. Cek outputs/cleaned_data.csv belum?")
    st.stop()

kelembaban_sekarang = df['humidity'].iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.markdown("Alert System")
    batas_aman = 40.0
    
    if kelembaban_sekarang < batas_aman:
        st.error(f"WASPADA: Kelembaban tanah hanya {kelembaban_sekarang}%. Tanah kering, nyalakan pompa air")
    else:
        st.success(f"AMAN: Kelembaban tanah aman di angka {kelembaban_sekarang}%.")
        
with col2:
    st.markdown("Gauge Kelembaban")
    fig1 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = kelembaban_sekarang,
        title = {'text': "Kelembaban (%)"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "dodgerblue"},
            'steps': [
                {'range': [0, 40], 'color': "tomato"},
                {'range': [40, 70], 'color': "gold"},
                {'range': [70, 100], 'color': "limegreen"}
            ]
        }
    ))
    st.plotly_chart(fig1, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.markdown("Tren Sensor")
    data_tren = df[['temp', 'humidity']].tail(100).reset_index(drop=True)
    st.line_chart(data_tren)

with col4:
    st.markdown("Heatmap Korelasi")
    fig2, ax = plt.subplots()
    kolom_angka = df[['MOI', 'temp', 'humidity', 'result']]
    sns.heatmap(kolom_angka.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig2)
