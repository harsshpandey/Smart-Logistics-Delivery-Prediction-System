"""
Testing utilities for Smart Logistics Delivery Prediction
Unit tests and validation functions
"""

import pandas as pd
import numpy as np
from app.utils import (
    validate_input_parameters,
    calculate_time_components,
    predict_delivery_time,
    generate_delivery_recommendations,
    create_forecast_range
)


def test_validate_input_parameters():
    """Test input parameter validation"""

    # Valid input
    valid_params = {
        'Delivery_person_Age': 30,
        'Delivery_person_Ratings': 4.5,
        'distance_km': 5.0,
        'traffic_level': 2,
        'hour': 12
    }
    is_valid, msg = validate_input_parameters(valid_params)
    assert is_valid, f"Valid parameters rejected: {msg}"
    print("✓ Valid parameters accepted")

    # Invalid age
    invalid_age = {**valid_params, 'Delivery_person_Age': 100}
    is_valid, msg = validate_input_parameters(invalid_age)
    assert not is_valid, "Invalid age not caught"
    print("✓ Invalid age rejected")

    # Invalid rating
    invalid_rating = {**valid_params, 'Delivery_person_Ratings': 6.0}
    is_valid, msg = validate_input_parameters(invalid_rating)
    assert not is_valid, "Invalid rating not caught"
    print("✓ Invalid rating rejected")

    # Invalid distance
    invalid_distance = {**valid_params, 'distance_km': 50}
    is_valid, msg = validate_input_parameters(invalid_distance)
    assert not is_valid, "Invalid distance not caught"
    print("✓ Invalid distance rejected")

    print("\n[PASS] Input parameter validation tests")


def test_calculate_time_components():
    """Test time component calculation"""

    components = calculate_time_components(
        distance_km=5.0,
        traffic_level=2,
        weather='Sunny',
        hour=12,
        age=30,
        rating=4.5,
        is_festival=False,
        multiple_deliveries=1
    )

    # Verify components exist
    required_keys = [
        'base_time', 'distance_time', 'traffic_factor',
        'weather_factor', 'age_factor', 'rating_factor',
        'festival_factor', 'rush_hour_factor', 'multiple_factor'
    ]

    for key in required_keys:
        assert key in components, f"Missing component: {key}"
    print("✓ All components calculated")

    # Verify reasonable values
    assert components['base_time'] == 10, "Base time incorrect"
    assert components['distance_time'] == 10, "Distance time incorrect (5km * 2)"
    assert components['traffic_factor'] == 6, "Traffic factor incorrect (2 * 3)"
    assert components['weather_factor'] == 0, "Weather factor incorrect for sunny"
    print("✓ Component values correct")

    # Test with adverse weather
    components_rainy = calculate_time_components(
        distance_km=5.0,
        traffic_level=2,
        weather='Rainy',
        hour=12,
        age=30,
        rating=4.5,
        is_festival=False,
        multiple_deliveries=1
    )
    assert components_rainy['weather_factor'] == 5, "Rainy weather impact incorrect"
    print("✓ Weather impact calculated correctly")

    # Test with rush hour
    components_rush = calculate_time_components(
        distance_km=5.0,
        traffic_level=2,
        weather='Sunny',
        hour=12,  # 12 is rush hour
        age=30,
        rating=4.5,
        is_festival=False,
        multiple_deliveries=1
    )
    assert components_rush['rush_hour_factor'] == 3, "Rush hour factor incorrect"
    print("✓ Rush hour impact calculated correctly")

    print("\n[PASS] Time component calculation tests")


def test_predict_delivery_time():
    """Test delivery time prediction"""

    params = {
        'distance_km': 5.0,
        'traffic_level': 2,
        'weather': 'Sunny',
        'hour': 12,
        'Delivery_person_Age': 30,
        'Delivery_person_Ratings': 4.5,
        'is_festival': False,
        'multiple_deliveries': 1
    }

    predicted_time, components = predict_delivery_time(
        model=None, params=params)

    # Verify prediction is positive
    assert predicted_time > 0, "Prediction should be positive"
    print(f"✓ Prediction generated: {predicted_time:.2f} minutes")

    # Verify prediction is in reasonable range
    assert 5 <= predicted_time <= 120, "Prediction outside reasonable range"
    print("✓ Prediction in reasonable range (5-120 min)")

    # Verify components are non-negative
    for key, value in components.items():
        assert value >= 0, f"Component {key} is negative: {value}"
    print("✓ All components non-negative")

    print("\n[PASS] Delivery time prediction tests")


def test_generate_delivery_recommendations():
    """Test recommendation generation"""

    # Normal conditions
    recommendations = generate_delivery_recommendations(
        distance_km=5.0,
        traffic_level=1,
        weather='Sunny',
        hour=10,
        rating=4.5,
        is_festival=False
    )
    assert len(recommendations) > 0, "Should generate at least one recommendation"
    print(
        f"✓ Generated {len(recommendations)} recommendation(s) for optimal conditions")

    # Adverse conditions
    recommendations_adverse = generate_delivery_recommendations(
        distance_km=20.0,
        traffic_level=4,
        weather='Stormy',
        hour=12,
        rating=2.0,
        is_festival=True
    )
    assert len(
        recommendations_adverse) > 2, "Should generate multiple recommendations for adverse conditions"
    print(
        f"✓ Generated {len(recommendations_adverse)} recommendation(s) for adverse conditions")

    # Verify recommendations are strings
    for rec in recommendations_adverse:
        assert isinstance(rec, str), "Recommendation should be a string"
    print("✓ All recommendations are valid strings")

    print("\n[PASS] Recommendation generation tests")


def test_create_forecast_range():
    """Test forecast range creation"""

    forecast = create_forecast_range(predicted_time=30.0, confidence=0.85)

    # Verify structure
    required_keys = ['lower_bound', 'point_estimate',
                     'upper_bound', 'confidence']
    for key in required_keys:
        assert key in forecast, f"Missing key: {key}"
    print("✓ Forecast range structure correct")

    # Verify bounds
    assert forecast['lower_bound'] < forecast['point_estimate'], "Lower bound should be less than point estimate"
    assert forecast['point_estimate'] < forecast['upper_bound'], "Upper bound should be more than point estimate"
    assert forecast['confidence'] == 0.85, "Confidence value incorrect"
    print("✓ Forecast bounds in correct order")

    # Verify reasonable margin
    margin = forecast['upper_bound'] - forecast['lower_bound']
    assert margin > 0, "Margin should be positive"
    print(
        f"✓ Confidence interval: {forecast['lower_bound']:.2f} - {forecast['upper_bound']:.2f} minutes")

    print("\n[PASS] Forecast range tests")


def run_all_tests():
    """Run all tests"""

    print("\n" + "="*60)
    print("SMART LOGISTICS - UNIT TESTS")
    print("="*60 + "\n")

    try:
        test_validate_input_parameters()
        test_calculate_time_components()
        test_predict_delivery_time()
        test_generate_delivery_recommendations()
        test_create_forecast_range()

        print("\n" + "="*60)
        print("ALL TESTS PASSED ✅")
        print("="*60 + "\n")
        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
