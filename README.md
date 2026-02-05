# 🚚 **Smart Logistics Delivery Prediction System**

A machine-learning powered **Streamlit dashboard** for predicting food delivery times using real-world factors such as weather, traffic, vehicle type, distance, delivery person rating, and more.

---

## ⚡ **Quick Start**

### **1-Click (Windows)**

```bash
run_app.bat
```

### **PowerShell**

```bash
.\run_app.ps1
```

### **Manual Run**

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

**App URL:** [http://localhost:8501](http://localhost:8501)

---

## 📋 **First-Time Setup**

```bash
cd "path/to/Smart_Logistics_Delivery_Prediction"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

> Make sure your dataset is placed in:
> `data/raw/train.csv` and `data/raw/test.csv`

---

## 🎯 **Dashboard Overview**

The dashboard has **3 main pages**, each with multiple analytics tools.

---

### 📊 **1. Dataset Overview**

Understand dataset structure:

* KPI metrics (records, missing values, feature count)
* Raw data preview (first 100 rows)
* Column-level info & statistics
* Missing value analysis & data quality score
* Feature descriptions

---

### 📈 **2. EDA Analysis**

Five in-depth analysis tabs:

**• Distribution Analysis**
Histograms and category-level distributions.

**• Relationship Analysis**
Scatter plots, trendlines, delivery time relationships.

**• Time Analysis**
Hourly delivery patterns, rush hour detection.

**• Geographic Analysis**
Interactive maps using Folium + city-level summaries.

**• Correlations**
Heatmaps and multicollinearity checks.

---

### 🎯 **3. Prediction Dashboard**

Real-time prediction with factor-level breakdown:

**Sidebar Controls**

* Age, rating, vehicle type
* Weather & traffic
* Distance & multiple deliveries
* Food type & festival indicator
* Time of day

**Main Output**

* Predicted delivery time with confidence
* Factor contribution breakdown (bar + pie chart)
* Route visualization map
* Smart alerts (traffic, weather, festival, rush hour)

---

## 🧠 **How Predictions Work**

### **Model Formula (Simplified)**

```
Total Delivery Time =
  Base Time +
  Distance × 2 +
  Traffic Impact +
  Weather Penalty +
  Rating & Age adjustments +
  Festival Impact +
  Rush Hour Impact +
  (Multiple Deliveries × 2)
```

### **Key Input Factors**

* Distance (primary predictor)
* Weather (up to +12 min)
* Traffic Levels (+3 to +12 min)
* Time of day (peak hour adjustments)
* Delivery person rating & age
* Festival indicator
* Vehicle type

---

## 📊 **Machine Learning Model**

* **Algorithm:** LightGBM Regression
* **Performance:** R² > 0.85, MAE < 5 minutes
* **Why LightGBM?** Fast, accurate, handles categorical features, ideal for structured data.

### **Pipeline**

1. Load raw data
2. Clean missing values
3. Engineer features (distance, time, traffic mappings)
4. Encode + scale
5. Train using GridSearchCV
6. Evaluate with MAE, RMSE, R²

### **Train Your Own Model**

```bash
python train_model.py
```

Model saved to:

```
models/delivery_time_model.pkl
```

---

## ⚙️ **Configuration (config.py)**

You can adjust:

* Base delivery time
* Time per km
* Weather & traffic penalty values
* Rush hour settings
* Geographic bounds
* File paths

Example:

```python
BASE_TIME = 10
TIME_PER_KM = 2
WEATHER_IMPACT = {"Sunny":0, "Rainy":5, "Fog":8, "Stormy":10}
RUSH_HOUR_HOURS = [7,8,9,11,12,13,18,19,20]
MODEL_PATH = "models/delivery_time_model.pkl"
```

---

## 📁 **Project Structure**

```
Smart_Logistics_Delivery_Prediction/
│
├── app/
│   ├── streamlit_app.py
│   ├── utils.py
│   ├── visualizations.py
│
├── data/
│   ├── raw/ (train.csv, test.csv)
│   └── processed/
│
├── models/
│   ├── delivery_time_model.pkl
│   └── preprocessor.pkl
│
├── config.py
├── train_model.py
├── preprocess_data.py
├── run_app.bat
├── run_app.ps1
└── README.md
```

---

## 🧪 **Testing**

```bash
python tests.py
```

Tests cover:

* Input validation
* Prediction logic
* Factor calculations
* Error handling

---

## 📦 **Dependencies**

All in `requirements.txt`:

* pandas, numpy
* scikit-learn, lightgbm, statsmodels
* streamlit, plotly, seaborn
* folium, geopy
* joblib, python-dotenv
* pytest

Install:

```bash
pip install -r requirements.txt
```

---

## 🚀 **Useful Commands**

| Task          | Command                                                 |
| ------------- | ------------------------------------------------------- |
| Start app     | `run_app.bat`                                           |
| Run manually  | `streamlit run app/streamlit_app.py`                    |
| Custom port   | `streamlit run app/streamlit_app.py --server.port 8502` |
| Preprocess Data| `python preprocess_data.py`                             |
| Train model   | `python train_model.py`                                 |
| Tests         | `python tests.py`                                       |
| Activate venv | `.venv\Scripts\activate`                                |

---

## 🐛 **Troubleshooting**

| Issue                    | Fix                                    |
| ------------------------ | -------------------------------------- |
| "Module not found"       | Reinstall dependencies                 |
| Port 8501 busy           | Use `--server.port 8502`               |
| Model missing            | Run `train_model.py`                   |
| Data loading error       | Run `python preprocess_data.py`        |
| Data not loading         | Ensure CSV in `data/raw/`              |
| PowerShell script denied | Run `Set-ExecutionPolicy RemoteSigned` |

---

## 🎓 **Expected Dataset Format**

Includes:

* Numeric: age, rating, multiple deliveries
* Categorical: weather, traffic, vehicle type, food type
* Geo: restaurant + delivery coordinates
* Time columns
* Target: `Time_taken(min)`

---

## 🎉 **Ready to Use**

**Launch the app:**

```bash
run_app.bat
```

**Open in browser:**
[http://localhost:8501](http://localhost:8501)

---

