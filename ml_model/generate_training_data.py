"""
Generate realistic training data for rockfall ML model
"""

import numpy as np
import pandas as pd
import random

print("🚀 Generating synthetic training data...")
print("=" * 50)

# Generate 10000 samples
n_samples = 10000
data = []

for i in range(n_samples):
    # Features
    vibration = random.uniform(0, 1)
    displacement = random.uniform(0, 15)
    rainfall = random.uniform(0, 50)
    temperature = random.uniform(15, 45)
    
    # Calculate risk (complex pattern)
    risk = 0.0
    if vibration > 0.7 and displacement > 8:
        risk = random.uniform(0.7, 1.0)
    elif vibration > 0.4 and displacement > 4:
        risk = random.uniform(0.4, 0.7)
    else:
        risk = random.uniform(0, 0.3)
    
    data.append([vibration, displacement, rainfall, temperature, risk])

# Create DataFrame
df = pd.DataFrame(data, columns=['vibration', 'displacement', 'rainfall', 'temperature', 'risk_score'])

# Save to CSV
df.to_csv('ml_model/rockfall_training_data.csv', index=False)

print(f"✅ Generated {len(df)} samples")
print(f"📊 Average risk: {df['risk_score'].mean():.3f}")
print("=" * 50)