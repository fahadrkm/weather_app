import requests
from django.shortcuts import render

def index(request):
    if request.method == "POST":
        city = request.POST['city']
        weather_api_key = 'da6ae46afce5bd10883ca855b0c20203'  # Replace with your OpenWeatherMap API Key
        image_api_key = '3Zb0JdD9xnOTt1Xl428COHNDzWrZvH_tnRw_0nbpbn4'  # Replace with your Unsplash Access Key

        # Weather API URL
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api_key}'
        weather_response = requests.get(weather_url)
        
        # Unsplash API URL for City Image
        image_url = f'https://api.unsplash.com/search/photos?query={city}&client_id={image_api_key}'
        image_response = requests.get(image_url)
        
        # Check if both requests are successful
        if weather_response.status_code == 200 and image_response.status_code == 200:
            weather_data = weather_response.json()
            image_data = image_response.json()

            # Extract the first image URL from Unsplash API response
            if image_data['results']:
                city_image = image_data['results'][0]['urls']['regular']  # Get the first image
            else:
                city_image = None  # Fallback if no image is found
            
            context = {'weather': weather_data, 'city_image': city_image}
        else:
            context = {'error': f"Could not retrieve data for '{city}'."}
        
        return render(request, 'index.html', context)
    
    return render(request, 'index.html')
