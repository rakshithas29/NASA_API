import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime


def create_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="rakshitha@2906",
        database="asteroids"
    )


predefined_queries = {
    "Count how many times each asteroid has approached Earth": """
        SELECT name, COUNT(*) AS approach_count
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        GROUP BY name
        ORDER BY approach_count DESC;
    """,
    "Average velocity of each asteroid over multiple approaches": """
        SELECT name, AVG(relative_velocity_kmph) AS avg_velocity
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        GROUP BY name
        ORDER BY avg_velocity DESC;
    """,
    "Top 10 fastest asteroids": """
        SELECT name, MAX(relative_velocity_kmph) AS max_velocity
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        GROUP BY name
        ORDER BY max_velocity DESC
        LIMIT 10;
    """,
    "Potentially hazardous asteroids with more than 3 approaches": """
        SELECT name, COUNT(*) AS count
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE is_potentially_hazardous_asteroid = TRUE
        GROUP BY name
        HAVING count > 3;
    """,
    "Month with most asteroid approaches": """
        SELECT MONTH(close_approach_date) AS month, COUNT(*) AS count
        FROM close_approach
        GROUP BY month
        ORDER BY count DESC
        LIMIT 1;
    """,
    "Asteroid with the fastest ever approach speed": """
        SELECT name, relative_velocity_kmph
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        ORDER BY relative_velocity_kmph DESC
        LIMIT 1;
    """,
    "Sort asteroids by maximum estimated diameter": """
        SELECT name, estimated_diameter_max_km
        FROM asteroids
        ORDER BY estimated_diameter_max_km DESC;
    """,
    "Asteroid getting closer over time (most approaches)": """
        SELECT name, COUNT(*) as approaches
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        GROUP BY name
        ORDER BY approaches DESC
        LIMIT 1;
    """,
    "Closest approach distance per asteroid": """
        SELECT name, close_approach_date, MIN(miss_distance_km) AS min_distance
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        GROUP BY name, close_approach_date
        ORDER BY min_distance ASC;
    """,
    "Asteroids with velocity > 50,000 km/h": """
        SELECT DISTINCT name, relative_velocity_kmph
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE relative_velocity_kmph > 50000;
    """,
    "Count approaches per month": """
        SELECT MONTH(close_approach_date) AS month, COUNT(*) AS approach_count
        FROM close_approach
        GROUP BY month
        ORDER BY month;
    """,
    "Asteroid with highest brightness (lowest magnitude)": """
        SELECT name, absolute_magnitude_h
        FROM asteroids
        ORDER BY absolute_magnitude_h ASC
        LIMIT 1;
    """,
    "Hazardous vs Non-Hazardous asteroid count": """
        SELECT is_potentially_hazardous_asteroid AS hazardous, COUNT(*) AS count
        FROM asteroids
        GROUP BY hazardous;
    """,
    "Asteroids that passed closer than Moon (<1 LD)": """
        SELECT name, close_approach_date, miss_distance_lunar
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE miss_distance_lunar < 1;
    """,
    "Asteroids within 0.05 AU": """
        SELECT name, close_approach_date, astronomical
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE astronomical < 0.05;
    """
}

custom_queries = {
    "Asteroids that only had 1 close approach": """
        SELECT name, COUNT(*) AS approach_count
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        GROUP BY name
        HAVING approach_count = 1;
    """,
    "Asteroids with max diameter > 1km": """
        SELECT name, estimated_diameter_max_km
        FROM asteroids
        WHERE estimated_diameter_max_km > 1;
    """,
    "Asteroids with avg miss distance < 100000 km": """
        SELECT name, AVG(miss_distance_km) AS avg_distance
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        GROUP BY name
        HAVING avg_distance < 100000;
    """,
    "Asteroids brighter than magnitude 18": """
        SELECT name, absolute_magnitude_h
        FROM asteroids
        WHERE absolute_magnitude_h < 18;
    """,
    "Asteroids with velocity between 20000-30000 km/h": """
        SELECT name, relative_velocity_kmph
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE relative_velocity_kmph BETWEEN 20000 AND 30000;
    """
}

-
st.set_page_config(page_title="🚀 NASA Asteroid Tracker", layout="wide")


st.sidebar.title("🛰 Asteroid Queries")
query_type = st.sidebar.radio("Select Type", ["Predefined", "Custom", "Filter"])

if query_type == "Predefined":
    selected_query = st.sidebar.selectbox("Choose a Predefined Query", list(predefined_queries.keys()))
    query = predefined_queries[selected_query]
elif query_type == "Custom":
    selected_query = st.sidebar.selectbox("Choose a Custom Query", list(custom_queries.keys()))
    query = custom_queries[selected_query]


st.markdown("<h2 style='text-align: center;'>🌌 NASA Asteroid Tracker</h2>", unsafe_allow_html=True)


if query_type == "Filter":
    st.subheader("🔎 Filter Asteroids")

    start_date = st.date_input("Start Date", datetime(2024, 1, 1))
    end_date = st.date_input("End Date", datetime(2024, 1, 8))
    min_mag, max_mag = st.slider("Absolute Magnitude (H)", 10.0, 35.0, (13.0, 32.0))
    min_dia, max_dia = st.slider("Estimated Diameter (km)", 0.0, 5.0, (0.0, 5.0))
    min_vel, max_vel = st.slider("Velocity (km/h)", 0.0, 200000.0, (1000.0, 100000.0))
    min_au, max_au = st.slider("Astronomical Distance (AU)", 0.0, 1.0, (0.0, 0.5))
    hazardous = st.selectbox("Potentially Hazardous?", ["All", "Yes", "No"])

    query = f"""
        SELECT a.name, a.absolute_magnitude_h, a.estimated_diameter_min_km,
               a.estimated_diameter_max_km, a.is_potentially_hazardous_asteroid,
               c.close_approach_date, c.relative_velocity_kmph, c.astronomical
        FROM asteroids a
        JOIN close_approach c ON a.id = c.neo_reference_id
        WHERE c.close_approach_date BETWEEN '{start_date}' AND '{end_date}'
          AND a.absolute_magnitude_h BETWEEN {min_mag} AND {max_mag}
          AND a.estimated_diameter_min_km >= {min_dia}
          AND a.estimated_diameter_max_km <= {max_dia}
          AND c.relative_velocity_kmph BETWEEN {min_vel} AND {max_vel}
          AND c.astronomical BETWEEN {min_au} AND {max_au}
    """
    if hazardous == "Yes":
        query += " AND a.is_potentially_hazardous_asteroid = 1"
    elif hazardous == "No":
        query += " AND a.is_potentially_hazardous_asteroid = 0"
    query += " ORDER BY c.close_approach_date;"


try:
    with create_connection() as conn:
        df = pd.read_sql(query, conn)
        st.subheader("📊 Results")
        st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Error running query: {e}")


