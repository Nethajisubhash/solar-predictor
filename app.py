# Flask app for predicting AC Power

from flask import Flask, request, render_template
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler

# Load the trained model and scaler (assuming they are saved as pickle files)
app = Flask(__name__)

# Load the trained model (assuming it is saved as a pickle file)
model = pickle.load(open('loaded_model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        irradiation = float(request.form['irradiation'])
        time_of_day = request.form['time']  # Time in HH:MM format (24-hour)
        
        # Convert time to total minutes
        hours, minutes = map(int, time_of_day.split(':'))  # Split into hours and minutes
        total_minutes = hours * 60 + minutes  # Calculate total minutes

        input_data = np.array([[temperature, humidity, irradiation, total_minutes]])

        # Make prediction
        prediction = [123.45]  # dummy value
        prediction = model.predict(input_data)

        prediction = np.expm1(prediction) - 1
        
        # Convert prediction to float and round
        predicted_value = float(np.round(prediction[0], 2))
        
        return render_template('index.html', prediction=predicted_value,
                                             temperature=temperature, 
                                             humidity=humidity, 
                                             irradiation=irradiation, 
                                             time=time_of_day)     
        except Exception as e:
              return render_template('index.html', prediction=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
