import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2.0)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def load_mobility_data(csv_path="data/mudik_tracking.csv"):
    df = pd.read_csv(csv_path)
    df["tanggal_parsed"] = pd.to_datetime(df["tanggal_parsed"])
    df["tanggal_str"] = df["tanggal_parsed"].dt.strftime("%Y-%m-%d")
    
    # Distance from Jakarta HQ
    df["distance_km"] = haversine(df["origin_lat"], df["origin_lon"], df["lat"], df["lon"]).round(1)
    
    # Employee summary statistics
    emp_stats = df.groupby(["id", "jenis_kelamin", "divisi", "umur"]).agg(
        days_mudik=("is_mudik", "sum"),
        max_distance=("distance_km", "max"),
        top_dest=("lokasi_dominan", lambda x: x[df.loc[x.index, "is_mudik"]].mode().iloc[0] if df.loc[x.index, "is_mudik"].any() else "Jabodetabek")
    ).reset_index()
    
    return df, emp_stats
