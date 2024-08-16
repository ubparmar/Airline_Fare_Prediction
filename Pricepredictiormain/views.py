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
from .forms import ContactForm  
from .models import Contact

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
                
            }

            def time_to_minutes(time_str):
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes

            def preprocess_user_input(user_input):
                user_df = pd.DataFrame([user_input])
                user_df['Date'] = pd.to_datetime(user_df['Date'])
                user_df['Month'] = user_df['Date'].dt.month
                user_df['DayOfWeek'] = user_df['Date'].dt.dayofweek
              

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


def about(request):
    user_count = User.objects.count()
    context = {
        'user_count': user_count
    }
    return render(request, 'Pricepredictiormain/about.html',context)

def contact_view(request):
    if request.method == 'POST':
        # Process the form submission
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save the contact response to the database
        Contact.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )

        # Redirect to the contact page with a success query parameter
        return redirect('contact')  # Update to your contact URL name

    # Fetch all contact responses to display
    contact_responses = Contact.objects.all()
    success = 'success' in request.GET  # Check if 'success' query parameter is present
    return render(request, 'contact.html', {'contact_responses': contact_responses, 'success': success})

    # Fetch all contact responses to display
    contact_responses = Contact.objects.all()
    return render(request, 'contact.html', {'contact_responses': contact_responses})
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Now You May Login')
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
                }

                def time_to_minutes(time_str):
                    hours, minutes = map(int, time_str.split(':'))
                    return hours * 60 + minutes

                def preprocess_user_input(user_input):
                    user_df = pd.DataFrame([user_input])
                    user_df['Date'] = pd.to_datetime(user_df['Date'])
                    user_df['Month'] = user_df['Date'].dt.month
                    user_df['DayOfWeek'] = user_df['Date'].dt.dayofweek
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

