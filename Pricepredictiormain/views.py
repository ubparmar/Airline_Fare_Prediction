from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login  # Import the login function
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
import joblib
from datetime import datetime, timedelta,time,date
from django.urls import reverse
import re
from pathlib import Path
from django.http import HttpResponse
from django.contrib import messages
from .forms import ProfileEditForm
import os
import pandas as pd

# Load the saved model and label encoders
model_path = os.path.join(os.path.dirname(__file__), 'model_files', 'decisiontree_model.joblib')
encoders_path = os.path.join(os.path.dirname(__file__), 'model_files', 'label_encoders.joblib')

model = joblib.load(model_path)
le_dict = joblib.load(encoders_path)

# Extract choices
airline_choices = le_dict['Airline'].classes_
source_choices = le_dict['Source'].classes_
destination_choices = le_dict['Destination'].classes_
class_choices = le_dict['Class'].classes_

def predict_price(request):
    error_message = None
    total_stops_choices = [0, 1, 2, 3]
    if request.method == 'POST':
        airline = request.POST.get('airline')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        stops = request.POST.get('stops')
        travel_class = request.POST.get('travel_class')
        date_of_travel = request.POST.get('date_of_travel')
        stopover_time = request.POST.get('stopover_time')
       # departure_time = request.POST.get('departure_time')
       # arrival_time = request.POST.get('arrival_time')
       # arrival_day_offset = request.POST.get('arrival_day_offset')
        #days_left = (datetime.strptime(date_of_travel, "%Y-%m-%d") - datetime.now()).days

        if source == destination:
            error_message = "Source and destination airports cannot be the same."
        elif datetime.strptime(date_of_travel, "%Y-%m-%d").date() < date.today():
            error_message = "The date of travel cannot be in the past."
        else:
            user_input = {
                "Airline": airline,
                "Source": source,
                "Destination": destination,
                "Number of Stops": int(stops),
                "Class": travel_class,
                "Date": date_of_travel,
                # "Total_Stopover_Time": int(stopover_time),
               # "Departure_24hr": departure_time,
               # "Arrival_24hr": arrival_time,
                #"Arrival_Day_Offset": int(arrival_day_offset),
                #"days_left": days_left
            }

            def time_to_minutes(time_str):
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes

            def preprocess_user_input(user_input):
                user_df = pd.DataFrame([user_input])
                user_df['Date'] = pd.to_datetime(user_df['Date'])
                user_df['Month'] = user_df['Date'].dt.month
                user_df['DayOfWeek'] = user_df['Date'].dt.dayofweek
               # user_df['Departure_Minutes'] = user_df['Departure_24hr'].apply(time_to_minutes)
               # user_df['Arrival_Minutes'] = user_df['Arrival_24hr'].apply(time_to_minutes)

                for col in ['Airline', 'Source', 'Destination', 'Class']:
                    user_df[col + '_encoded'] = le_dict[col].transform(user_df[col])

                features = ['Number of Stops', 
                            'Month', 'DayOfWeek',
                            'Airline_encoded', 'Source_encoded', 'Destination_encoded', 'Class_encoded']
                return user_df[features]

            processed_input = preprocess_user_input(user_input)
            predicted_price = model.predict(processed_input)[0]
            prediction = f"{predicted_price:.2f} CAD"

            # Redirect to the result page with the prediction
            return redirect(reverse('show_prediction', args=[prediction]))

    return render(request, 'Pricepredictiormain/home.html', {
        'airline_choices': airline_choices,
        'source_choices': source_choices,
        'destination_choices': destination_choices,
        'class_choices': class_choices,
        'error_message': error_message,
        'total_stops_choices': total_stops_choices,
    })

def show_prediction(request, prediction):
    return render(request, 'Pricepredictiormain/prediction_result.html', {'prediction': prediction})
#Other Views

# def home(request):
#     user_count = User.objects.count()
#     context = {
#         'user_count': user_count
#     }   
#     return render(request, 'Pricepredictiormain/home.html',context)

def about(request):
    user_count = User.objects.count()
    context = {
        'user_count': user_count
    }
    return render(request, 'Pricepredictiormain/about.html',context)

def contact(request):
    user_count = User.objects.count()
    context = {
        'user_count': user_count
    }
    return render(request, 'Pricepredictiormain/contact.html',context)
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "Pricepredictiormain/register.html", {"form": form})
@login_required
def profile(request):
    predictions = {}
    error_message = None
    total_stops_choices = [0, 1, 2, 3]  # Example choices for number of stops

    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        stops = request.POST.get('stops')
        travel_class = request.POST.get('travel_class')
        date_of_travel = request.POST.get('date_of_travel')
        #stopover_time = request.POST.get('stopover_time')
       # departure_time = request.POST.get('departure_time')
       # arrival_time = request.POST.get('arrival_time')
        #arrival_day_offset = request.POST.get('arrival_day_offset')

        # Validate source and destination
        if source == destination:
            error_message = "Source and destination cannot be the same."

        # Validate date of travel
        travel_date = datetime.strptime(date_of_travel, "%Y-%m-%d").date()
        current_date = datetime.now().date()
        if travel_date < current_date:
            error_message = "Date of travel cannot be in the past."

        if not error_message:
            #days_left = (travel_date - current_date).days
            airlines = le_dict['Airline'].classes_

            for airline in airlines:
                user_input = {
                    "Airline": airline,
                    "Source": source,
                    "Destination": destination,
                    "Number of Stops": int(stops),
                    "Class": travel_class,
                    "Date": date_of_travel,
                    #"Total_Stopover_Time": int(stopover_time),
                    #"Departure_24hr": departure_time,
                    #"Arrival_24hr": arrival_time,
                    #"Arrival_Day_Offset": int(arrival_day_offset),
                    #"days_left": days_left
                }

                def time_to_minutes(time_str):
                    hours, minutes = map(int, time_str.split(':'))
                    return hours * 60 + minutes

                def preprocess_user_input(user_input):
                    user_df = pd.DataFrame([user_input])
                    user_df['Date'] = pd.to_datetime(user_df['Date'])
                    user_df['Month'] = user_df['Date'].dt.month
                    user_df['DayOfWeek'] = user_df['Date'].dt.dayofweek
                   # user_df['Departure_Minutes'] = user_df['Departure_24hr'].apply(time_to_minutes)
                   # user_df['Arrival_Minutes'] = user_df['Arrival_24hr'].apply(time_to_minutes)

                    for col in ['Airline', 'Source', 'Destination', 'Class']:
                        user_df[col + '_encoded'] = le_dict[col].transform(user_df[col])

                    features = ['Number of Stops', 
                                'Month', 'DayOfWeek', 
                                'Airline_encoded', 'Source_encoded', 'Destination_encoded', 'Class_encoded']
                    return user_df[features]

                processed_input = preprocess_user_input(user_input)
                predicted_price = model.predict(processed_input)[0]
                predictions[airline] = f"{predicted_price:.2f} CAD"

            return render(request, 'Pricepredictiormain/new_predict.html', {
                'predictions': predictions,
                'source': source,
                'destination': destination,
                'date_of_travel': date_of_travel,
               # 'departure_time': departure_time,
                #'arrival_time': arrival_time,
                #'stopover_time': stopover_time,
                'error_message': error_message
            })

    return render(request, 'Pricepredictiormain/profile.html', {
        'source_choices': source_choices,
        'destination_choices': destination_choices,
        'class_choices': class_choices,
        'total_stops_choices': total_stops_choices,
        'error_message': error_message
    })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'profile_edit.html', {'form': form})

