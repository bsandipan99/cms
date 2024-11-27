from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm
import requests
from contents.models import Post
from django.contrib.auth import logout
import os

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Send request to /api/token/ endpoint
        token_url = os.getenv('TOKEN_URL', 'http://localhost:8000/api/token/')
        response = requests.post(token_url, data={'username':username, 'password':password})

        if response.status_code == 200:
            tokens = response.json()

            # Save the tokens in the session
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']
            return redirect('dashboard')
        
        else:
            return render(request,'users/login.html',{'error': 'Invalid username or password'})

    return render(request,'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    form = ProfileForm()
    return render(request, 'users/registration.html', {'form': form})

def refresh(request):
    refresh_token = request.session['refresh_token']

    if not refresh_token:
        return redirect('login')

    # Send the refresh token to fetch access token
    refresh_url = os.getenv('REFRESH_URL', 'http://localhost:8000/api/token/refresh/')
    response = requests.post(refresh_url,data={'refresh':refresh_token})

    if response.status_code == 200:
        tokens = response.json()

        # Store the new access token
        request.session['access_token'] = tokens['access']
        return redirect('dashboard')
    
    else:
        return redirect('login')
