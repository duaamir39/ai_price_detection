import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Machine Learning Algorithms
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
    AdaBoostRegressor
)
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

# Evaluation Metrics
from sklearn.metrics import r2_score, mean_absolute_error


def main():

    # =========================
    # LOAD DATA
    # =========================
    print("\nLoading dataset...")

    try:
        df = pd.read_csv('laptop_data.csv')

    except FileNotFoundError:
        print("\nERROR: laptop_data.csv not found!")
        print("Please run generate_dummy_data.py first.")
        return

    print("Dataset loaded successfully!")

    # =========================
    # FEATURES & TARGET
    # =========================
    X = df.drop('Price_PKR', axis=1)
    y = df['Price_PKR']

    # =========================
    # COLUMN TYPES
    # =========================
    categorical_cols = ['Brand', 'Processor', 'GPU']
    numerical_cols = ['RAM_GB', 'Storage_GB']

    # =========================
    # PREPROCESSING
    # =========================
    print("\nPreprocessing data...")

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )

    # =========================
    # TRAIN TEST SPLIT
    # =========================
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # =========================
    # ALL ML MODELS
    # =========================
    models = {

        "Linear Regression": LinearRegression(),

        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ),

        "Decision Tree": DecisionTreeRegressor(
            random_state=42
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=100,
            random_state=42
        ),

        "Extra Trees": ExtraTreesRegressor(
            n_estimators=100,
            random_state=42
        ),

        "AdaBoost": AdaBoostRegressor(
            n_estimators=100,
            random_state=42
        ),

        "K-Nearest Neighbors": KNeighborsRegressor(
            n_neighbors=5
        ),

        "Support Vector Regressor": SVR(
            kernel='rbf'
        )
    }

    # Dictionary to store trained pipelines
    trained_models = {}

    print("\n" + "=" * 60)
    print("TRAINING MACHINE LEARNING MODELS")
    print("=" * 60)

    # =========================
    # TRAIN ALL MODELS
    # =========================
    for model_name, model in models.items():

        print(f"\nTraining {model_name}...")

        # Create pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])

        # Train model
        pipeline.fit(X_train, y_train)

        # Predictions
        predictions = pipeline.predict(X_test)

        # Evaluation
        r2 = r2_score(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)

        # Store model
        trained_models[model_name] = pipeline

        # Print Results
        print(f"{model_name} Results:")
        print(f"R2 Score              : {r2:.4f}")
        print(f"Mean Absolute Error   : {mae:.2f}")

    # =========================
    # MODEL SELECTION
    # =========================
    print("\n" + "=" * 60)
    print("SELECT MODEL TO SAVE")
    print("=" * 60)

    model_names = list(models.keys())

    for i, name in enumerate(model_names, start=1):
        print(f"{i}. {name}")

    choice = input("\nEnter model number: ")

    try:

        choice = int(choice)

        if choice < 1 or choice > len(model_names):
            raise ValueError

        selected_model_name = model_names[choice - 1]

    except:
        print("\nInvalid choice!")
        print("Defaulting to Random Forest...\n")

        selected_model_name = "Random Forest"

    # Selected trained pipeline
    selected_pipeline = trained_models[selected_model_name]

    # =========================
    # SAVE MODEL
    # =========================
    print(f"Saving {selected_model_name} model...")

    joblib.dump(
        selected_pipeline,
        'laptop_model.joblib'
    )

    # =========================
    # SAVE METADATA
    # =========================
    metadata = {

        'brands': sorted(df['Brand'].unique().tolist()),

        'processors': sorted(df['Processor'].unique().tolist()),

        'gpus': sorted(df['GPU'].unique().tolist()),

        'rams': sorted(df['RAM_GB'].unique().tolist()),

        'storages': sorted(df['Storage_GB'].unique().tolist()),

        'algorithms': model_names
    }

    joblib.dump(
        metadata,
        'laptop_metadata.joblib'
    )

    # =========================
    # FINAL MESSAGE
    # =========================
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)

    print(f"\nSaved Model: {selected_model_name}")

    print("\nGenerated Files:")
    print("1. laptop_model.joblib")
    print("2. laptop_metadata.joblib")

    print("\nProject completed successfully!")


# =========================
# MAIN FUNCTION CALL
# =========================
if __name__ == "__main__":
    main()
