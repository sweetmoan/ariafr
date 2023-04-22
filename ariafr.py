import requests
from math import radians, sin, cos, sqrt, asin
import json
import time
import threading
 
#telegram bot
bot_token = '5880937101:AAEaJH8sO1coKephJjf4Bq1d4WI1Q3FwJpY' 
chat_id = '6142127925'
#requests.get(bot_url)

N2YO_API_KEY = 'C8JULN-R755FA-KCYTK3-507U'
MY_LATITUDE = 49.682831
MY_LONGITUDE = -124.992531
THRESHOLD_DISTANCE = 1000  # Threshold distance in km for ISS passing over location

def Weather():
    print("running weather function")
    
    city_name='Tagbilaran City, PH'
    api_key = '30d4741c779ba94c470ca1f63045390a'
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={api_key}") 
    if weather_data.json()['cod'] == '404':
        print("Weather Function: No City Found")
    else:
        # Retrieve temperature data
        weather = weather_data.json()['weather'][0]['main']
        
        temp_f = weather_data.json()['main']['temp']
        temp_c = round((temp_f - 32) * 5/9)

        feels_like_f = weather_data.json()['main']['feels_like']
        feels_like_c = round((feels_like_f - 32) * 5/9)
        
        temp_min_f = weather_data.json()['main']['temp_min']
        temp_min_c = round((temp_min_f - 32) * 5/9)
        
        temp_max_f = weather_data.json()['main']['temp_max']
        temp_max_c = round((temp_max_f - 32) * 5/9)

        humidity = weather_data.json()['main']['humidity']  # Retrieve humidity data
        precipitation = weather_data.json()['weather'][0]['description']  # Retrieve precipitation data
        
        dew_point_f = temp_f - ((100 - humidity)/5)  # Retrieve dew_point data
        dew_point_c = round((dew_point_f - 32) * 5/9)

        pressure = weather_data.json()['main']['pressure']  # Retrieve pressure data
        
        visibility_meters = weather_data.json()['visibility']  # Retrieve visibility data
        visibility_km = visibility_meters / 1000
        
        wind_speed_mph = weather_data.json()['wind']['speed']  # Retrieve wind_speed data
        wind_speed_ms = wind_speed_mph * 0.44704
        wind_speed_rounded = round(wind_speed_ms, 1)
        
        wind_direction = weather_data.json()['wind']['deg']  # Retrieve wind_direction data

        # Convert the wind direction angle to a cardinal direction
        if 348.75 <= wind_direction < 11.25:
            direction = "N"
        elif 11.25 <= wind_direction < 33.75:
            direction = "NNE"
        elif 33.75 <= wind_direction < 56.25:
            direction = "NE"
        elif 56.25 <= wind_direction < 78.75:
            direction = "ENE"
        elif 78.75 <= wind_direction < 101.25:
            direction = "E"
        elif 101.25 <= wind_direction < 123.75:
            direction = "ESE"
        elif 123.75 <= wind_direction < 146.25:
            direction = "SE"
        elif 146.25 <= wind_direction < 168.75:          
            direction = "SSE"
        elif 168.75 <= wind_direction < 191.25:
            direction = "S"
        elif 191.25 <= wind_direction < 213.75:
            direction = "SSW"
        elif 213.75 <= wind_direction < 236.25:
            direction = "SW"
        elif 236.25 <= wind_direction < 258.75:
            direction = "WSW"
        elif 258.75 <= wind_direction < 281.25:
            direction = "W"
        elif 281.25 <= wind_direction < 303.75:
            direction = "WNW"
        elif 303.75 <= wind_direction < 326.25:
            direction = "NW"
        elif 326.25 <= wind_direction < 348.75:
            direction = "NNW"
        else:
            direction = "Unknown"

        message = f"Weather Information for {city_name}\n"
        message += f"{temp_min_c} °C\n"
        message += f"Feels Like: {feels_like_c} °C {precipitation}\n"
        message += f"Wind Speed: {wind_speed_rounded} m/s {direction}\n"
        message += f"Humidity: {humidity}%\n"
        message += f"Dew Point: {dew_point_c} °C\n"
        message += f"Visibility: {visibility_km} km"

        while True:
            bot_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
            requests.get(bot_url)
            time.sleep(10800)#3hrs 
            
def calculate_distance(self, lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Apply haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

def Iss():
    print("running iss function")
    
    while True:
        try:
            response = requests.get('https://api.n2yo.com/rest/v1/satellite/positions/25544/0/0/0/1/&apiKey={}'.format(self.N2YO_API_KEY))
            data = json.loads(response.text)
            iss_latitude = float(data['positions'][0]['satlatitude'])
            iss_longitude = float(data['positions'][0]['satlongitude'])
        except:
            print("iss error!")
            iss_message = "ISS Function: Error! Might exceed the maximum request per hour on the API"
            bot_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={iss_message}'
            requests.get(bot_url)
            time.sleep(4200) # Sleep for 120 seconds and try again
            continue

        iss_longitude_rounded = round(iss_longitude, 2)
        iss_latitude_rounded = round(iss_latitude, 2)

        distance = self.calculate_distance(self.MY_LATITUDE, self.MY_LONGITUDE, iss_latitude, iss_longitude)
        
        if distance <= self.THRESHOLD_DISTANCE:
            iss_message = f"Current place of ISS: LAT: {iss_latitude_rounded}, LNG: {iss_longitude_rounded}. The ISS will be passing within {self.THRESHOLD_DISTANCE} km of your location"
            bot_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={iss_message}'
            requests.get(bot_url)
            time.sleep(120)
        else:
            iss_message = f"Current place of ISS: LAT: {iss_latitude_rounded}, LNG: {iss_longitude_rounded}. The ISS won't be passing within your location"
            bot_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={iss_message}'
            requests.get(bot_url)
            time.sleep(120)
            
if __name__ == '__main__':
    # Create separate threads for function1 and function2
    thread1 = threading.Thread(target=Weather)
    thread2 = threading.Thread(target=Iss)
    
    # Start the threads
    thread1.start()
    thread2.start()
    
    # Wait for the threads to finish
    thread1.join()
    thread2.join()

    
