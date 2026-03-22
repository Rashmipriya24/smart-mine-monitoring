"""
ML Model Predictor for Rockfall API
Loads trained model and makes predictions
"""

import joblib
import numpy as np
import json
import os

class RockfallPredictor:
    def __init__(self, model_path='ml_model/rockfall_model.pkl', features_path='ml_model/features.json'):
        """Load model and features on initialization"""
        print("🚀 Loading ML Model...")
        
        # Load model
        self.model = joblib.load(model_path)
        print(f"✅ Model loaded from: {model_path}")
        
        # Load feature names
        with open(features_path, 'r') as f:
            self.features = json.load(f)
        print(f"✅ Features loaded: {self.features}")
        
        # Model accuracy (from training)
        self.accuracy = 89.1
        print(f"📊 Model Accuracy: {self.accuracy}%")
    
    def predict(self, vibration, displacement, rainfall=0, temperature=25):
        """
        Predict risk score based on sensor readings
        Returns: risk_score (0-1), risk_level, confidence
        """
        # Create feature array in correct order
        features = np.array([[vibration, displacement, rainfall, temperature]])
        
        # Predict
        risk_score = self.model.predict(features)[0]
        
        # Clip between 0 and 1
        risk_score = max(0.0, min(1.0, risk_score))
        
        # Determine risk level
        if risk_score > 0.7:
            risk_level = "CRITICAL"
            color = "🔴"
        elif risk_score > 0.4:
            risk_level = "WARNING"
            color = "🟠"
        elif risk_score > 0.2:
            risk_level = "LOW"
            color = "🟡"
        else:
            risk_level = "SAFE"
            color = "🟢"
        
        # Confidence based on model accuracy
        confidence = self.accuracy / 100.0
        
        return {
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'color': color,
            'confidence': confidence,
            'features_used': {
                'vibration': vibration,
                'displacement': displacement,
                'rainfall': rainfall,
                'temperature': temperature
            }
        }
    
    def explain_prediction(self, vibration, displacement, rainfall=0, temperature=25):
        """Explain why this prediction was made"""
        result = self.predict(vibration, displacement, rainfall, temperature)
        
        explanation = f"\n{'='*50}\n"
        explanation += f"🔮 PREDICTION EXPLANATION\n"
        explanation += f"{'='*50}\n"
        explanation += f"Input: Vib={vibration:.3f}g, Disp={displacement:.2f}mm\n"
        explanation += f"Risk Score: {result['risk_score']:.3f} ({result['risk_level']}) {result['color']}\n"
        explanation += f"Confidence: {result['confidence']*100:.1f}%\n\n"
        
        # Simple rule-based explanation
        if vibration > 0.7 and displacement > 8:
            explanation += "⚠️ CRITICAL: Both vibration and displacement very high!\n"
        elif vibration > 0.5 and displacement > 5:
            explanation += "⚠️ WARNING: Moderately high readings\n"
        elif vibration > 0.3 or displacement > 3:
            explanation += "ℹ️ LOW: Slightly elevated readings\n"
        else:
            explanation += "✅ SAFE: Normal operating conditions\n"
        
        explanation += f"{'='*50}"
        
        return explanation

# Test if run directly
if __name__ == "__main__":
    predictor = RockfallPredictor()
    
    # Test predictions
    test_cases = [
        (0.2, 1.0),   # Safe
        (0.5, 5.0),   # Warning
        (0.9, 12.0),  # Critical
    ]
    
    print("\n📊 TEST PREDICTIONS:")
    for vib, disp in test_cases:
        result = predictor.predict(vib, disp)
        print(f"Vib={vib:.1f}, Disp={disp:.1f} → Risk={result['risk_score']:.3f} ({result['risk_level']})")
    
    # Show explanation for one case
    print(predictor.explain_prediction(0.8, 10.0))