"""
Data preprocessing script to create processed_train.csv
"""

import pandas as pd
import numpy as np
from geopy.distance import geodesic
import os

print("=" * 80)
print("DATA PREPROCESSING PIPELINE")
print("=" * 80)

# Load raw data
print("\n[1/4] Loading raw data...")
try:
    df = pd.read_csv('data/raw/train.csv')
    print(f"✓ Loaded data: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)

# Clean and preprocess
print("\n[2/4] Cleaning and preprocessing...")
try:
    # Clean column names - make them consistent
    df.columns = df.columns.str.strip()
    
    # Convert datetime columns
    date_cols = ['order_date', 'Time_Orderd', 'Time_Order_picked']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Extract time features
    if 'order_date' in df.columns:
        df['day_of_week'] = df['order_date'].dt.day_name()
        df['month'] = df['order_date'].dt.month
        df['is_weekend'] = df['order_date'].dt.dayofweek.isin([5, 6]).astype(int)
    
    if 'Time_Orderd' in df.columns:
        df['order_hour'] = df['Time_Orderd'].dt.hour
        df['order_shift'] = pd.cut(df['order_hour'], 
                                    bins=[0, 6, 12, 18, 24], 
                                    labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                                    include_lowest=True)
    
    if 'Time_Order_picked' in df.columns:
        df['pickup_hour'] = df['Time_Order_picked'].dt.hour
    
    # Calculate delivery duration if both times exist
    if 'Time_Orderd' in df.columns and 'Time_Order_picked' in df.columns:
        df['delivery_duration_min'] = (df['Time_Order_picked'] - df['Time_Orderd']).dt.total_seconds() / 60
    
    # Clean weather conditions
    if 'Weatherconditions' in df.columns:
        df['Weatherconditions'] = df['Weatherconditions'].str.replace('conditions ', '', regex=False).str.strip()
    
    # Clean city names
    if 'City' in df.columns:
        df['City'] = df['City'].str.strip().replace({"Metropolitian": "Metropolitan"})
    
    # Calculate distance if coordinates exist
    coord_cols = ['Restaurant_latitude', 'Restaurant_longitude', 
                  'Delivery_location_latitude', 'Delivery_location_longitude']
    
    if all(col in df.columns for col in coord_cols):
        print("  - Calculating delivery distances...")
        def calculate_distance(row):
            try:
                restaurant = (row['Restaurant_latitude'], row['Restaurant_longitude'])
                delivery = (row['Delivery_location_latitude'], row['Delivery_location_longitude'])
                return geodesic(restaurant, delivery).km
            except:
                return np.nan
        
        df['delivery_distance_km'] = df.apply(calculate_distance, axis=1)
    
    # Create traffic level mapping
    if 'Road_traffic_density' in df.columns:
        traffic_map = {'Low': 1, 'Medium': 2, 'High': 3, 'Jam': 4}
        df['traffic_level'] = df['Road_traffic_density'].map(traffic_map)
    
    # Create rush hour indicator
    if 'order_hour' in df.columns:
        rush_hours = [9, 10, 11, 17, 18, 19, 20]
        df['is_rush_hour'] = df['order_hour'].isin(rush_hours).astype(int)
    
    # Clean target variable
    if 'Time_taken (min)' in df.columns:
        # Remove any non-numeric characters and convert to float
        df['time_taken_minutes'] = df['Time_taken (min)'].astype(str).str.extract('(\d+\.?\d*)')[0].astype(float)
    elif 'Time_taken(min)' in df.columns:
        # Remove any non-numeric characters and convert to float
        df['time_taken_minutes'] = df['Time_taken(min)'].astype(str).str.extract('(\d+\.?\d*)')[0].astype(float)
    
    print("✓ Preprocessing completed")
    print(f"  - New shape: {df.shape}")
    
except Exception as e:
    print(f"✗ Error during preprocessing: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Handle missing values
print("\n[3/4] Handling missing values...")
try:
    # Numeric columns - fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Categorical columns - fill with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
    
    print("✓ Missing values handled")
    print(f"  - Remaining missing values: {df.isnull().sum().sum()}")
    
except Exception as e:
    print(f"✗ Error handling missing values: {e}")
    exit(1)

# Save processed data
print("\n[4/4] Saving processed data...")
try:
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/processed_train.csv'
    df.to_csv(output_path, index=False)
    print(f"✓ Saved to: {output_path}")
    print(f"  - Final shape: {df.shape}")
    print(f"  - Columns: {len(df.columns)}")
    
except Exception as e:
    print(f"✗ Error saving data: {e}")
    exit(1)

print("\n" + "=" * 80)
print("PREPROCESSING COMPLETED SUCCESSFULLY!")
print("=" * 80)
