import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_mobility_data
from src.visualizer import (
    build_2d_daily_migration_curves,
    build_division_participation,
    build_3d_deckgl_migration_map,
    build_3d_demographic_space,
    build_4d_spatiotemporal_scatter,
    DIV_COLORS
)

st.set_page_config(
    page_title="Workforce Mobility & 4D Mudik Geospatial Flow",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom modern CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }
    
    .mobility-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_mobility_data("data/mudik_tracking.csv")

df, emp_stats = get_data()

# Sidebar
st.sidebar.title("🗺️ Mudik Telemetry")
st.sidebar.markdown("Geospatial Workforce Migration, 3D Arc Layers & 4D Spatio-Temporal Mobility.")

div_filter = st.sidebar.multiselect("Department", options=sorted(df["divisi"].unique()), default=sorted(df["divisi"].unique()))
gender_filter = st.sidebar.multiselect("Gender", options=sorted(df["jenis_kelamin"].unique()), default=sorted(df["jenis_kelamin"].unique()))

filtered_df = df[(df["divisi"].isin(div_filter)) & (df["jenis_kelamin"].isin(gender_filter))]
filtered_emp = emp_stats[(emp_stats["divisi"].isin(div_filter)) & (emp_stats["jenis_kelamin"].isin(gender_filter))]

# Header KPIs
col_title, col_kpis = st.columns([2, 3])
with col_title:
    st.title("Workforce Mudik Mobility AI")
    st.caption("3D geospatial migration arcs, archipelago mobility tracking, and 4D spatio-temporal homecoming flows.")

total_staff = len(filtered_emp)
mudik_participated = (filtered_emp["days_mudik"] > 0).sum()
mudik_pct = (mudik_participated / max(1, total_staff)) * 100
avg_dist = filtered_emp[filtered_emp["days_mudik"] > 0]["max_distance"].mean() if mudik_participated > 0 else 0
max_dist = filtered_emp["max_distance"].max() if total_staff > 0 else 0

with col_kpis:
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="mobility-card">
            <span style="color: #94a3b8; font-size: 11px;">TRACKED STAFF</span>
            <h3 style="margin: 0; color: #38bdf8;">{total_staff}</h3>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="mobility-card">
            <span style="color: #94a3b8; font-size: 11px;">MUDIK PARTICIPATION</span>
            <h3 style="margin: 0; color: #10b981;">{mudik_pct:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="mobility-card">
            <span style="color: #94a3b8; font-size: 11px;">AVG DISTANCE</span>
            <h3 style="margin: 0; color: #f59e0b;">{avg_dist:.0f} km</h3>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="mobility-card">
            <span style="color: #94a3b8; font-size: 11px;">MAX TRAVEL RADIUS</span>
            <h3 style="margin: 0; color: #f43f5e;">{max_dist:.0f} km</h3>
        </div>
        """, unsafe_allow_html=True)

# Tabs
tab_2d, tab_3d_map, tab_3d_demo, tab_4d, tab_emp = st.tabs([
    "📊 2D Migration Dynamics",
    "🗾 3D Geospatial Arc Layer",
    "🌐 3D Demographic Space",
    "⏳ 4D Spatio-Temporal Animation",
    "👤 Individual Staff Tracker"
])

# TAB 1: 2D
with tab_2d:
    st.plotly_chart(build_2d_daily_migration_curves(filtered_df), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(build_division_participation(filtered_emp), use_container_width=True)
    with col2:
        st.markdown("#### Top Mudik Destinations Outside Greater Jakarta")
        top_dest = filtered_df[filtered_df["is_mudik"]]["lokasi_dominan"].value_counts().head(8).reset_index()
        top_dest.columns = ["City / Regency", "Tracking Check-ins"]
        t_fig = px.bar(top_dest, x="Tracking Check-ins", y="City / Regency", orientation="h", color="Tracking Check-ins", color_continuous_scale="Teal")
        t_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"))
        st.plotly_chart(t_fig, use_container_width=True)

# TAB 2: 3D MAP
with tab_3d_map:
    st.subheader("3D Indonesian Archipelago Migration Arc & Density Columns")
    st.markdown("Curved 3D spatial arcs connect Jakarta Headquarters to employee homecoming destinations across Java, Sumatra, and Sulawesi. Column heights mark regional headcount.")
    
    dates_available = sorted(df["tanggal_str"].unique())
    sel_date = st.select_slider("Select Tracking Date", options=dates_available, value=dates_available[15])
    
    df_date = df[df["tanggal_str"] == sel_date]
    deck_map = build_3d_deckgl_migration_map(df_date)
    st.pydeck_chart(deck_map)

# TAB 3: 3D DEMO
with tab_3d_demo:
    st.subheader("3D Workforce Mobility Demographic Space")
    st.markdown("Visualizes employees in 3D: Age × Days on Mudik × Max Travel Distance from Capital.")
    st.plotly_chart(build_3d_demographic_space(filtered_emp), use_container_width=True)

# TAB 4: 4D
with tab_4d:
    st.subheader("4D Spatio-Temporal Mudik Flow Animation")
    st.markdown("Press **Play** to observe 100 employees travel across Indonesia from Jakarta HQ, scatter across distant provinces for Eid celebrations, and journey back home.")
    st.plotly_chart(build_4d_spatiotemporal_scatter(filtered_df), use_container_width=True)

# TAB 5: INDIVIDUAL TRACKER
with tab_emp:
    st.subheader("👤 Individual Employee Mudik Itinerary & GPS Trace")
    
    sel_id = st.selectbox("Select Employee ID", options=sorted(df["id"].unique()), index=1)
    emp_record = emp_stats[emp_stats["id"] == sel_id].iloc[0]
    emp_trace = df[df["id"] == sel_id].sort_values(by="tanggal_parsed")
    
    ec1, ec2, ec3, ec4 = st.columns(4)
    with ec1:
        st.markdown(f"**Department**: `{emp_record['divisi']}`")
    with ec2:
        st.markdown(f"**Age / Gender**: `{emp_record['umur']} yrs / {emp_record['jenis_kelamin']}`")
    with ec3:
        st.markdown(f"**Days Away**: `{emp_record['days_mudik']} days`")
    with ec4:
        st.markdown(f"**Furthest Distance**: `{emp_record['max_distance']} km ({emp_record['top_dest']})`")
        
    trace_fig = px.line(
        emp_trace,
        x="tanggal_str",
        y="distance_km",
        markers=True,
        text="lokasi_dominan",
        labels={"tanggal_str": "Date", "distance_km": "Distance from Jakarta (km)"},
        title=f"Employee #{sel_id} Travel Distance Timeline"
    )
    trace_fig.update_traces(textposition="top center", line=dict(color="#38bdf8", width=3))
    trace_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#f8fafc"), height=400)
    st.plotly_chart(trace_fig, use_container_width=True)
