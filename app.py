from flask import Flask, request, jsonify, send_from_directory, render_template_string
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Load the model
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'pipe.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

@app.route('/')
def home():
    # Serve index.html directly from root directory
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        company = request.form.get('company')
        car_model = request.form.get('car_models')
        year = int(request.form.get('year'))
        kilo_driven = int(request.form.get('kilo_driven'))
        fuel_type = request.form.get('fuel_type')

        # Create input DataFrame
        input_data = pd.DataFrame([[
            car_model,
            company,
            year,
            kilo_driven,
            fuel_type
        ]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])

        # Make prediction
        prediction = model.predict(input_data)
        
        # Return the prediction
        return str(round(prediction[0], 2))
    
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)