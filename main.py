import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
import threading
import win32api
import time

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')

class CheckScreen(FloatLayout):
    def initiate(self):
        notify = threading.Thread(target=self.notification)
        notify.start()

    def notification(self):
        self.old_title = ''
        while True:
            self.payload = {'pagesize':1,'sort':'creation','tagged':'python','site':'stackoverflow'}
            self.url = requests.get('https://api.stackexchange.com/2.1/questions',params=self.payload)
            self.data = self.url.json()["items"][0]
            self.new_title =  self.url.json()["items"][0]["title"]
            if self.new_title != self.old_title:
                #Beep! Beep! Beep!
                win32api.MessageBeep()
            self.old_title = self.new_title
            time.sleep(float(self.ids.delay.text))

class MainApp(App):
    def build(self):
        return CheckScreen()

if __name__ == "__main__":
    MainApp().run()

#https://api.stackexchange.com/docs
#http://requests.readthedocs.org/

"""
Might wanna look at:
--- http://stackoverflow.com/questions/9494739/how-to-build-a-systemtray-app-for-windows
--- http://stackoverflow.com/questions/1025029/how-to-use-win32-apis-with-python
--- http://www.brunningonline.net/simon/blog/archives/SysTrayIcon.py.html

"""

"""
Implement Threading
"""