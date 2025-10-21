import joblib

# Create a simple dictionary simulating a model with prediction label and confidence
model = {
    'prediction': 'cat',
    'confidence': 0.95,
    'model_type': 'image_classifier'
}

# Save the model as model.pkl using joblib
joblib.dump(model, 'model.pkl')

print("Model saved successfully as model.pkl")
