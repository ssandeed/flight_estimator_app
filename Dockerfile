# Use the official Python image as the base image
FROM python:3.9.13

# Set the working directory in the container
WORKDIR /flight_estimator_app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the trained model file into the container
COPY /models/random_forest.joblib models/
COPY /models/xgboost.joblib models/
COPY /models/multilayer_neural_network.joblib models/
COPY /models/keras_neural_network.joblib models/

# Copy your Streamlit app file (streamlit_app.py) into the container
COPY app.py .

# Expose the port your Streamlit app will run on
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "app.py"]
