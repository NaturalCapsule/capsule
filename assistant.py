import speech_recognition as sr
import subprocess, shlex
from app_info import *
import os
recognizer = sr.Recognizer()

apps = {}

ap = get_app_info()
for name, exec, icon in get_app_info():
    print(name.lower())
    apps[name.lower()] = exec



def listen_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            os.system('clear')
            print(f"You said: {command.lower()}")
            return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return ""

def execute_command(command):
    if command in list(apps.keys()):
        cmd = apps.get(command)
        if command == 'steam':
            cmd = apps.get('steam (runtime)')
        print(cmd)
        cmd = shlex.split(cmd)
        print(cmd)
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, cwd=os.path.expanduser("~"))
    else:
        pass

while True:
    command = listen_command()
    if command:
        execute_command(command)