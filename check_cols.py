import pandas as pd
try:
    df = pd.read_csv('data/processed/processed_train.csv')
    print("Columns:", df.columns.tolist())
except Exception as e:
    print(e)
