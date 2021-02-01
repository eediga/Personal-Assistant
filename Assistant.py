import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import json
import geocoder


g = geocoder.ip('me')

listener = sr.Recognizer()
engine = pyttsx3.init()
engine.say('Hi Eashwar')
engine.runAndWait()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()

def weather():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
              str(g.latlng[0]) + "&lon=" + str(g.latlng[1])

    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        talk(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
        talk('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')
        print('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')
        talk('weather type ' + weather_desc['main'])
        talk('Wind speed is ' + str(wind['speed']) + ' metre per second')
        talk('Temperature: ' + str(main['temp']) + 'degree celcius')
        talk('Humidity is ' + str(main['humidity']))



def talk_news():
    url = ('http://newsapi.org/v2/top-headlines?'
           'sources=bbc-news&'
           'apiKey=10790965ee1541dd96354d461fb2b65f')
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict['articles']
    talk('Eashwar the Source is: The Times Of India')
    talk('Todays Headlines are..')
    for index, articles in enumerate(arts):
        talk(articles['title'])
        print(articles['title'])
        if index == len(arts)-1:
            break
        talk('Moving on the next news headline..')
    talk('These were the top headlines, Have a nice day Sir!!..')

def getNewsUrl():
    return 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=9b17ea366f744f5eadbbd8dc545e3f79'



def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('eashwar please wait while the song is playing ' + song )
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Eashwar current time is ' + time)
    elif 'date' in command:
        year = int(datetime.datetime.now().year)
        month = int(datetime.datetime.now().month)
        date = int(datetime.datetime.now().day)
        talk("the current date is")
        talk(date)
        talk(month)
        talk(year)
        print(date, month, year)



    elif 'open youtube' in command:
        webbrowser.open("www.youtube.com")
        talk('Eashwar please wait while i am  opening youtube')
    elif 'open facebook' in command:
        webbrowser.open("www.facebook.com")
        talk('Eashwar please wait while i am  opening facebook')
    elif 'open google' in  command:
        talk('Eashwar what can i search in google')
        cm = take_command().lower()
        webbrowser.open(f"{cm}")
        talk('Eashwar please wait while i am  opening google')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        weather()
    elif 'Hi'  in command:
        talk('Thank you eashwar i am fine how may i help you?')
    elif 'news' in command:
        talk('Ofcourse Eashwar..')
        talk_news()
        talk('Eashwar Do you want to read the full news...')
        test = take_command()
        if 'yes' in test:
            talk('Ok Eashwar, Opening browser...')
            webbrowser.open(getNewsUrl())
            talk('You can now read the full news from this website.')
        else:
            talk('No Problem Eashwar')


    elif 'how are you' in command:
        talk('Thank you eashwar i am fine how may i help you?')

    if 'jarvis are you there' in command:
        talk("Yes Eashwar, at your service")


    elif 'open notepad' in command:
        npath = "C:\\WINDOWS\\system32\\notepad.exe"
        os.startfile(npath)
        talk('Eashwar please wait while i am  opening notepad')
    elif 'open command prompt' in command:
        os.system("start cmd")
    elif 'who is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'close notepad' in  command:
        os.system("taskkill /f /im notepad.exe")
        talk('Eashwar i have closed notepad')


while True:
    run_alexa()

