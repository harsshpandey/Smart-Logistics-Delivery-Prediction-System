import pandas as pd
import sys
import os
import joblib

# Add project root to path
sys.path.append(os.getcwd())

import project_config as config
from app import utils

def verify_logic():
    print("1. Testing Data Loading...")
    try:
        df = pd.read_csv(f"{config.DATA_RAW_PATH}/processed_train.csv")
        print(f"   SUCCESS: Loaded {len(df)} rows.")
    except Exception as e:
        print(f"   FAILURE: {e}")
        return

    print("\n2. Testing Model Loading...")
    try:
        model = utils.load_model(config.MODEL_PATH)
        if model:
            print("   SUCCESS: Model loaded.")
        else:
            print("   WARNING: Model not found, will use heuristic.")
    except Exception as e:
        print(f"   FAILURE: Model load error: {e}")
        model = None

    print("\n3. Testing Prediction Logic...")
    try:
        # Mock input params matching new schema
        params = {
            'delivery_person_age': 30,
            'delivery_person_ratings': 4.5,
            'delivery_distance_km': 10,
            'prep_time_min': 15,
            'traffic_level': 2, # Changed from 'Medium' to 2
            'order_hour': 14,
            'festival': "No",
            'weatherconditions': "conditions Sunny", # Testing with prefix
            'type_of_vehicle': "motorcycle",
            'type_of_order': "Meal",
            'city': "Metropolitian"
        }
        
        # Test prediction
        pred_time, components = utils.predict_delivery_time(model, params, use_demo=False)
        print(f"   SUCCESS: Prediction returned {pred_time} min.")
        print(f"   Components: {components}")
        
    except Exception as e:
        print(f"   FAILURE: Prediction logic error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_logic()
