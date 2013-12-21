import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
import threading
import win32api


class CheckScreen(FloatLayout):
    def check(self):
        data = threading.Thread(target=self.get_data)
        data.start()

    def get_data(self):
        self.payload = {'pagesize':1,'sort':'creation','tagged':'python','site':'stackoverflow'}
        self.url = requests.get('https://api.stackexchange.com/2.1/questions',params=self.payload)
        self.data = self.url.json()["items"][0]
        self.ids.label.text += self.data["title"]
        #Beep! Beep! Beep!
        win32api.MessageBeep()


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