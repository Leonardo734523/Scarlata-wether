import requests, os
from dotenv import load_dotenv
from dataclasses import dataclass



class api_error_handling(Exception):

    # You can find notes on the different errors in the open weather map FAQ: https://openweathermap.org/faq

    # Custom expression for handling open weather API errors

    def __init__(self, API_status_code):
        self.API_status_code = API_status_code
        super().__init__(self.get_message())



    def get_message(self) :
        match self.API_status_code :
            case 401:
                return("(Error 401) There might be a problem with the API key")
            case 404:
                return("(Error 404) Please input a valid location") #  You can also get the error if the format of your API request is incorrect
            case 429:
                return("(Error 429) ScarlataWeather.com is down due to heavy traffic")
            case 400000:
                return("(Error 400000) The information you are requesting is outside of the API subscription")
            case 500 | 502 | 503 | 504: # If one of these errors occur, please contact Open Weather Map
                return(f"(Error {self.API_status_code}) The API Provider Open weather Map is experiencing technical difficulties")
            case 100:
                return("(Error 100) Json file valid, but empty")
            case 101:
                return("(Error 101) Failed to convert json too py")
            case 102:
                return("(Error 102) API response is missing key value pairs")
            case 103:
                return("(Error 103) The values in the key value pairs are not the correct data type")
            case 104:
                return("(Error 104) The data in the key value pairs is invalid but the data types are correct")
            case _:
                return(f"(Error {self.API_status_code}) Unknown error occurred.")



class API_key_retrieval_error(Exception):

    def __init__(self, message="Failed to retrieve API key from env file, please make sure you have the env file in the same folder"):
        super().__init__(message)



@dataclass
class LocationData:
    name: str
    state: str
    country: str
    lat: float
    lon: float



@dataclass
class ForecastData:
    time: str
    temp: float
    feels_like: float
    description: str
    wind: float
    


def get_api_key():

    load_dotenv("api-key.env")
    APIKEY = os.getenv("APIKEY") or os.environ.get("APIKEY")
    if not APIKEY:
        raise API_key_retrieval_error()
    else:
        return(APIKEY)
    


def json_to_py(raw, code): # Returns status code instead of data if the code is not 200

    if not code == 200:
        return code
    try:
        py = raw.json()
    except ValueError:
        return 101
    if not py:
        return 100
    
    return py



def get_geocoding(city_name, state_code, unit_type) :

    # Open Weather Map geocoding API document: https://openweathermap.org/api/geocoding-api

    # Makes a API call to get geographical information

    API_KEY = get_api_key()

    country_code = "US"

    units = unit_type
    
    URL_geocoding = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={20}&appid={API_KEY}&units={units}"

    raw_geocoding = requests.get(URL_geocoding)
    geocoding_status_code = raw_geocoding.status_code 

    geocoding = json_to_py(raw_geocoding, geocoding_status_code)

    return geocoding
  

  
def organize_geocoding (geocoding):

    # Organizes geocoding's into LocationData

    organized_geocoding_results = []

    for location_info in geocoding:
        
        try:
            organized_geocoding_results.append(LocationData(
                location_info["name"],
                location_info["state"],
                location_info["country"],
                location_info["lat"],
                location_info["lon"]
                ))
        except KeyError:
            raise api_error_handling(102)
        except TypeError:
            raise api_error_handling(103)
        except ValueError:
            raise api_error_handling(104)

    return organized_geocoding_results



def get_weather_forecast(lat, lon):

    # Open Weather Map 5 day weather forecast API document: https://openweathermap.org/forecast5

    # Makes a API call to get the 5 day weather forecast

    units = "imperial"

    API_KEY = get_api_key()

    URL_weather_forecast = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"

    raw_weather = requests.get(URL_weather_forecast)
    weather_status_code = raw_weather.status_code

    weather = json_to_py(raw_weather, weather_status_code)

    return weather



def organize_weather(weather):

    # Organizes data into ForecastData

    clean_forecasts = []

    for f in weather["list"]:

        try:
            clean_forecasts.append(
                ForecastData(
                    time=f["dt_txt"],
                    temp=f["main"]["temp"],
                    feels_like=f["main"]["feels_like"],
                    description=f["weather"][0]["description"],
                    wind=f["wind"]["speed"],
                    ))
        except KeyError:
            raise api_error_handling(102)
        except TypeError:
            raise api_error_handling(103)
        except ValueError:
            raise api_error_handling(104)

    
    return clean_forecasts