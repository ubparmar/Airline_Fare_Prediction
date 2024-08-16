# Sky Vista Fare Prediction Project

## Predict Fare Prices with Machine Learning

> "The future belongs to those who believe in the beauty of their dreams." - Eleanor Roosevelt

Welcome to the Sky Vista Fare Prediction Project! Our mission is to harness the power of machine learning to provide accurate fare price predictions, empowering travelers to make informed decisions and optimize their journeys.

## Project Website
Just wait 1 minute and reload the link it takes time to wakeup the project on render.
Visit our project website [Click here](https://airline-fare-prediction.onrender.com/).

## Project Demo

Check out our project demo video(Click below image to see video):

[![Sky Vista Fare Prediction Demo](https://img.youtube.com/vi/V9zUiECHzNE/0.jpg)](https://www.youtube.com/watch?v=V9zUiECHzNE)

## Project Setup

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: Version 3.7 or higher
- **pip**: The Python package installer
- **Virtual Environment**: (optional but recommended)

### Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/ubparmar/Airline_Fare_Prediction.git
   cd Airline_Fare_Prediction

2. **Active Virtual Environment**:
   ```sh
   To activate the virtual environment, use the following command:
   source venv/bin/activate # On macOS/Linux
   .\venv\Scripts\activate # On Windows

2. **Run Project**:
   ```sh
   py manage.py runserver

3. **In Order to run the project in localhost**:
   ```sh
   Configure settings.py for Local Development:
   When running the project on localhost, make the following adjustments to the settings.py 
   Uncomment the below:
   ALLOWED_HOSTS = []
   And Remove the below:
   ALLOWED_HOSTS = ['airline-fare-prediction.onrender.com' ]

4. **Ensure below lines are also uncommented**
   ```sh
   STATIC_URL = "static/"

   STATICFILES_DIRS = [
      os.path.join(BASE_DIR, "static"),
   ]

5. **Ensure Debug is Set to True**
   ```sh
   DEBUG = True

6. **Leave the following commented out**
-Production ALLOWED_HOSTS
-WhiteNoise middleware and storage
-Production STATIC_ROOT setting
7. **Start the Development Server**
   ```sh
   python manage.py runserver
8. **Access the Application:Open your web browser and navigate to below link**
   ```sh
   http://127.0.0.1:8000/
## Features

- Accurate prediction of airline fares using advanced machine learning algorithms
- User-friendly web interface for easy input and result visualization
- Support for multiple airlines and routes
- Historical data analysis for trend identification

## Technologies Used

- Python 3.x
- Scikit-learn for machine learning models
- Pandas and NumPy for data manipulation
- Django for web application framework
- HTML/CSS/JavaScript for frontend
- Git for version control

## Data

Our model is trained on a comprehensive dataset of historical flight prices, which includes:
- Date of journey
- Source and Destination
- Airline
- Duration of flight
- Total stops

To download dataset [click here](https://github.com/ubparmar/Airline_Fare_Prediction/tree/main/Data).

## Model

We use a Decision Tree Regressor model, which has shown the best performance for our use case. The model is periodically retrained with updated data to ensure accuracy.

## Usage

After setting up the project, you can use the prediction model through our web interface or via API:

1. Navigate to the home page
2. Input your flight details (date, source, destination, etc.)
3. Click "Predict" to see the estimated fare

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/ubparmar/Airline_Fare_Prediction?tab=MIT-1-ov-file) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape the Sky Vista Fare Prediction Project
- Special thanks to [Kayak] for providing additional data resources
- Inspired by [Kayak], [https://www.ca.kayak.com/]

## Collaborators
[@tirth-patel01](https://github.com/tirth-patel01)
[@Swethaloyalist](https://github.com/Swethaloyalist)
[@Janki-31](https://github.com/Janki-31)
[@gaurav809](https://github.com/gaurav809)
[@Comfyonuoha](https://github.com/Comfyonuoha)
[@DSS7](https://github.com/DSS7)
[@Fatemi](https://github.com/fatemi-loyalist)
[@Isha-123456](https://github.com/Isha-123456)
[@itzgauravvv](https://github.com/itzgauravvv)
[@Mohamed-Maaz-Rehan](https://github.com/Mohamed-Maaz-Rehan)
[@Urjeet Parmar](https://github.com/ubparmar)
