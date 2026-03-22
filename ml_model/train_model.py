"""
Train ML model for rockfall prediction
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

print("🚀 Training Rockfall Prediction Model...")
print("=" * 50)

# Load data
print("📊 Loading training data...")
df = pd.read_csv('ml_model/rockfall_training_data.csv')
print(f"   Loaded {len(df)} samples")

# Features and target
features = ['vibration', 'displacement', 'rainfall', 'temperature']
X = df[features]
y = df['risk_score']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples: {len(X_test)}")

# Train model
print("\n🧠 Training Random Forest model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("\n📈 Evaluating model...")
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"   Mean Squared Error: {mse:.4f}")
print(f"   R² Score: {r2:.4f}")
print(f"   Accuracy: {r2*100:.1f}%")

# Feature importance
importance = model.feature_importances_
print("\n🔑 Feature Importance:")
for feat, imp in zip(features, importance):
    print(f"   {feat}: {imp:.3f}")

# Save model
print("\n💾 Saving model...")
joblib.dump(model, 'ml_model/rockfall_model.pkl')
print("   Model saved to: ml_model/rockfall_model.pkl")

# Save feature names
import json
with open('ml_model/features.json', 'w') as f:
    json.dump(features, f)
print("   Features saved to: ml_model/features.json")

print("\n✅ Model training complete!")
print("=" * 50)