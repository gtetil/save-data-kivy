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
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty

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
    button_layout = ObjectProperty(None)
    indicator_edit_popup = ObjectProperty(None)
    button_edit_popup = ObjectProperty(None)
    layout_file = 'dynamic_layout.json'

    def save_layout(self):
        data = {}
        for indicator in self.indicator_layout.children:
            config = {}
            config['label'] = indicator.text
            data[indicator.id] = config
        for button in self.button_layout.children:
            config = {}
            config['label'] = button.text
            config['toggle'] = button.toggle
            data[button.id] = config
        with open(self.layout_file, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

    def build_layout(self):
        with open(self.layout_file, 'r') as fp:
            data = json.load(fp)
        for i in range(6):
            indicator_label = data['indicator_'+str(i)]['label']
            indicator_button = Button(text=indicator_label, id='indicator_' + str(i))
            indicator_button.bind(on_press=partial(self.indicator_edit_popup.edit_popup, 'indicator_' + str(i)))
            self.indicator_layout.add_widget(indicator_button)

            button_label = data['button_' + str(i)]['label']
            toggle = data['button_' + str(i)]['toggle']
            if toggle == "True":
                button = DynToggleButton(text=button_label, id='button_' + str(i))
            else:
                button = DynButton(text=button_label, id='button_' + str(i))
            button.bind(on_press=partial(self.button_edit_popup.edit_popup, 'button_' + str(i)))
            self.button_layout.add_widget(button)

class IndicatorEditPopup(Popup):
    ind_label_input = ObjectProperty(None)
    indicator = ObjectProperty(None)
    dynamic_layout = ObjectProperty(None)

    def edit_popup(self, instance, indicator):
        self.indicator = indicator
        self.ind_label_input.text = self.indicator.text
        self.open()

    def save_indicator(self):
        self.indicator.text = self.ind_label_input.text
        self.dynamic_layout.save_layout()
        self.dismiss()

class ButtonEditPopup(Popup):
    label_input = ObjectProperty(None)
    toggle_check = ObjectProperty(None)
    button = ObjectProperty(None)
    dynamic_layout = ObjectProperty(None)

    def edit_popup(self, instance, button):
        self.button = button
        self.label_input.text = self.button.text
        self.toggle_check.active = self.button.toggle
        self.open()

    def save_button(self):
        self.button.text = self.label_input.text
        self.button.toggle = self.toggle_check.active
        self.dynamic_layout.save_layout()
        self.dismiss()

class DynToggleButton(ToggleButton):
    toggle = BooleanProperty(True)

class DynButton(Button):
    toggle = BooleanProperty(False)

if __name__ == '__main__':

    MainApp().run()
