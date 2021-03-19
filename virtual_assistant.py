'''
    Description:
    Create your own virtual assistant with python.

    Author: AlejandroV
    Version: 1.0
    Video: https://youtu.be/8WKjX0dbh4E
'''
import speech_recognition as sr
import pyttsx3
import pywhatkit
import urllib.request
import json
import datetime
import wikipedia

# name of the virtual assistant
name = 'cortana'

# your api key
key = 'YOUR_API_KEY_HERE'

# the flag help us to turn off the program
flag = 1

listener = sr.Recognizer()

engine = pyttsx3.init()

# get voices and set the first of them
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# editing default configuration
engine. setProperty('rate', 178)
engine.setProperty('volume', 0.7)

def talk(text):
    '''
        here, virtual assistant can talk
    '''
    engine.say(text)
    engine.runAndWait()

def listen():
    '''
        The program recover our voice and it sends to another function
    '''
    flag = 1
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()
            
            if name in rec:
                rec = rec.replace(name, '')
                flag = run(rec)
            else:
                talk("Vuelve a intentarlo, no reconozco: " + rec)
    except:
        pass
    return flag

def run(rec):
    '''
        All the actions that virtual assistant can do
    '''
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    elif 'cuantos suscriptores tiene' in rec:
        name_subs = rec.replace('cuantos suscriptores tiene', '')
        data = urllib.request.urlopen(f'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={name_subs.strip()}&key={key}').read()
        subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
        talk(name_subs + " tiene {:,d}".format(int(subs)) + " suscriptores!")
    elif 'hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        wikipedia.set_lang("es")
        info = wikipedia.summary(order, 1)
        talk(info)
    elif 'exit' in rec:
        flag = 0
        talk("Saliendo...")
    else:
        talk("Vuelve a intentarlo, no reconozco: " + rec)
    return flag

while flag:
    flag = listen()