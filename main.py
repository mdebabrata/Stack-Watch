import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.config import Config
import threading
import win32api
import time

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')

class CheckScreen(FloatLayout):
    def initiate(self):
        self.ids.start_button.enabled = False
        notify = threading.Thread(target=self.notification)
        notify.start()

    def notification(self):
        self.old_title = ''
        self.payload = {'pagesize': 1, 'sort': 'creation', 'tagged': 'python','site': 'stackoverflow'}
        while True:
            self.url = requests.get('https://api.stackexchange.com/2.1/questions',params=self.payload)
            self.data = self.url.json()["items"][0]
            self.new_title =  self.data["title"]
            if self.new_title != self.old_title:
                print self.new_title
                print self.old_title
                #Beep! Beep! Beep!
                win32api.MessageBeep()
            self.old_title = self.new_title
            time.sleep(float(self.ids.delay.text))

class StartButton(Button):
    enabled = BooleanProperty(True)

    def on_enabled(self, instance, value):
        if value:
            self.background_color = [0.118,0.253,0.138,100]
            self.color = [1,1,1,1]
        else:
            self.background_color = [1,1,1,.3]
            self.color = [1,1,1,.5]

    def on_touch_down( self, touch ):
        if self.enabled:
            return super(self.__class__, self).on_touch_down(touch)

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

--- http://docs.activestate.com/activepython/2.7/pywin32/PyWin32.HTML
--- http://timgolden.me.uk/pywin32-docs/index.html

"""