# Imports
import datetime
import operator
import os
import sys
import webbrowser
import instaloader
import psutil
from requests import get
import cv2
import pyttsx3
import speech_recognition as sr
import wikipedia
import pyjokes
import pyautogui
import time
import PyPDF2
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from celiagui import Ui_CeliaGui
from bs4 import BeautifulSoup as bs
from pywikihow import search_wikihow
import speedtest

engine = pyttsx3.init()
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', en_voice_id)
engine.setProperty('rate', 173)


def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def towish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour<=12:
        speak("Good Morning sir")
    elif hour>12 and hour<=16:
        speak("Good Afternoon sir")
    elif hour>16 and hour<=18:
        speak("Good Evening sir")
    else:
        speak("Good Night sir")
    speak("I am Celia how can i help you sir?")

def news():
    mainurl = "https://newsapi.org/v2/top-headlines?sources=techcrunch&apikey=9b4efd58c40241e18fb26901048dd769"
    mainpage = get(mainurl).json()
    articles = mainpage['articles']
    head = []
    day = ['first','second','third','fourth','fifth','sixth','seventh',"eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar['title'])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")

def pdf_reader():
    speak("Please tell me the pdf name")
    name = input("Enter the name: ")
    book = open(f"{name}.pdf","rb")
    pdf = PyPDF2.PdfFileReader(book)
    pages = pdf.numPages
    speak(f"Total number of pages in the pdf are {pages}")
    speak("Which page do you want me to read")
    n = int(input("Enter the page number : "))
    page =pdf.getPage(n)
    text = page.extractText()
    speak(text)

        
    

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.tasks()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening....")
            r.pause_threshold = 1
            audio = r.listen(source,timeout=1,phrase_time_limit=5)
            try:
                print("Recognizing....")
                self.query = r.recognize_google(audio, language='en-in')
                print(f"User: {self.query} ")
            except:
                return ""

        return self.query.lower()

    def sleep(self):
        a = True
        while a:
            x = self.listen()
            if "wake up" in x:
                a = False
        speak("Hi sir welcome back")

    def tasks(self):
        towish()
        while True:
            self.query = self.listen()
            if "open notepad" in self.query:
                path = "C:\\Windows\\notepad.exe"
                os.startfile(path)
            
                speak("Anything else sir")
            
            elif "open cmd" in self.query:
                os.system("start cmd")

                speak("Anything else sir")
            
            elif "open camera" in self.query:
                cap = cv2.VideoCapture()
                while True:
                    ret,img = cap.read()
                    cv2.imshow('Web Cam',img)
                    k = cv2.waitKey(58)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
        
                speak("Anything else sir")
            
            elif "ip address" in self.query:
                ip = get("https://api.ipify.org").text
                speak(f"Your ip address is {ip}")
            
                speak("Anything else sir")
            
            elif "wikipedia" in self.query:
                speak("Searching in wikipedia...")
                self.query = self.query.replace("wikipedia","")
                results = wikipedia.summary(self.query,sentence=2)
                speak("According to wikipedia")
                speak(results)
            
                speak("Anything else sir")
            
            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")
            
                speak("Anything else sir")
            
            elif "open google" in self.query:
                speak("What should i search in google")
                cmd = self.listen()
                webbrowser.open(cmd)

                speak("Anything else sir")
            
            elif "tell me a joke" in  self.query:
                jokes = pyjokes.get_joke()
                speak(jokes)

                speak("Anything else sir")
            
            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:
                os.system("shutdown /r /t 5")

            elif "go to sleep" in self.query:
                os.system("rundl32.exe powrprof.dll,SetSuspendState 0,1,0")
            
            elif "switch the window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
            
                speak("Anything else sir")
            
            elif "tell me news" in self.query:
                speak("Please wait sir, I am fetching the news")
                news()
            
                speak("Anything else sir")
            
            elif "get my location" in self.query:
                speak("Let me check")
                try:
                    ip = get("https://api.ipify.org").text
                    geo_req = get(f"https://get.geojs.io/v1/ip/geo/{ip}.json")
                    geodata = geo_req.json()
                    speak(f"Sir i am not sure,but i think we are in {geodata['longitude']} longitude and {geodata['latitude']} latitude of {geodata['country']} country")
                except Exception as e:
                    speak("Sorry sir i think we lost network")
                    pass
            
                speak("Anything else sir")
            
            elif "insta profile" in self.query:
                speak("please enter username correctly")
                name = input("Enter the username: ")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Here is the profile of the user{name}")
                time.sleep(5)
                speak("Would you like to download the profile pic")
                cond = self.listen()
                if "yes" in cond:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name,profile_pic_only=True)
                    speak("Downloaded the profile pic sir")
                else:
                    pass

                speak("Anything else sir")
            
            elif "take a screen shot" in self.query:
                speak("Please say the name of the file to save as")
                name = self.listen()
                speak("Hold on the screen to capture the shot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("Screen shot saved sir")
            
                speak("Anything else sir")
            
            elif "read pdf" in self.query:
                pdf_reader()

                speak("Anything else sir")
            
            elif "hide all files" in self.query:
                speak("Hiding the files..")
                os.system("attrib +h /s /d")
                speak("All files of the folder are hidden")
            
                speak("Anything else sir")
            
            elif "visible for everyone" in self.query:
                speak("Making all the files visible")
                os.system("attrib -h /s /d")
            
                speak("All the files are now visible to everyone")

                speak("Anything else sir")
            

            elif "do some calculations" in self.query:
                speak("Say what to calculate for example 3 plus 3")
                mystr = self.listen()
                def op(op):
                    return{
                        "+":operator.add,
                        "-":operator.sub,
                        "x":operator.mul,
                        "/":operator.__truediv__
                    }[op]
                def eval_bin(op1,oper,op2):
                    op1,op2 = int(op1),int(op2)
                    return op(oper)(op1,op2)
                speak("Your result is")
                speak(eval_bin(*(mystr.split())))
            
                speak("Anything else sir")
            

            elif "sleep now" in self.query:
                speak("Ok sir you can wake me any time")
                self.sleep()
            
            elif "current weather" in self.query:
                speak("Please say the city sir: ")
                x = self.listen()
                url = f"https://www.google.com/search?q=teampurature in  {x}"
                r = get(url)
                data = bs(r.text,"html.parser")
                temp = data.find("div",class_="BNeawe").text
                speak(f"Current tempurature at {x} is {temp}")
            
                speak("Anything else sir")
            

            elif "activate how to do mode" in self.query:
                speak("How to do mode is activated.. ")
                s = True
                while s:
                    speak("please tell me what you wanna know")
                    how = self.listen()
                    try:
                        if how  == "exit":
                            speak("how to do mode deactivated")
                            s=False
                        else:
                            max_r = 1
                            how_to = search_wikihow(how,max_r)
                            assert len(how_to) == 1
                            how_to[0].print()
                            speak(how_to[0].summary)
                    except Exception as e:
                        speak("Sorry sir unable to find this")
                        
                speak("Anything else sir")
            
            
            elif "how much power left" in self.query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Sir you have your system at {percentage} percent")
                if percentage >= 75:
                    speak("We have enough power to work sir")
                elif percentage >= 45:
                    speak("We have enough power but its healthy to connect the charger")
                elif percentage >= 15:
                    speak("We dont have enough power but connect the charger")
            

                speak("Anything else sir")
            
            elif "internet speed" in self.query:
                try:
                    os.system('cmd /k "speedtest"')
                except:
                    speak("No internet connected sir")
            
            elif "volume up" in self.query:
                pyautogui.press("volumeup")

            elif "volume down" in self.query:
                pyautogui.press("volumedown")

            elif "volume mute" in self.query:
                pyautogui.press("volumemute")

            elif "exit" in self.query:
                speak("Thank you sir, Have a nice day!!")
                sys.exit()

            else:
                speak("Sorry sir i am unable to understand what you said please try again..")

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CeliaGui()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    
    def startTask(self):
        self.ui.movie= QMovie("./img/jarvis.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie= QMovie("./img/loader.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        cut = QTime.currentTime()
        cud = QDate.currentDate()
        lbl_time =cut.toString("hh:mm:ss")
        lbl_date = cud.toString(Qt.ISODate)
        self.ui.textBrowser.setText(lbl_date)
        self.ui.textBrowser_2.setText(lbl_time)


app =QApplication(sys.argv)
celia = Main()
celia.show()
exit(app.exec())