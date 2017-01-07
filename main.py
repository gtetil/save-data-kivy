import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'maxfps', '10')

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

import json
from functools import partial

from kivy.core.window import Window

Window.size = (800,480)

class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.dynamic_layout.build_layout()


class MainApp(App):
    def build(self):
        return MainScreen()

class DynamicLayout(Widget):
    indicator_layout = ObjectProperty(None)
    button_edit_popup = ObjectProperty(None)
    layout_file = 'dynamic_layout.json'

    def save_layout(self):
        data = {}
        for indicator in self.indicator_layout.children:
            label = {}
            label['label'] = indicator.text
            data[indicator.id] = label
        with open(self.layout_file, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

    def build_layout(self):
        with open(self.layout_file, 'r') as fp:
            data = json.load(fp)
        for i in range(6):
            indicator_label = data['indicator_'+str(i)]['label']
            indicator_button = Button(text=indicator_label, id='indicator_' + str(i))
            indicator_button.bind(on_press=partial(self.button_edit_popup.edit_popup, 'indicator_' + str(i)))
            self.indicator_layout.add_widget(indicator_button)

class ButtonEditPopup(Popup):
    label_input = ObjectProperty(None)
    button = ObjectProperty(None)
    dynamic_layout = ObjectProperty(None)

    def edit_popup(self, instance, button):
        self.button = button
        self.label_input.text = button.text
        self.open()

    def save_button(self):
        self.button.text = self.label_input.text
        self.dynamic_layout.save_layout()
        self.dismiss()


if __name__ == '__main__':

    MainApp().run()
