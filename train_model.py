"""
Script to train and save the delivery time prediction model
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from lightgbm import LGBMRegressor
import joblib
import warnings

warnings.filterwarnings('ignore')

# Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODEL_PATH = 'models/delivery_time_model.pkl'
PREPROCESSOR_PATH = 'models/preprocessor.pkl'

print("=" * 80)
print("SMART LOGISTICS - MODEL TRAINING PIPELINE")
print("=" * 80)

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Load data
print("\n[1/5] Loading data...")
try:
    df = pd.read_csv('data/raw/train.csv')
    print(f"✓ Loaded training data: {df.shape}")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    sys.exit(1)

# Data preprocessing
print("\n[2/5] Preprocessing data...")
try:
    # Convert datetime columns
    for col in ['order_date', 'time_orderd', 'time_order_picked']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Extract features
    if 'order_date' in df.columns:
        df['day_of_week'] = df['order_date'].dt.day_name()
        df['month'] = df['order_date'].dt.month

    if 'time_orderd' in df.columns:
        df['order_hour'] = df['time_orderd'].dt.hour

    # Clean text columns
    if 'weatherconditions' in df.columns:
        df['weatherconditions'] = df['weatherconditions'].str.replace(
            'conditions ', '', regex=False).str.strip()

    if 'city' in df.columns:
        df['city'] = df['city'].replace({"Metropolitian": "Metropolitan"})

    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    print("✓ Data preprocessing completed")
    print(f"  - Dataset shape: {df.shape}")
    print(f"  - Missing values: {df.isnull().sum().sum()}")

except Exception as e:
    print(f"✗ Error during preprocessing: {e}")
    sys.exit(1)

# Feature selection
print("\n[3/5] Selecting features...")
try:
    # Define features and target
    numeric_features = ['Delivery_person_Age', 'Delivery_person_Ratings',
                        'multiple_deliveries', 'order_hour']
    categorical_features = ['weatherconditions', 'type_of_order', 'type_of_vehicle',
                            'festival', 'city', 'day_of_week']

    # Filter existing columns
    numeric_features = [f for f in numeric_features if f in df.columns]
    categorical_features = [f for f in categorical_features if f in df.columns]

    target = 'Time_taken(min)' if 'Time_taken(min)' in df.columns else 'time_taken_min'

    if target not in df.columns:
        # Try to find target column
        target_cols = [
            col for col in df.columns if 'time' in col.lower() and 'taken' in col.lower()]
        if target_cols:
            target = target_cols[0]
        else:
            print(f"✗ Target column not found")
            sys.exit(1)

    X = df[numeric_features + categorical_features]
    y = df[target]

    print("✓ Feature selection completed")
    print(f"  - Numeric features: {len(numeric_features)}")
    print(f"  - Categorical features: {len(categorical_features)}")
    print(f"  - Target: {target}")

except Exception as e:
    print(f"✗ Error during feature selection: {e}")
    sys.exit(1)

# Create preprocessing pipeline
print("\n[4/5] Building preprocessing pipeline...")
try:
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    print("✓ Preprocessing pipeline created")
    print(f"  - Train set: {X_train.shape}")
    print(f"  - Test set: {X_test.shape}")

except Exception as e:
    print(f"✗ Error building pipeline: {e}")
    sys.exit(1)

# Train model
print("\n[5/5] Training LightGBM model...")
try:
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LGBMRegressor(n_estimators=100,
         random_state=RANDOM_STATE, verbose=-1))
    ])

    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("✓ Model training completed")
    print(f"\nModel Performance:")
    print(f"  - MAE (Mean Absolute Error): {mae:.2f} minutes")
    print(f"  - RMSE (Root Mean Squared Error): {rmse:.2f} minutes")
    print(f"  - R² Score: {r2:.4f}")

    # Save model and preprocessor
    joblib.dump(pipeline, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    print(f"\n✓ Model saved to: {MODEL_PATH}")
    print(f"✓ Preprocessor saved to: {PREPROCESSOR_PATH}")

except Exception as e:
    print(f"✗ Error during model training: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 80)
