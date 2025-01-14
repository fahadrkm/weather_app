import requests
from django.shortcuts import render

def index(request):
    if request.method == "POST":
        city = request.POST['city']  # City entered by the user

        # API keys for Weather and Unsplash APIs
        weather_api_key = 'da6ae46afce5bd10883ca855b0c20203'  # Replace with your OpenWeatherMap API Key
        image_api_key = '3Zb0JdD9xnOTt1Xl428COHNDzWrZvH_tnRw_0nbpbn4'  # Replace with your Unsplash Access Key


        # API URLs
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api_key}'
        image_url = f'https://api.unsplash.com/search/photos?query={city}&client_id={image_api_key}'
        wikipedia_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{city}'

        # API Requests
        weather_response = requests.get(weather_url)
        image_response = requests.get(image_url)
        wikipedia_response = requests.get(wikipedia_url)

        # Handle API responses
        if weather_response.status_code == 200 and wikipedia_response.status_code == 200:
            weather_data = weather_response.json()
            wiki_data = wikipedia_response.json()
            city_info = wiki_data.get('extract', "No description available.")  # Get city summary

            # Fetch city image (if available)
            if image_response.status_code == 200:
                image_data = image_response.json()
                city_image = image_data['results'][0]['urls']['regular'] if image_data['results'] else None
            else:
                city_image = None

            context = {
                'weather': weather_data,
                'city_image': city_image,
                'city_info': city_info
            }
        else:
            context = {'error': f"Could not retrieve data for '{city}'."}

        return render(request, 'index.html', context)

    return render(request, 'index.html')
