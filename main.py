from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.config import Config
import requests
import threading
#import win32api
import time
import sys
from Queue import Queue
#from windows_popup import balloon_tip
from utils import arithmeticEval

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')


class CheckScreen(FloatLayout):
    def initiate(self):
        """
        Starts the notification thread
        """
        self.ids.start_button.enabled = False
        self.first_run = True
        self.popup_queue = Queue()
        notify = threading.Thread(target=self.manage_notifications)
        notify.start()

    def manage_notifications(self):
        """
        Creates the notifications
        """
        tags = [i.strip() for i in self.ids.tags.text.split(',')]
        for tag in tags:
            thread = threading.Thread(target=self.notification,args=(tag,))
            thread.start()
            popup_manager = threading.Thread(target=self.popup_manager)
            popup_manager.start()

    def notification(self,tag):
        print 'Initiated : ' + tag
        old = [['']]
        new = ''
        from_date = None
        first_run = True
        while True:
            request = self.get_new_title(tag,after=from_date)
            new =  request if request else None
            from_date = new[0][1] -1 if new else None
            if new:
                if new[0][0] != old[0][0] and not first_run:
                    #win32api.MessageBeep()  #Beep! Beep! Beep!
                    number_of_qs = len(new)-1  #Number of Questions

                    title = '{} new {} questions '.format(number_of_qs,tag) \
                        if number_of_qs>1 else '{} new {} question '.format(1,tag)

                    msg = '{} Latest : "{}"'.format(tag,new[0][0])
                    self.popup_queue.put([(title,msg)])
                old = list(new)
            first_run = False
            time.sleep(arithmeticEval(self.ids.delay.text))


    def get_new_title(self,tag,after=None):
        """
        This method gets the latest titles of the given tag after a certain time which is specified by "after"
        """
        payload = {'pagesize': 1, 'sort': 'creation', 'tagged': tag, 'site': 'stackoverflow',
                   'client_id':2416, 'key':'JKpvjcIrXZ3fUITWvszu6A(('}
        if after:
            #print "tag : {} after value : {}".format(tag,after)
            payload["fromdate"] = after
            del payload['pagesize']

        url = requests.get('https://api.stackexchange.com/2.1/questions',params= payload)
        data = url.json()["items"]
        time_asked =  [data[i]["creation_date"] for i in xrange(len(data))]
        #avg_size = sys.getsizeof(url.json()) # This might be useful sometime later to log size of each request
        title = [data[i]["title"] for i in xrange(len(data))]
        return zip(title,time_asked)

    def popup_manager(self):
        """
        Manages popups efficiently. This class was created in order to avoid errors when
        multiple tags created notifications at the same time.
        """
        while True:
            queue = self.popup_queue.get()
            for popup in queue:
                #print popup
                balloon_tip(popup[0],popup[1])

    #def logger(self,size,time_per_request): # check pympler https://pypi.python.org/pypi/Pympler/


class StartButton(Button):
    enabled = BooleanProperty(True)

    def on_enabled(self, instance, value):
        if value:
            self.background_color = [0.118,0.253,0.138,1]
            self.color = [1,1,1,1]
        else:
            self.background_color = [1,1,1,1]
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

----------
- https://github.com/Cereal84/notifyMe
-----------

"""
