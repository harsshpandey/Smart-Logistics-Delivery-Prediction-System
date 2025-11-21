"""
Utility functions for Smart Logistics Delivery Prediction
"""

import numpy as np
import pandas as pd
from geopy.distance import geodesic
import joblib
from typing import Dict, Tuple, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate Haversine distance between two geographic points.

    Args:
        lat1, lon1: Latitude and longitude of point 1
        lat2, lon2: Latitude and longitude of point 2

    Returns:
        Distance in kilometers
    """
    try:
        return geodesic((lat1, lon1), (lat2, lon2)).km
    except Exception as e:
        logger.error(f"Error calculating distance: {e}")
        return 0


def load_model(model_path: str) -> Any:
    """
    Load trained model from disk.

    Args:
        model_path: Path to model file

    Returns:
        Loaded model or None if failed
    """
    try:
        model = joblib.load(model_path)
        logger.info(f"Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        logger.warning(f"Model file not found at {model_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None


def save_model(model: Any, model_path: str) -> bool:
    """
    Save trained model to disk.

    Args:
        model: Model to save
        model_path: Path to save model

    Returns:
        True if successful, False otherwise
    """
    try:
        joblib.dump(model, model_path)
        logger.info(f"Model saved successfully to {model_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        return False


def prepare_prediction_input(params: Dict) -> Dict:
    """
    Prepare input data for model prediction.

    Args:
        params: Dictionary of input parameters

    Returns:
        Processed input dictionary
    """
    processed_params = {}

    # Ensure all values are in correct format
    numeric_params = [
        'Delivery_person_Age', 'Delivery_person_Ratings',
        'delivery_distance_km', 'traffic_level', 'multiple_deliveries',
        'hour', 'is_festival'
    ]

    for param in numeric_params:
        if param in params:
            processed_params[param] = float(params[param])

    return processed_params


def calculate_time_components(
    distance_km: float,
    traffic_level: int,
    weather: str,
    hour: int,
    age: float,
    rating: float,
    is_festival: bool,
    multiple_deliveries: int
) -> Dict[str, float]:
    """
    Calculate delivery time components for breakdown analysis.

    Args:
        Various delivery parameters

    Returns:
        Dictionary with time component breakdown
    """
    base_time = 10
    distance_time = distance_km * 2
    traffic_factor = traffic_level * 3

    weather_factors = {
        "Sunny": 0,
        "Cloudy": 2,
        "Rainy": 5,
        "Fog": 8,
        "Stormy": 10,
        "Sandstorms": 12
    }
    weather_factor = weather_factors.get(weather, 0)

    age_factor = max(0, -0.1 * age + 5)
    rating_factor = max(0, -1 * rating)
    festival_factor = 5 if is_festival else 0

    rush_hours = [7, 8, 9, 11, 12, 13, 18, 19, 20]
    rush_hour_factor = 3 if hour in rush_hours else 0

    multiple_factor = multiple_deliveries * 2

    components = {
        'base_time': base_time,
        'distance_time': distance_time,
        'traffic_factor': traffic_factor,
        'weather_factor': weather_factor,
        'age_factor': age_factor,
        'rating_factor': rating_factor,
        'festival_factor': festival_factor,
        'rush_hour_factor': rush_hour_factor,
        'multiple_factor': multiple_factor
    }

    return components


def predict_delivery_time(
    model: Any,
    params: Dict,
    use_demo: bool = False
) -> Tuple[float, Dict[str, float]]:
    """
    Predict delivery time using model or demo calculation.

    Args:
        model: Trained model object
        params: Input parameters
        use_demo: Use demo calculation if True

    Returns:
        Tuple of (predicted_time, components_breakdown)
    """
    # Try using model if available and not in demo mode
    if model is not None and not use_demo:
        try:
            # Prepare input dataframe
            input_df = prepare_prediction_input(params)
            
            # Predict
            predicted_time = float(model.predict(input_df)[0])
            
            # For components, we still use heuristic as model doesn't give breakdown
            # But we scale them to match model prediction
            heuristic_time, components = _calculate_heuristic_time(params)
            
            # Scale components
            if heuristic_time > 0:
                scale_factor = predicted_time / heuristic_time
                components = {k: v * scale_factor for k, v in components.items()}
            
            return predicted_time, components
        except Exception as e:
            print(f"Model prediction failed: {e}. Falling back to demo mode.")
            # Fallback to demo
            pass

    # Demo/Heuristic mode
    return _calculate_heuristic_time(params)


def _calculate_heuristic_time(params: Dict) -> Tuple[float, Dict[str, float]]:
    """Internal function for heuristic calculation"""
    components = calculate_time_components(
        distance_km=params.get('delivery_distance_km', 5),
        traffic_level=params.get('traffic_level', 2),
        weather=params.get('Weatherconditions', 'Sunny'),
        hour=params.get('order_hour', 12),
        age=params.get('Delivery_person_Age', 30),
        rating=params.get('Delivery_person_Ratings', 4.5),
        is_festival=params.get('Festival', 'No') == 'Yes',
        multiple_deliveries=params.get('multiple_deliveries', 1)
    )

    total_time = sum(v for v in components.values() if v > 0)
    predicted_time = max(5, total_time)
    
    return predicted_time, components


def generate_delivery_recommendations(
    distance_km: float,
    traffic_level: int,
    weather: str,
    hour: int,
    rating: float,
    is_festival: bool
) -> list:
    """
    Generate recommendations based on delivery parameters.

    Args:
        Various delivery parameters

    Returns:
        List of recommendation strings
    """
    recommendations = []

    # Traffic recommendations
    traffic_map = {1: "Low", 2: "Medium", 3: "High", 4: "Jam"}
    if traffic_level >= 3:
        recommendations.append(
            f"🚨 {traffic_map.get(traffic_level, 'Unknown')} traffic detected! "
            "Consider alternative routes or time adjustments."
        )

    # Weather recommendations
    adverse_weather = ["Rainy", "Stormy", "Sandstorms"]
    if weather in adverse_weather:
        recommendations.append(
            f"⛈️ {weather} conditions detected. Delivery may experience delays. "
            "Ensure safety precautions."
        )

    # Rush hour recommendations
    rush_hours = [11, 12, 13, 18, 19, 20]
    if hour in rush_hours:
        recommendations.append(
            "⏰ Rush hour detected. Higher demand expected. "
            "Plan for potential delays."
        )

    # Festival recommendations
    if is_festival:
        recommendations.append(
            "🎉 Festival day detected. Expect higher delivery demand and longer times."
        )

    # Distance recommendations
    if distance_km > 15:
        recommendations.append(
            f"📍 Long-distance delivery ({distance_km:.1f} km). "
            "Time estimates may vary based on route conditions."
        )

    # Rating-based recommendations
    if rating >= 4.5:
        recommendations.append(
            f"⭐ High-rated delivery person ({rating:.1f}/5). "
            "Expect reliable and timely delivery!"
        )
    elif rating < 3.5:
        recommendations.append(
            f"⚠️ Delivery person has lower ratings ({rating:.1f}/5). "
            "Consider the impact on delivery reliability."
        )

    # Optimal conditions
    if (traffic_level <= 2 and weather == "Sunny" and
            hour not in rush_hours and not is_festival and distance_km <= 5):
        recommendations.append(
            "✅ Optimal conditions for on-time delivery!"
        )

    return recommendations


def validate_input_parameters(params: Dict) -> Tuple[bool, str]:
    """
    Validate input parameters for prediction.

    Args:
        params: Input parameters dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_params = [
        'Delivery_person_Age', 'Delivery_person_Ratings',
        'distance_km', 'traffic_level', 'hour'
    ]

    for param in required_params:
        if param not in params:
            return False, f"Missing parameter: {param}"

    # Validate ranges
    if not (18 <= params['Delivery_person_Age'] <= 70):
        return False, "Delivery person age must be between 18 and 70"

    if not (1.0 <= params['Delivery_person_Ratings'] <= 5.0):
        return False, "Ratings must be between 1.0 and 5.0"

    if not (0 <= params['distance_km'] <= 30):
        return False, "Distance must be between 0 and 30 km"

    if not (0 <= params['hour'] <= 23):
        return False, "Hour must be between 0 and 23"

    return True, ""


def create_forecast_range(
    predicted_time: float,
    confidence: float = 0.85
) -> Dict[str, float]:
    """
    Create confidence interval for prediction.

    Args:
        predicted_time: Point prediction
        confidence: Confidence level (0-1)

    Returns:
        Dictionary with lower, point, and upper estimates
    """
    # Estimate margin of error based on confidence
    margin = predicted_time * (1 - confidence) * 0.5

    return {
        'lower_bound': max(5, predicted_time - margin),
        'point_estimate': predicted_time,
        'upper_bound': predicted_time + margin,
        'confidence': confidence
    }


def render_map(rest_lat: float, rest_lon: float, del_lat: float, del_lon: float) -> Any:
    """
    Render a Folium map with restaurant and delivery locations.

    Args:
        rest_lat, rest_lon: Restaurant coordinates
        del_lat, del_lon: Delivery coordinates

    Returns:
        Folium Map object
    """
    import folium

    # Calculate center
    center_lat = (rest_lat + del_lat) / 2
    center_lon = (rest_lon + del_lon) / 2

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles='OpenStreetMap'
    )

    # Restaurant marker
    folium.Marker(
        location=[rest_lat, rest_lon],
        popup="🍽️ Restaurant",
        icon=folium.Icon(color='red', icon='cutlery'),
        tooltip="Restaurant Location"
    ).add_to(m)

    # Delivery location marker
    folium.Marker(
        location=[del_lat, del_lon],
        popup="📦 Delivery Location",
        icon=folium.Icon(color='blue', icon='home'),
        tooltip="Delivery Location"
    ).add_to(m)

    # Route line
    folium.PolyLine(
        locations=[[rest_lat, rest_lon], [del_lat, del_lon]],
        color='green',
        weight=3,
        opacity=0.7,
        popup="Direct Route"
    ).add_to(m)

    return m
