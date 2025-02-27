import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


# OpenWeatherMap API Key
API_KEY = "72bbb6e6a585e73075962aaee00347d5"

# Load all cities from a dataset
df = pd.read_csv(r"C:\Users\tanni\Downloads\worldcities.csv")  # Replace with your city dataset file
CITIES = df["city"].tolist()  # Limiting to 50 cities for testing

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"]
        }
    return None
weather_data = [fetch_weather(city) for city in CITIES if fetch_weather(city)]


def generate_graph(weather_data, param, filename, ylabel, color):
    cities = [d["city"] for d in weather_data]
    values = [d[param] for d in weather_data]

    plt.figure(figsize=(15, 7))
    plt.bar(cities, values, color=color)
    plt.xticks(rotation=90)  # Rotate city names for better visibility
    plt.xlabel("Cities")
    plt.ylabel(ylabel)
    plt.title(f"{param.capitalize()} Data Across the World")

    filepath = r"staticC:\Users\tanni\OneDrive\Desktop\WEATHER-APP\graph"
    plt.savefig(filepath, format="png",)
    plt.close()
    return filepath

@app.route("/")
def home():
    return render_template("weather.html")

@app.route("/temperature")
def temperature():
    weather_data = [fetch_weather(city) for city in CITIES if fetch_weather(city)]
    graph_url = generate_graph(weather_data, "temp", "temperature.png", "Temperature (°C)", "red")
    return render_template("temperature.html", graph_url=graph_url)

@app.route("/humidity")
def humidity():
    weather_data = [fetch_weather(city) for city in CITIES if fetch_weather(city)]
    graph_url = generate_graph(weather_data, "humidity", "humidity.png", "Humidity (%)", "blue")
    return render_template("humidity.html", graph_url=graph_url)

@app.route("/wind")
def wind():
    weather_data = [fetch_weather(city) for city in CITIES if fetch_weather(city)]
    graph_url = generate_graph(weather_data, "wind_speed", "wind.png", "Wind Speed (m/s)", "green")
    return render_template("wind.html", graph_url=graph_url)

@app.route("/pressure")
def pressure():
    weather_data = [fetch_weather(city) for city in CITIES if fetch_weather(city)]
    graph_url = generate_graph(weather_data, "pressure", "pressure.png", "Pressure (hPa)", "purple")
    return render_template("pressure.html", graph_url=graph_url)

if __name__ == "__main__":
    app.run(debug=True)
