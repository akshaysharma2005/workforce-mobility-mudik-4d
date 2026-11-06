# 🗺️ Workforce Mobility & 4D Mudik Geospatial Flow Visualizer

[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![PyDeck](https://img.shields.io/badge/PyDeck-0.8+-00D2B8?style=for-the-badge&logo=uber&logoColor=white)](https://deckgl.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Geospatial Workforce Migration Analytics, 3D Arc Layers, and 4D Spatio-Temporal Flows across the Indonesian Archipelago during Eid Homecoming.**

---

## 🌟 Overview

The **Workforce Mobility & 4D Mudik Geospatial Flow Visualizer** tracks the temporal migration dynamics of corporate employees during Indonesia's annual Eid *Mudik* homecoming phenomenon. Analyzing daily geographic traces from Jakarta headquarters across 28 regencies and major islands, this platform delivers 3D PyDeck arc routes, demographic mobility spaces, individual traveler GPS timelines, and a 4D spatio-temporal migration playback.

```
                              ┌───────────────────────────────────┐
                              │     Workforce Location Logs       │
                              │    (2,600 Daily Check-in Pings)   │
                              └─────────────────┬─────────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
      ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐
      │  2D Migration Curve │        │   3D Deck.gl Arcs   │        │ 4D Spatio-Temporal  │
      │  & Department Rate  │        │   & Demographic Cube│        │ Migration Animation │
      └──────────┬──────────┘        └──────────┬──────────┘        └──────────┬──────────┘
                 │                              │                              │
                 ▼                              ▼                              ▼
     • Outflow & Return Waves        • 3D Arcs to Remote Islands    • Animated Day-by-Day Flow
     • Jabodetabek Retention %       • 3D Density Elevation Columns • Individual GPS Traces
     • Department Mobility Index     • Age × Duration × Distance    • Journey Distance Tracker
```

---

## ✨ Features & Visual Dimensions

### 📊 1. 2D Migration Dynamics
- **Homecoming & Return Curves**: Daily dual-axis bar and line charts depicting the percentage of active workforce displaced outside the capital.
- **Departmental Participation Rankings**: Comparing mobility behavior across Engineering, Product, Customer Service, and Operations divisions.

### 🗾 2. 3D Geospatial PyDeck / Deck.gl Arc Layer
- **3D Atmospheric Migration Arcs**: Rendered in hardware-accelerated WebGL connecting Jakarta HQ ($-6.18^\circ$, $106.82^\circ$) directly to provincial hometowns (Medan, Padang, Yogyakarta, Surabaya, Manado, Banda Aceh).
- **3D Elevation Density Columns**: Dynamic column height illustrating real-time employee concentration per city.

### 🌐 3. 3D Demographic Mobility Space
- **Tri-Axial Employee Space**:
  - **X-Axis**: Employee Age
  - **Y-Axis**: Days Away on Leave (Duration)
  - **Z-Axis**: Maximum Distance from Capital (km)
  - **Color**: Corporate Department

### ⏳ 4. 4D Spatio-Temporal Animation
- **4D Hyper-Dimensional Projection**:
  - **Dim 1 (X)**: Longitude
  - **Dim 2 (Y)**: Latitude
  - **Dim 3 (Z)**: Distance from Headquarters (km)
  - **Dim 4 (Color)**: Department
  - **Dim 5 (Size)**: Distance Traveled
  - **Dim 6 (Time / Frame Animation)**: Date Timeline (May 21 to June 15, 2019)
- Press **Play** to watch the workforce disperse across thousands of kilometers and systematically return.

### 👤 5. Individual Employee GPS Timeline Tracker
- Inspect individual employee travel itineraries, cumulative distance covered, and hometown destinations.

---

## 🚀 Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akshaysharma2005/workforce-mobility-mudik-4d.git
   cd workforce-mobility-mudik-4d
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```

4. Open `http://localhost:8501`.

---

## 👤 Author
- **M Akshay Sharma** ([@akshaysharma2005](https://github.com/akshaysharma2005))
- GitHub: [https://github.com/akshaysharma2005](https://github.com/akshaysharma2005)
