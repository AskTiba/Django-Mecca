import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseRedirect
from django.urls import reverse



# Base URL for the Thrones API
API_BASE_URL = "https://thronesapi.com/api/v2/Characters"

# Create your views here.
def home(request):
    # Fetch data from the Thrones API
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        characters = response.json()  # Convert the API response to JSON
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., no internet, API failure)
        characters = []
        print(f"Error fetching characters: {e}")

    # Pass the characters to the template
    return render(request, "posts/home.html", {"characters": characters})

def character_detail(request, character_id):
    try:
        # Fetch data for the specific character
        response = requests.get(f"{API_BASE_URL}/{character_id}")
        response.raise_for_status()
        character = response.json()
    except requests.exceptions.RequestException as e:
        character = None
        print(f"Error fetching character with ID {character_id}: {e}")

    # Handle case where character is not found
    if not character:
        return render(request, "404.html", status=404)

    return render(request, "posts/character_detail.html", {"character": character})

def global1(request):
    return render(request, "global.html",)

def quotes(request):
    return render(request, "posts/quotes.html",)

def play(request):
    return render(request, "posts/play.html",)
    
def flex(request):
    return render(request, "posts/flex.html",)
    
def grid(request):
    return render(request, "posts/grid.html",)
    
def google(request,id):
    url = reverse('character_detail', args = [id])
    return HttpResponseRedirect(url) 