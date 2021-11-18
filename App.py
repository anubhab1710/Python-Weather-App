from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
import requests
from PIL import Image, ImageTk

app = Tk()
app.title("Weather App")
app.geometry('350x250')

url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather)
        return final
    else:
        return None


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        # image['bitmap'] = 'icons/{}@2x.gif'.format(weather[4])
        # img["file"] = '\Desktop\Weather App Project\icons\{}@2x.png'.format(weather[4])
        temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[5]
    else:
        messagebox.showerror('Error', 'Cannot Find City {}'.format(city))


city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text='Get Weather Info', width=15, command=search)
search_btn.pack()

location_lbl = Label(app, text='', font=('Poppins', 20, 'bold'))
location_lbl.pack()

image = Label(app, bitmap='')
image.pack()

temp_lbl = Label(app, text='', font=("Helvetica", 22, 'bold'))
temp_lbl.pack()

weather_lbl = Label(app, text='', font=("Calibri", 22, 'italic'))
weather_lbl.pack()

app.mainloop()
