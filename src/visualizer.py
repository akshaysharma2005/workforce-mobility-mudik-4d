import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk
import pandas as pd
import numpy as np

DIV_COLORS = {
    "Data Engineer": "#38bdf8",
    "Software Engineer": "#10b981",
    "Product": "#f59e0b",
    "Business Development": "#a855f7",
    "Customer Service": "#f43f5e",
    "Marketing": "#ec4899",
    "Finance": "#64748b"
}

def build_2d_daily_migration_curves(df):
    """Daily headcount outside Jabodetabek over the holiday timeline."""
    daily = df.groupby(["tanggal_str", "is_mudik"]).size().unstack(fill_value=0).reset_index()
    daily.columns = ["Date", "In_Jabodetabek", "On_Mudik"]
    daily["Mudik_Pct"] = (daily["On_Mudik"] / (daily["In_Jabodetabek"] + daily["On_Mudik"])) * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily["Date"],
        y=daily["In_Jabodetabek"],
        name="Stationed in Jakarta HQ Area",
        marker_color="#334155"
    ))
    fig.add_trace(go.Bar(
        x=daily["Date"],
        y=daily["On_Mudik"],
        name="Migrated to Hometown (Mudik)",
        marker_color="#10b981"
    ))
    fig.add_trace(go.Scatter(
        x=daily["Date"],
        y=daily["Mudik_Pct"],
        name="% Workforce Away",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=3)
    ))

    fig.update_layout(
        title="Daily Workforce Homecoming Migration & Return Curve",
        barmode="stack",
        xaxis_title="Calendar Date (May 21 - June 15, 2019)",
        yaxis=dict(title="Active Employees", gridcolor="rgba(255,255,255,0.1)"),
        yaxis2=dict(title="% Outside Jakarta", overlaying="y", side="right", range=[0, 100], showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        height=400,
        margin=dict(l=40, r=40, t=40, b=50)
    )
    return fig

def build_division_participation(emp_stats):
    """Mudik participation rate by corporate department."""
    div_agg = emp_stats.groupby("divisi").agg(
        Total=("id", "count"),
        Mudik=("days_mudik", lambda x: (x > 0).sum())
    ).reset_index()
    div_agg["Mudik_Rate"] = (div_agg["Mudik"] / div_agg["Total"]) * 100

    fig = px.bar(
        div_agg.sort_values(by="Mudik_Rate", ascending=False),
        x="divisi",
        y="Mudik_Rate",
        color="divisi",
        color_discrete_map=DIV_COLORS,
        text_auto=".1f",
        labels={"divisi": "Department", "Mudik_Rate": "% Participating in Mudik"}
    )
    fig.update_layout(
        title="Departmental Mudik Departure Rates",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        showlegend=False,
        height=380,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def build_3d_deckgl_migration_map(df_selected_date):
    """
    3D PyDeck Arc & Column Layer Map:
    Arcs originate from Jakarta HQ (-6.18, 106.82) to active employee destinations.
    Columns elevate at each destination based on employee density.
    """
    dest_counts = df_selected_date[df_selected_date["is_mudik"]].groupby(["lokasi_dominan", "lat", "lon"]).size().reset_index(name="count")
    
    # 3D Arc Layer
    arc_data = []
    for _, row in dest_counts.iterrows():
        arc_data.append({
            "source": [106.8227, -6.1818], # Jakarta
            "target": [row["lon"], row["lat"]],
            "name": row["lokasi_dominan"],
            "count": row["count"]
        })
        
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=arc_data,
        get_source_position="source",
        get_target_position="target",
        get_source_color=[56, 189, 248, 200], # Cyan glow
        get_target_color=[244, 63, 94, 220],   # Red destination
        get_width=3,
        pickable=True,
        auto_highlight=True
    )

    column_layer = pdk.Layer(
        "ColumnLayer",
        data=dest_counts,
        get_position=["lon", "lat"],
        get_elevation="count * 25000",
        elevation_scale=1,
        radius=18000,
        get_fill_color=[245, 158, 11, 200], # Amber
        pickable=True,
        auto_highlight=True
    )

    view_state = pdk.ViewState(
        latitude=-3.0,
        longitude=110.0,
        zoom=4.5,
        pitch=45,
        bearing=0
    )

    r = pdk.Deck(
        layers=[arc_layer, column_layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={"text": "{name}\nActive Staff: {count}"}
    )
    return r

def build_3d_demographic_space(emp_stats):
    """
    3D Demographic Mobility Space:
    X: Employee Age
    Y: Days on Mudik (Duration)
    Z: Max Distance Traveled (km)
    Color: Department
    """
    fig = px.scatter_3d(
        emp_stats,
        x="umur",
        y="days_mudik",
        z="max_distance",
        color="divisi",
        hover_name="top_dest",
        hover_data={"id": True, "jenis_kelamin": True, "umur": True, "days_mudik": True, "max_distance": ":.0f km"},
        color_discrete_map=DIV_COLORS,
        labels={
            "umur": "Employee Age",
            "days_mudik": "Days Away (Mudik Duration)",
            "max_distance": "Max Distance from Jakarta (km)"
        }
    )

    fig.update_layout(
        title="3D Workforce Mobility Space (Age × Days Away × Distance from Capital)",
        scene=dict(
            xaxis=dict(title="Employee Age", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Days Away", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(title="Distance (km)", backgroundcolor="#0f172a", gridcolor="rgba(255,255,255,0.1)"),
            camera=dict(eye=dict(x=1.7, y=1.7, z=1.2))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=620,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def build_4d_spatiotemporal_scatter(df):
    """
    4D Spatio-Temporal Animation:
    - Dim 1 (X): Longitude
    - Dim 2 (Y): Latitude
    - Dim 3 (Z): Distance from Jakarta (km)
    - Dim 4 (Color): Division
    - Dim 5 (Size): Distance
    - Animation Frame: Date String (May 21 -> June 15)
    """
    df_anim = df.sort_values(by="tanggal_parsed").copy()

    fig = px.scatter_3d(
        df_anim,
        x="lon",
        y="lat",
        z="distance_km",
        color="divisi",
        size="distance_km",
        size_max=16,
        animation_frame="tanggal_str",
        animation_group="id",
        hover_name="lokasi_dominan",
        hover_data={"divisi": True, "distance_km": True, "umur": True},
        color_discrete_map=DIV_COLORS,
        range_x=[94, 126],
        range_y=[-9, 6],
        range_z=[0, 2200],
        labels={"lon": "Longitude", "lat": "Latitude", "distance_km": "Distance (km)"}
    )

    fig.update_layout(
        title="4D Geospatial Mudik Flow Animation (Archipelago Coordinates × Elevation Distance × Date)",
        scene=dict(
            xaxis=dict(title="Longitude", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(title="Latitude", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)"),
            zaxis=dict(title="Distance (km)", backgroundcolor="#0b132b", gridcolor="rgba(255,255,255,0.1)"),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.3))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=620,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig
