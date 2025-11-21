import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import sys
import os

# Add project root to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import utils
import project_config as config

# Set page config
st.set_page_config(
    page_title="Smart Logistics Delivery Prediction",
    page_icon="🚴",
    layout=config.PAGE_WIDTH,
    initial_sidebar_state=config.SIDEBAR_STATE
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #ff7f0e;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_resource
def load_data():
    try:
        # Use config path - pointing to processed_train.csv
        train_df = pd.read_csv(f"{config.DATA_PROCESSED_PATH}/processed_train.csv")
        return train_df
    except Exception as e:
        st.error(f"Could not load data from {config.DATA_RAW_PATH}/processed_train.csv. Error: {e}")
        return None

# Load model
@st.cache_resource
def load_model():
    return utils.load_model(config.MODEL_PATH)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "📊 Dataset Overview"

# Sidebar Navigation
st.sidebar.title("🚚 Smart Logistics Delivery Prediction")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["📊 Dataset Overview", "📈 EDA Analysis", "🎯 Prediction Dashboard"]
)

# Load data
df = load_data()
model = load_model()

if df is not None:
    # PAGE 1: DATASET OVERVIEW
    if page == "📊 Dataset Overview":
        st.markdown(
            '<p class="main-header">📊 Dataset Understanding & Cleaning</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sub-header">Comprehensive Overview of Smart Logistics Delivery Data</p>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Features", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        with col4:
            st.metric("Cities", df['City'].nunique() if 'City' in df.columns else "N/A")

        st.markdown("---")

        # Dataset Info Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Raw Data", "Data Info", "Statistics", "Missing Values", "Data Quality"])

        with tab1:
            st.markdown("### First 100 Records")
            st.dataframe(df.head(100), use_container_width=True)

        with tab2:
            st.markdown("### Data Structure")
            buffer = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null': df.count(),
                'Null Count': df.isnull().sum()
            })
            st.dataframe(buffer, use_container_width=True)

        with tab3:
            st.markdown("### Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)

        with tab4:
            st.markdown("### Missing Values Analysis")
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if len(missing) > 0:
                fig = px.bar(
                    x=missing.index,
                    y=missing.values,
                    title="Missing Values by Column",
                    labels={'x': 'Column', 'y': 'Count'},
                    color=missing.values,
                    color_continuous_scale="Reds"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("✅ No missing values detected!")

        with tab5:
            st.markdown("### Data Quality Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Completeness", f"{(1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100:.2f}%")
            with col2:
                st.metric("Duplicate Rows", len(df[df.duplicated()]))
            with col3:
                st.metric("Column Count", len(df.columns))

            st.markdown('<div class="insight-box"><strong>Data Cleaning Performed:</strong><br>✓ Removed duplicates<br>✓ Handled missing values (median/mode imputation)<br>✓ Standardized column names<br>✓ Validated geographic coordinates<br>✓ IQR-based outlier treatment</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔍 Column Description")

        descriptions = {
            'Delivery_person_Age': 'Age of the delivery person',
            'Delivery_person_Ratings': 'Rating given to the delivery person (1-5)',
            'Restaurant_latitude/longitude': 'Geographic coordinates of restaurant',
            'Delivery_location_latitude/longitude': 'Geographic coordinates of delivery location',
            'Weatherconditions': 'Weather during delivery (Sunny, Rainy, Cloudy, Fog)',
            'traffic_level': 'Traffic density level (1-4)',
            'Type_of_vehicle': 'Vehicle type (motorcycle, scooter, etc.)',
            'Type_of_order': 'Food type (Snack, Drink, Meal, Buffet)',
            'multiple_deliveries': 'Number of deliveries on the same route',
            'Festival': 'Whether delivery was during festival',
            'City': 'City name (Metropolitan, Urban, Semi-Urban)',
            'time_taken_minutes': 'Target: Actual delivery time in minutes',
            'delivery_distance_km': 'Calculated Haversine distance in km'
        }

        for col, desc in descriptions.items():
            if col in df.columns:
                st.markdown(f"- **{col}**: {desc}")

    # PAGE 2: EDA ANALYSIS
    elif page == "📈 EDA Analysis":
        st.markdown(
            '<p class="main-header">📈 Exploratory Data Analysis</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sub-header">Interactive Visualizations & Statistical Insights</p>', unsafe_allow_html=True)

        eda_tab1, eda_tab2, eda_tab3, eda_tab4, eda_tab5 = st.tabs(
            ["Distribution", "Relationships",
                "Time Analysis", "Geographic", "Correlations"]
        )

        with eda_tab1:
            st.markdown("### Feature Distributions")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Delivery Person Age")
                if 'Delivery_person_Age' in df.columns:
                    fig = px.histogram(df, x='Delivery_person_Age', nbins=30, title="Age Distribution",
                                       color_discrete_sequence=['#1f77b4'])
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### Delivery Person Ratings")
                if 'Delivery_person_Ratings' in df.columns:
                    fig = px.histogram(df, x='Delivery_person_Ratings', nbins=20, title="Rating Distribution",
                                       color_discrete_sequence=['#ff7f0e'])
                    st.plotly_chart(fig, use_container_width=True)

            col3, col4 = st.columns(2)

            with col3:
                st.markdown("#### Target: Delivery Time")
                if 'time_taken_minutes' in df.columns:
                    fig = px.histogram(df, x='time_taken_minutes', nbins=40, title="Delivery Time Distribution",
                                       color_discrete_sequence=['#2ca02c'])
                    st.plotly_chart(fig, use_container_width=True)

            with col4:
                st.markdown("#### Multiple Deliveries")
                if 'multiple_deliveries' in df.columns:
                    fig = px.bar(df['multiple_deliveries'].value_counts(), title="Multiple Deliveries Count",
                                 color_discrete_sequence=['#d62728'])
                    st.plotly_chart(fig, use_container_width=True)

        with eda_tab2:
            st.markdown("### Feature Relationships")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Distance vs Delivery Time")
                if 'delivery_distance_km' in df.columns and 'time_taken_minutes' in df.columns:
                    fig = px.scatter(df.head(1000), x='delivery_distance_km', y='time_taken_minutes',
                                     title="Distance vs Delivery Time",
                                     trendline="ols", color='Delivery_person_Ratings',
                                     color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Distance or time columns missing.")

            with col2:
                st.markdown("#### Rating vs Delivery Time")
                if 'Delivery_person_Ratings' in df.columns and 'time_taken_minutes' in df.columns:
                    fig = px.scatter(df, x='Delivery_person_Ratings', y='time_taken_minutes',
                                     title="Rating vs Delivery Time",
                                     color='Delivery_person_Age',
                                     size='multiple_deliveries' if 'multiple_deliveries' in df.columns else None,
                                     color_continuous_scale='Plasma')
                    st.plotly_chart(fig, use_container_width=True)

        with eda_tab3:
            st.markdown("### Time-Based Analysis")

            # Use pre-calculated order_hour
            if 'order_hour' in df.columns:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Delivery Time by Hour of Day")
                    hourly_stats = df.groupby('order_hour')[
                        'time_taken_minutes'].mean()
                    fig = px.line(hourly_stats, title="Average Delivery Time by Hour",
                                  labels={'value': 'Avg Time (min)', 'index': 'Hour'})
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown("#### Delivery Count by Hour")
                    hourly_count = df.groupby('order_hour').size()
                    fig = px.bar(hourly_count, title="Number of Deliveries by Hour",
                                 labels={'value': 'Count',
                                         'index': 'Hour'},
                                 color=hourly_count.values, color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("order_hour column missing.")

        with eda_tab4:
            st.markdown("### Geographic Analysis")

            if all(col in df.columns for col in ['Restaurant_latitude', 'Restaurant_longitude']):
                st.markdown("#### Restaurant Distribution Map")

                sample = df.dropna(
                    subset=['Restaurant_latitude', 'Restaurant_longitude']).head(500)
                
                import folium
                m = folium.Map(
                    location=[sample['Restaurant_latitude'].mean(), sample['Restaurant_longitude'].mean()],
                    zoom_start=6,
                    tiles='OpenStreetMap'
                )

                for idx, row in sample.iterrows():
                    folium.CircleMarker(
                        location=[row['Restaurant_latitude'], row['Restaurant_longitude']],
                        radius=3,
                        popup=f"Restaurant {idx}",
                        color='red',
                        fill=True,
                        fillOpacity=0.7
                    ).add_to(m)

                st_folium(m, width=700, height=500)

                st.markdown("#### City-wise Statistics")
                if 'City' in df.columns:
                    city_stats = df.groupby('City').agg({
                        'time_taken_minutes': ['mean', 'median', 'std', 'count']
                    }).round(2)
                    st.dataframe(city_stats, use_container_width=True)

        with eda_tab5:
            st.markdown("### Correlation Analysis")

            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr_matrix = numeric_df.corr()

                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.values,
                    texttemplate='%{text:.2f}',
                    textfont={"size": 10}
                ))
                fig.update_layout(
                    title="Feature Correlation Heatmap", height=700)
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### Strong Correlations with Delivery Time")
                if 'time_taken_minutes' in corr_matrix.columns:
                    time_corr = corr_matrix['time_taken_minutes'].sort_values(
                        ascending=False)[1:8]
                    fig = px.bar(time_corr, title="Top Features Correlated with Delivery Time",
                                 labels={'value': 'Correlation',
                                         'index': 'Feature'},
                                 color=time_corr.values, color_continuous_scale='RdBu',
                                 color_continuous_midpoint=0)
                    st.plotly_chart(fig, use_container_width=True)

    # PAGE 3: PREDICTION DASHBOARD
    else:  # Prediction Dashboard
        st.markdown(
            '<p class="main-header">🎯 Smart Logistics Prediction Dashboard</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sub-header">Real-time Delivery Time Estimation with Detailed Breakdown</p>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 2], gap="large")

        with col_left:
            st.markdown("### 🎛️ Delivery Parameters")
            st.markdown("---")

            # Delivery Person Info
            st.markdown("#### 👤 Delivery Person")
            delivery_age = st.slider("Age", 18, 70, 30)
            delivery_rating = st.slider("Rating (1-5)", 1.0, 5.0, 4.5, 0.1)

            st.markdown("#### 🛵 Vehicle & Conditions")
            vehicle_type = st.selectbox(
                "Vehicle Type", ["motorcycle", "scooter", "car", "bike"])
            weather = st.selectbox(
                "Weather", ["Sunny", "Cloudy", "Rainy", "Fog", "Stormy", "Sandstorms", "Windy"])
            
            # Map traffic to numeric
            traffic_map = {"Low": 1, "Medium": 2, "High": 3, "Jam": 4}
            traffic = st.select_slider(
                "Traffic Density", ["Low", "Medium", "High", "Jam"])
            traffic_numeric = traffic_map[traffic]

            st.markdown("#### 📍 Location & Time")
            distance_km = st.slider("Delivery Distance (km)", 0.5, 30.0, 5.0, 0.5)
            hour = st.slider("Order Hour (24h format)", 0, 23, 12)
            
            st.markdown("#### 📦 Order Details")
            order_type = st.selectbox(
                "Order Type", ["Snack", "Meal", "Drinks", "Buffet"])
            multiple_deliveries = st.slider("Multiple Deliveries", 0, 3, 0)
            festival = st.selectbox("Festival Day", ["No", "Yes"])
            city = st.selectbox("City", ["Urban", "Metropolitian", "Semi-Urban"])

            st.markdown("---")
            
            # Predict Button
            if st.button("🚀 Predict Delivery Time", type="primary", use_container_width=True):
                # Prepare input data
                input_data = {
                    'Delivery_person_Age': delivery_age,
                    'Delivery_person_Ratings': delivery_rating,
                    'delivery_distance_km': distance_km,
                    'traffic_level': traffic_numeric,
                    'multiple_deliveries': multiple_deliveries,
                    'order_hour': hour,
                    'Weatherconditions': weather,
                    'Type_of_vehicle': vehicle_type,
                    'Type_of_order': order_type,
                    'Festival': festival,
                    'City': city
                }
                
                # Make prediction
                predicted_time, components = utils.predict_delivery_time(
                    model, input_data, use_demo=(model is None)
                )
                
                # Store in session state for display in right column
                st.session_state['prediction'] = predicted_time
                st.session_state['components'] = components
                st.session_state['input_data'] = input_data

        with col_right:
            if 'prediction' in st.session_state:
                predicted_time = st.session_state['prediction']
                components = st.session_state['components']
                input_data = st.session_state['input_data']
                
                # Display Prediction Result
                st.markdown("### 📊 Prediction Results")
                
                # Main prediction with confidence interval
                forecast = utils.create_forecast_range(predicted_time)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Lower Estimate", f"{forecast['lower_bound']:.1f} min")
                with col2:
                    st.metric("Predicted Time", f"{predicted_time:.1f} min", 
                             help="Most likely delivery time")
                with col3:
                    st.metric("Upper Estimate", f"{forecast['upper_bound']:.1f} min")
                
                st.markdown("---")
                
                # Time Breakdown
                st.markdown("### ⏱️ Time Breakdown Analysis")
                
                # Prepare breakdown data
                breakdown_df = pd.DataFrame({
                    'Component': [k.replace('_', ' ').title() for k in components.keys()],
                    'Minutes': list(components.values())
                })
                breakdown_df = breakdown_df[breakdown_df['Minutes'] > 0].sort_values('Minutes', ascending=False)
                
                # Bar chart
                fig = px.bar(breakdown_df, x='Component', y='Minutes',
                            title="Time Contribution by Factor",
                            color='Minutes', color_continuous_scale='Blues')
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Pie chart
                fig_pie = px.pie(breakdown_df, values='Minutes', names='Component',
                                title="Time Distribution by Factor")
                st.plotly_chart(fig_pie, use_container_width=True)
                
                st.markdown("---")
                
                # Route Map Simulation
                st.markdown("### 🗺️ Delivery Route Visualization")
                
                # Generate random restaurant and delivery locations for demo
                np.random.seed(hash(str(input_data['delivery_distance_km'])) % 2**32)
                rest_lat = np.random.uniform(12.8, 13.1)
                rest_lon = np.random.uniform(77.5, 77.7)
                # Approximate lat/lon shift for distance
                # 1 deg lat ~ 111 km. 1 km ~ 0.009 deg
                shift = input_data['delivery_distance_km'] * 0.009
                del_lat = rest_lat + np.random.uniform(-shift, shift)
                del_lon = rest_lon + np.random.uniform(-shift, shift)
                
                # Use utils to render map
                m = utils.render_map(rest_lat, rest_lon, del_lat, del_lon)
                st_folium(m, width=700, height=500)
                
                st.markdown("---")
                
                # Key Insights
                st.markdown("### 💡 Key Insights")
                
                # Use utils to generate recommendations
                recommendations = utils.generate_delivery_recommendations(
                    input_data['delivery_distance_km'], 
                    input_data['traffic_level'], 
                    input_data['Weatherconditions'], 
                    input_data['order_hour'], 
                    input_data['Delivery_person_Ratings'], 
                    input_data['Festival'] == 'Yes'
                )
                
                if recommendations:
                    for rec in recommendations:
                        st.markdown(f'<div class="insight-box">{rec}</div>', unsafe_allow_html=True)
                else:
                    st.success("✅ Optimal conditions for on-time delivery!")
            else:
                st.info("👈 Enter delivery parameters and click 'Predict Delivery Time' to see results")

else:
    st.error("Unable to load application. Please check data file.")
