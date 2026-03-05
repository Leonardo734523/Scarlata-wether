## 🌦️ Scarlata Weather – Django Weather Forecast Website

A Django-based weather application that uses the OpenWeatherMap API to retrieve and display a 5-day weather forecast for U.S. locations.

Users can:

Search for a city and state

Select from matching locations

View a detailed 5-day weather forecast including temperature, feels-like temperature, description, and wind speed



---

🚀 Features

🌍 City + State geolocation search

📅 5-day weather forecast

🌡️ Temperature (Imperial units)

💨 Wind speed data

🧾 Clean data organization using Python dataclasses

⚠️ Custom API error handling with user-friendly messages

🔐 Secure API key management using environment variables



---

🛠️ Tech Stack

Backend Framework: Django

Language: Python 3

API Provider: OpenWeatherMap

Environment Management: python-dotenv

HTTP Requests: requests

---

⚙️ Installation & Setup

1️⃣ Clone the repository


2️⃣ Create and activate a virtual environment

python -m venv venv

source venv/bin/activate  # Mac/Linux

venv\Scripts\activate     # Windows

3️⃣ Install dependencies

pip install django requests python-dotenv

4️⃣ Create an OpenWeatherMap API Key

1. Sign up at OpenWeatherMap


2. Generate a free API key


3. Create a env file for the API key:



name env file: api-key.env

Inside that file:

APIKEY=your_api_key_here

⚠️ Make sure this file is in the same directory as main.py.


---

▶️ Running the Server

python manage.py runserver

Visit:

http://127.0.0.1:8000/


---

🧠 Core Logic

main.py functions:

🔹 get_geocoding

Takes city and state input

Calls OpenWeatherMap Geocoding API

Returns matching locations


🔹 get_weather_forecast

Takes latitude & longitude

Calls OpenWeatherMap 5-day forecast API

Returns a structured 5-day weather forecast response

🔹 organize data functions

organize_geocoding -> Takes data from get_geocoding and then organizes it into dataclasses stored in a list

organize_weather ->  Takes data from get_weather_forecast and then organizes it into dataclasses stored in a list

🔹 json_to_py

Accepts a raw JSON response and status code

Returns parsed Python data when successful

Returns an error code if an error occurred

🔹 get_api_key

Retrieves the API key from api-key.env

---

🛡️ Error Handling

Custom exceptions are implemented for:

401 → Invalid API key

404 → Invalid location

429 → Too many requests

500–504 → API provider issues

100 → Empty JSON

101 → JSON conversion error


All errors are displayed to the user through a dedicated error template.


---

🔐 Environment Variables

The project securely loads the API key using: 

from dotenv import load_dotenv

This protects the API key.

---

📁 Project structure

```python
weather_project/
│
├── frontend                # Django app, manages the front end and HTTP requests
│   ├── templates/               # HTML templates directory
│   │   ├── home.html            # Search form page
│   │   ├── select_location.html                 # Location selection page
│   │   ├── weather.html                         # Weather forecast display page
│   │   ├── inout-error.html                     # Inout error message page
│   │   └── server-error.html                    # Server error message page
│   ├── views.py                 # Django view controllers (handle requests/responses, render templates)
├── api-key.env             # API key storage (gitignored)
├── main.py                 # Core logic and API functions (geocoding, weather, json_to_py, organize functions)
└── manage.py               # Django management script

```
---

📌 Future Improvements

Add metric/imperial toggle

Improve UI styling

Add caching to reduce API calls

Deploy to production
