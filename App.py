from dotenv import load_dotenv
from tkinter import Button, Label, Tk, PhotoImage, StringVar, Entry
import requests, os
from PIL import Image, ImageTk

load_dotenv()
api_key = os.getenv('key')

app = Tk()
app.title("Weather App")
app.geometry('350x250')
app.resizable(0, 0)
color = '#fff'
titlebar_icon = PhotoImage(file='icons/back.png')
app.configure(bg=color)
app.iconphoto(False, titlebar_icon)

url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

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
    global img
    city = city_text.get()
    try:
        weather = get_weather(city)
        if weather:
            location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
            img = PhotoImage(file='icons/{}@2x.png'.format(weather[4]))
            image['image'] = img
            temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(
                weather[2], weather[3])
            weather_lbl['text'] = weather[5]
        else:
            messagebox.showerror('Error', 'Cannot Find City {}'.format(city))
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Error', 'Connection error')


city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text='Get Weather Info', width=15, command=search)
search_btn.configure(bg=color)
search_btn.pack()

location_lbl = Label(app, text='', font=('Poppins', 20, 'bold'))
location_lbl.configure(bg=color)
location_lbl.pack()

image = Label(app, image='')
image.configure(bg=color)
image.pack()

temp_lbl = Label(app, text='', font=("Helvetica", 22, 'bold'))
temp_lbl.configure(bg=color)
temp_lbl.pack()

weather_lbl = Label(app, text='', font=("Calibri", 22, 'italic'))
weather_lbl.configure(bg=color)
weather_lbl.pack()

if __name__ == '__main__':
    app.mainloop()