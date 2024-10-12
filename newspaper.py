import imagewriter
from datetime import date
import calendar

iw = imagewriter.Imagewriter('/dev/ttyS0')
iw.slashedzero(True)

##### Header

dayofweek = calendar.day_name[date.today().weekday()]
title = "Justin's News"
datestring = date.today().strftime("%d %B %Y")
leftspaces = 28-(3+dayofweek.__len__())
rightspaces = 80-52-(1+datestring.__len__())

iw.linefeed(-2)

iw.boldface(True)
iw.repeatchar(b'\xd6',80)
iw.carriagereturn()
iw.linefeed()

iw.printchar(b'\xd6')
iw.printstr(dayofweek)
iw.repeatchar(b'\x20',leftspaces)
iw.doublewidth(True)
iw.printstr(title)
iw.doublewidth(False)
iw.repeatchar(b'\x20',rightspaces)
iw.printstr(datestring)
iw.printchar(b'\xd6')
iw.carriagereturn()
iw.linefeed()

iw.repeatchar(b'\xd6',80)
iw.carriagereturn()
iw.linefeed()
iw.boldface(False)

iw.linefeed(2)

def sectionheader(section: str):
    iw.boldface(True)
    iw.printchar(b'\xd6\x20')
    iw.printstr(section)
    iw.carriagereturn()
    iw.linefeed()

    iw.repeatchar(b'\xd6', section.__len__()+2)
    iw.carriagereturn()
    iw.linefeed()
    iw.boldface(True)

##### Weather Section

weather_codes = { 
    0: "Clear",
    1: "Mostly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    56: "Freezing Drizzle",
    57: "Freezing Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Freezing Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    77: "Snow",
    80: "Showers",
    81: "Showers",
    82: "Showers",
    85: "Snow Showers",
    86: "Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm",
    99: "Thunderstorm" }

# Weather Header
sectionheader("Weather")

import openmeteo_requests
import pandas as pd

openmeteo = openmeteo_requests.Client()

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 43.9441,
	"longitude": -90.8129,
	"current": ["temperature_2m", "weather_code"],
	"hourly": ["temperature_2m", "weather_code"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset"],
	"wind_speed_unit": "kn",
	"precipitation_unit": "inch",
	"timezone": "America/Chicago",
	"temporal_resolution": "hourly_3"
}
responses = openmeteo.weather_api(url, params=params)

response = responses[0]

current = response.Current()
current_temp = current.Variables(0).Value()
current_weather_code = current.Variables(1).Value()

currentstr = "Current: " + f"{current_temp:.1f}" + "c " + weather_codes[current_weather_code]
iw.printstr(currentstr)
iw.carriagereturn()
iw.linefeed()

daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_max = daily.Variables(1).ValuesAsNumpy()
daily_min = daily.Variables(2).ValuesAsNumpy()

todaystr = "Today: " + weather_codes[daily_weather_code[0]] + f" High: {daily_max[0]:.1f}c Low: {daily_min[0]:.1f}c" 
tomorrowstr = "Tomorrow: "+ weather_codes[daily_weather_code[1]] + f" High: {daily_max[1]:.1f}c Low: {daily_min[1]:.1f}c" 

iw.printstr(todaystr)
iw.carriagereturn()
iw.linefeed()
iw.printstr(tomorrowstr)
iw.carriagereturn()
iw.linefeed()

iw.linefeed(2)

#### News Headlines
import feedparser

sectionheader("News Headlines")

wapo = feedparser.parse("https://feeds.washingtonpost.com/rss/national?itid=lk_inline_manual_31")
for n in wapo.entries.__len__():
    iw.boldface(True)
    iw.printstr(wapo.entries[n].title)
    iw.carriagereturn()
    iw.linefeed()
    iw.boldface(False)
    iw.printstr(wapo.entries[n].description)
    iw.carriagereturn()
    iw.linefeed(2)


#### End

iw.formfeed()