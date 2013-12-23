import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.config import Config
from windows_popup import balloon_tip
import threading
import win32api
import time
import sys

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')

class CheckScreen(FloatLayout):
    def initiate(self):
        """Starts the notification thread"""
        self.ids.start_button.enabled = False
        self.first_run = True
        notify = threading.Thread(target=self.notification)
        notify.start()

    def notification(self):
        """Creates the notifications"""
        tags = [i.strip() for i in self.ids.tags.text.split(',')]
        old = {tag:'' for tag in tags}
        new = {}
        from_date = {tag:None for tag in tags}
        first_run = {tag:True for tag in tags}
        print first_run
        while True:
            for tag in tags:
                if not first_run[tag]:
                    print  '******'
                    new[tag] =  self.get_new_title(tag,after=from_date[tag])
                    print new[tag]
                    from_date[tag] = new[tag][0][1] if new[tag] else None
                    print from_date[tag]
                    if new[tag][0][0] != old[tag][-1][0]:
                        win32api.MessageBeep() #Beep! Beep! Beep!
                        number_of_qs = len(new[tag])-1 #Number of Questions
                        title = '{} new {} questions '.format(number_of_qs,tag) if number_of_qs>1 else '{} new {} question '.format(1,tag)
                        msg = '{} Latest : "{}"'.format(tag,new[tag][0][0])
                        print title
                        popup = balloon_tip(title,msg)
                else:
                    new[tag] =  self.get_new_title(tag)
                    from_date[tag] = new[tag][0][1]

                old = new
                first_run[tag] = False
                print '******'+str(first_run)

            time.sleep(60*float(self.ids.delay.text))

    def get_new_title(self,tag,after=None):
        """This method gets the latest title of the given tag"""
        payload = {'pagesize': 1, 'sort': 'creation', 'tagged': tag,'site': 'stackoverflow'}
        if after:
            payload["fromdate"] = after
            del payload['pagesize']
        url = requests.get('https://api.stackexchange.com/2.1/questions',params= payload)
        #print url.url
        data = url.json()["items"]
        time_asked =  [data[i]["creation_date"] for i in xrange(len(data))]
        #avg_size = sys.getsizeof(url.json()) # This might be useful sometime later to log size of each request
        title = [data[i]["title"] for i in xrange(len(data))]

        return zip(title,time_asked)

    #def logger(self,size,time_per_request):


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