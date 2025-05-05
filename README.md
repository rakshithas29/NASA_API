# 🚀 NASA NEO Tracker

A Streamlit web application that fetches Near-Earth Object (NEO) data from NASA's API, stores it in a MySQL database, and visualizes insights through interactive streamlit.
---
## 🌟 Features

- Fetches NASA NEO data from the public API  
- Stores data in a MySQL database  
- Displays 15 predefined and 5–10 custom SQL queries  
- Interactive filtering by date, velocity, distance, and hazard status
---

## 🛠️ Installation
### 1. Clone the repository

```bash
git clone https://github.com/yourusername/nasa-neo-tracker.git
cd nasa-neo-tracker
# 2.Install dependencies
pip install -r requirements.txt
# 3.Run the app
Run the app
▶️ Usage
•	Select a date range to fetch NEO data
•	View predefined SQL queries from the sidebar
•	Create and run custom SQL queries using filters
•	Explore insights via interactive tables and charts
📁 Project Structure
•	app.py             # Main Streamlit app
•	data_loader.py     # Fetches and loads NEO data
•	queries.py         # Predefined and custom SQL queries
•	requirements.txt   # Python dependencies
•	README.md          # Project documentation
🗃️ Database Schema
Tables
asteroids
•	id (Primary Key)
•	name
•	absolute_magnitude
•	estimated_diameter_min
•	estimated_diameter_max
•	is_potentially_hazardous
close_approach
•	id (Primary Key)
•	asteroid_id (Foreign Key to asteroids)
•	close_approach_date
•	relative_velocity_km_s
•	miss_distance_km
•	orbiting_body

