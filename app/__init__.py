"""
Smart Logistics Delivery Prediction Application
A comprehensive ML system for predicting food delivery times
"""

__version__ = "1.0.0"
__author__ = "Smart Logistics Team"
__title__ = "Smart Logistics Delivery Prediction"

from .utils import (
    haversine_distance,
    load_model,
    save_model,
    calculate_time_components,
    predict_delivery_time,
    generate_delivery_recommendations,
    validate_input_parameters
)

__all__ = [
    'haversine_distance',
    'load_model',
    'save_model',
    'calculate_time_components',
    'predict_delivery_time',
    'generate_delivery_recommendations',
    'validate_input_parameters'
]
