import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import joblib

def main():
    print("Loading data...")
    try:
        df = pd.read_csv('laptop_data.csv')
    except FileNotFoundError:
        print("laptop_data.csv not found! Please run generate_dummy_data.py first.")
        return

    print("Preprocessing data...")
    X = df.drop('Price_PKR', axis=1)
    y = df['Price_PKR']
    
    categorical_cols = ['Brand', 'Processor', 'GPU']
    numerical_cols = ['RAM_GB', 'Storage_GB']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Linear Regression...")
    lr_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('model', LinearRegression())])
    lr_pipeline.fit(X_train, y_train)
    
    print("Training Random Forest...")
    rf_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('model', RandomForestRegressor(n_estimators=100, random_state=42))])
    rf_pipeline.fit(X_train, y_train)
    
    lr_preds = lr_pipeline.predict(X_test)
    rf_preds = rf_pipeline.predict(X_test)
    
    lr_r2 = r2_score(y_test, lr_preds)
    rf_r2 = r2_score(y_test, rf_preds)
    
    print("-" * 30)
    print("Evaluation Results (R^2 Score):")
    print(f"Linear Regression R^2: {lr_r2:.4f}")
    print(f"Random Forest R^2:     {rf_r2:.4f}")
    print("-" * 30)
    
    print("Saving Random Forest model to laptop_model.joblib for the web app...")
    joblib.dump(rf_pipeline, 'laptop_model.joblib')
    
    metadata = {
        'brands': sorted(df['Brand'].unique().tolist()),
        'processors': sorted(df['Processor'].unique().tolist()),
        'gpus': sorted(df['GPU'].unique().tolist()),
        'rams': sorted(df['RAM_GB'].unique().tolist()),
        'storages': sorted(df['Storage_GB'].unique().tolist())
    }
    joblib.dump(metadata, 'laptop_metadata.joblib')
    print("Training complete! Model and metadata saved.")

if __name__ == "__main__":
    main()
