import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_RAW_PATH = os.path.join(BASE_DIR, "data", "processed")
DATA_PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

# Model Configuration
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'final_model.joblib')
MODEL_TYPE = 'xgboost'  # Default model type
RANDOM_STATE = 42

# Feature Configuration
NUMERIC_FEATURES = [
    'Delivery_person_Age', 
    'Delivery_person_Ratings', 
    'delivery_distance_km',
    'traffic_level',
    'multiple_deliveries',
    'order_hour',
    'pickup_hour',
    'delivery_duration_min',
    'month'
]

CATEGORICAL_FEATURES = [
    'Weatherconditions', 
    'Type_of_order', 
    'Type_of_vehicle', 
    'Festival', 
    'City',
    'day_of_week',
    'is_weekend',
    'is_rush_hour',
    'order_shift'
]

TARGET_FEATURE = 'time_taken_minutes'

# Prediction Constraints
MIN_DELIVERY_TIME = 5   # minutes
MAX_DELIVERY_TIME = 120 # minutes
MIN_DISTANCE = 0.5
MAX_DISTANCE = 30.0

# UI Configuration
APP_TITLE = "Smart Logistics: Zomato Delivery Prediction"
APP_ICON = "🚚"
THEME_COLOR = "#FF4B4B"
PAGE_WIDTH = "wide"
SIDEBAR_STATE = "expanded"

# Delivery Time Factors (for demo/heuristic fallback)
BASE_TIME = 15
TIME_PER_KM = 2.5
RUSH_HOUR_HOURS = [9, 10, 11, 17, 18, 19, 20]

# Impact Factors (multipliers)
WEATHER_IMPACT = {
    'Sunny': 1.0,
    'Stormy': 1.4,
    'Sandstorms': 1.3,
    'Cloudy': 1.1,
    'Fog': 1.2,
    'Windy': 1.1
}

TRAFFIC_IMPACT = {
    'Low': 1.0,
    'Medium': 1.2,
    'High': 1.4,
    'Jam': 1.8
}

# Geographic Bounds (approximate for India)
LAT_MIN, LAT_MAX = 8.0, 37.0
LON_MIN, LON_MAX = 68.0, 97.0

# Logging
LOG_FILE = "app.log"
LOG_LEVEL = "INFO"
