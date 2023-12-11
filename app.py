import streamlit as st
import joblib
import datetime
import pandas as pd
import numpy as np

# Dictionary of airport codes and their corresponding city names
airport_data = {
    'OAK': 'Oakland',
    'DEN': 'Denver',
    'LGA': 'New York (LaGuardia)',
    'LAX': 'Los Angeles',
    'ATL': 'Atlanta',
    'CLT': 'Charlotte',
    'PHL': 'Philadelphia',
    'DTW': 'Detroit',
    'IAD': 'Washington (Dulles)',
    'JFK': 'New York (JFK)',
    'DFW': 'Dallas/Fort Worth',
    'BOS': 'Boston',
    'EWR': 'Newark',
    'SFO': 'San Francisco',
    'ORD': "Chicago (O'Hare)",
    'MIA': 'Miami'
}

# List of airport codes
airport_codes = list(airport_data.keys())

# Load your saved models (XGBoost, Random Forest, Multilayer NN, Keras NN)
model1 = joblib.load('models/xgboost.joblib')
model2 = joblib.load('models/random_forest.joblib')
model3 = joblib.load('models/multilayer_neural_network.joblib')
model4 = joblib.load('models/keras_neural_network.joblib')

# Define a function to make predictions based on user inputs
def predict_fare(airport_origin, airport_destination, departure_date, departure_time, cabin_type):
    # Calculate FlightDayOfMonth, FlightMonth, FlightDayOfWeek, and departureHourOfDay
    flight_day_of_month = departure_date.day
    flight_month = departure_date.month
    flight_day_of_week = departure_date.weekday()
    departure_hour_of_day = departure_time.hour

    # Create a DataFrame with the user inputs
    data = pd.DataFrame({
        'startingAirport': [airport_origin],
        'destinationAirport': [airport_destination],
        'totalFare': [0], 
        'segmentsCabinCode': [cabin_type.lower()],
        'FlightDayOfMonth': [flight_day_of_month],
        'FlightMonth': [flight_month],
        'FlightDayOfWeek': [flight_day_of_week],
        'departureHourOfDay': [departure_hour_of_day]
    })

    # Use each model to make fare predictions
    predicted_fare1 = model1.predict(data)
    predicted_fare2 = model2.predict(data)
    predicted_fare3 = model3.predict(data)
    predicted_fare4 = model4.predict(data)

    # Return the predicted fares from all four models
    return predicted_fare1[0], predicted_fare2[0], predicted_fare3[0], predicted_fare4[0]

# Create a Streamlit web app
st.title("Flight Fare Estimation App \U0001F6EB")

# User input fields with both city names and airport codes
airport_origin = st.selectbox("Select Origin Airport", [f"{code} - {city}" for code, city in airport_data.items()], index=0)
airport_destination = st.selectbox("Select Destination Airport", [f"{code} - {city}" for code, city in airport_data.items()], index=1)
departure_date = st.date_input("Departure Date", min_value=datetime.date.today())
departure_time = st.time_input("Departure Time", datetime.time(8, 0))
cabin_type = st.selectbox("Cabin Type", ["Coach", "Premium Coach", "Business", "First"])

# Get the selected airport codes (e.g., 'OAK' from 'OAK - Oakland')
selected_origin_code = airport_origin.split(' - ')[0]
selected_destination_code = airport_destination.split(' - ')[0]

# Check if the same airport is selected for both origin and destination
if selected_origin_code == selected_destination_code:
    st.warning("Please select different airports for origin and destination.")
else:
    # Predict button
    if st.button(f"\u2708\ufe0f Get fare"):
        if airport_origin and airport_destination and departure_date and departure_time and cabin_type:
            # Call the predict_fare function and calculate the average fare from four models
            fare1, fare2, fare3, fare4 = predict_fare(selected_origin_code, selected_destination_code, departure_date, departure_time, cabin_type)
            float_fare1 = float(fare1) if fare1.size == 1 else fare1
            float_fare2 = float(fare2) if fare2.size == 1 else fare2
            float_fare3 = float(fare3) if fare3.size == 1 else fare3
            float_fare4 = float(fare4) if fare4.size == 1 else fare4
            average_fare = np.mean([float_fare1, float_fare2, float_fare3, float_fare4])
            st.success(f"The estimated fare is US${average_fare:.2f}")
        else:
            st.warning("Please fill in all the required fields.")

# Display additional information or instructions
st.markdown("### Instructions")
st.write("1. Select the Origin and Destination airports from the dropdown lists.")
st.write("2. Select the Departure Date and Time from the present day.")
st.write("3. Choose the Cabin Type from the dropdown.")
st.write("4. Click the '\u2708\ufe0f Get fare' button to get the estimated fare.")

# Display additional information
st.markdown("### About")
st.write("This app calculates the average fare from four different models' predicted fares.")
st.write("It takes into account the origin and destination airports, departure date and time, and cabin type.")
st.write("Github Models Link: https://github.com/ssandeed/flight_prediction_exp")
