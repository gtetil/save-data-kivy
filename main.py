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
import json
from functools import partial

from kivy.core.window import Window

Window.size = (800,480)
Config.set('graphics', 'maxfps', '10')

class MainScreen(BoxLayout):
    dynamic_layout = ObjectProperty(None)
    indicator_layout = ObjectProperty(None)
    button_edit_popup = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.dynamic_layout.build_layout(self.indicator_layout, self.button_edit_popup)
        self.dynamic_layout.save_layout(self.indicator_layout)


class MainApp(App):
    def build(self):
        self.dynamic_layout = DynamicLayout()
        return MainScreen()

class DynamicLayout(Widget):
    layout_file = 'dynamic_layout.json'

    def save_layout(self, layout):
        data = {}
        for indicator in layout.children:
            label = {}
            label['label'] = indicator.text
            data[indicator.id] = label
        with open(self.layout_file, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

    def build_layout(self, layout, popup):
        with open(self.layout_file, 'r') as fp:
            data = json.load(fp)
        for i in range(6):
            indicator_label = data['indicator_'+str(i)]['label']
            indicator_button = Button(text=indicator_label, id='indicator_' + str(i))
            indicator_button.bind(on_press=partial(popup.edit_popup, 'indicator_' + str(i)))
            layout.add_widget(indicator_button)

class ButtonEditPopup(Popup):
    label_input = ObjectProperty(None)

    def edit_popup(self, instance, button):
        self.label_input.text = button.text
        self.open()


if __name__ == '__main__':

    MainApp().run()
