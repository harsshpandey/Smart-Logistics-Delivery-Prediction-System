"""
Alternative entry point for Smart Logistics Delivery Prediction
This can be used instead of streamlit_app.py

Usage:
    streamlit run app/main.py
"""

import streamlit as st
from streamlit_app import *


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Smart Logistics Delivery Prediction",
        page_icon="🚴",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.info("""
    👋 Welcome to **Smart Logistics Delivery Prediction System**
    
    This application predicts delivery times based on real-world conditions.
    Navigate using the sidebar to explore different sections:
    
    - 📊 **Dataset Overview**: Understand the data structure and quality
    - 📈 **EDA Analysis**: Explore patterns and relationships in the data
    - 🎯 **Prediction Dashboard**: Make real-time delivery predictions
    """)


if __name__ == "__main__":
    main()
