from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
#import messages
from django.contrib import messages
# Create your views here.

def index(request):
    # Load the JSON file
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    currency_data = []
    with open(file_path) as json_file:
        data = json.load(json_file)
        # import pdb; pdb.set_trace()
        for k,v in data.items():
            currency_data.append({'name': k, 'value': v})
    exists= UserPreference.objects.filter(user=request.user).exists()
    user_preference = None
    if exists:
        user_preference = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':
        
        # Pass the data to the template
        return render(request, 'preferences/index.html', {'currencies': currency_data,'user_preference':user_preference})
    
    elif request.method == 'POST':
        #Get the currency from the form
        currency = request.POST['currency']
        if exists:
            # Update the user preferences
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved',fail_silently=True)
        return render(request, 'preferences/index.html', {'currencies': currency_data,'user_preference':user_preference})
        
            