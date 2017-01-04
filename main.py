import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore

from kivy.core.window import Window

Window.size = (800,480)
Config.set('graphics', 'maxfps', '10')

class MainScreen(BoxLayout):
    dynamic_layout = ObjectProperty(None)
    indicator_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.dynamic_layout.build_layout(self.indicator_layout)
        self.dynamic_layout.save_layout(self.indicator_layout)


class MainApp(App):
    def build(self):
        self.dynamic_layout = DynamicLayout()
        return MainScreen()

class DynamicLayout(Widget):
    store = JsonStore('dynamic_layout.json')

    def save_layout(self, layout):
        for indicator in layout.children:
            print(indicator.id)
            self.store.put(indicator.id, label=indicator.text)

    def build_layout(self, layout):
        for i in range(6):
            indicator_label = self.store.get('indicator_'+str(i))['label']
            indicator_button = Button(text=indicator_label, id='indicator_' + str(i))
            layout.add_widget(indicator_button, i)

if __name__ == '__main__':

    MainApp().run()
