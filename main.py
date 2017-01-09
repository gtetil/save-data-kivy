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
from kivy.animation import Animation

import json
from functools import partial
import random

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
    modify_mode = BooleanProperty(False)
    layout_file = 'dynamic_layout.json'

    def save_layout(self):
        data = {}
        for indicator in self.indicator_layout.children:
            config = {}
            config['label'] = indicator.text
            config['channel'] = indicator.channel
            data[indicator.id] = config
        for button in self.button_layout.children:
            config = {}
            config['label'] = button.text
            config['toggle'] = button.toggle
            config['channel'] = button.channel
            data[button.id] = config
        with open(self.layout_file, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

    def build_layout(self):
        self.indicator_layout.clear_widgets()
        self.button_layout.clear_widgets()
        with open(self.layout_file, 'r') as fp:
            data = json.load(fp)
        for i in range(6):
            indicator_label = data['indicator_'+str(i)]['label']
            channel = data['button_' + str(i)]['channel']
            indicator_button = IndicatorButton(text=indicator_label, id='indicator_' + str(i))
            indicator_button.bind(on_press=partial(self.indicator_edit_popup.edit_popup, 'indicator_' + str(i)))
            indicator_button.set_properties('null', channel)
            self.indicator_layout.add_widget(indicator_button)

            button_label = data['button_' + str(i)]['label']
            toggle = data['button_' + str(i)]['toggle']
            channel = data['button_' + str(i)]['channel']
            if toggle:
                button = DynToggleButton(text=button_label, id='button_' + str(i))
            else:
                button = DynButton(text=button_label, id='button_' + str(i))
            button.bind(on_press=partial(self.button_edit_popup.edit_popup, 'button_' + str(i)))
            button.set_properties(self, channel)
            self.button_layout.add_widget(button)
        if self.modify_mode:
            self.modify_screen()

    def modify_screen(self):
        self.modify_mode = True
        for indicator in self.indicator_layout.children:
            self.animate(indicator)
        for button in self.button_layout.children:
            self.animate(button)

    def end_modify(self):
        self.modify_mode = False
        for indicator in self.indicator_layout.children:
            Animation.cancel_all(indicator)
            indicator.background_color = 1, 1, 1, 1
        for button in self.button_layout.children:
            Animation.cancel_all(button)
            button.background_color = 1, 1, 1, 1

    def animate(self, widget):
        anim = Animation(background_color=[1, 1, 0, 0.75], duration=0.5, t='linear') + Animation(
            background_color=[1, 1, 1, 1], duration=0.5, t='linear')
        anim.repeat = True
        anim.start(widget)

class IndicatorEditPopup(Popup):
    ind_label_input = ObjectProperty(None)
    ind_channel_spinner = ObjectProperty(None)
    indicator = ObjectProperty(None)
    dynamic_layout = ObjectProperty(None)
    modify_mode = BooleanProperty(False)

    def edit_popup(self, instance, indicator):
        if self.modify_mode:
            self.indicator = indicator
            self.ind_label_input.text = self.indicator.text
            self.ind_channel_spinner.text = str(self.indicator.channel)
            self.open()

    def save_indicator(self):
        self.indicator.text = self.ind_label_input.text
        self.indicator.channel = int(self.ind_channel_spinner.text)
        self.dynamic_layout.save_layout()
        self.dismiss()

class ButtonEditPopup(Popup):
    label_input = ObjectProperty(None)
    toggle_check = ObjectProperty(None)
    channel_spinner = ObjectProperty(None)
    button = ObjectProperty(None)
    dynamic_layout = ObjectProperty(None)
    modify_mode = BooleanProperty(False)

    def edit_popup(self, instance, button):
        if self.modify_mode:
            self.button = button
            self.label_input.text = self.button.text
            self.toggle_check.active = self.button.toggle
            self.channel_spinner.text = str(self.button.channel)
            self.open()

    def save_button(self):
        self.button.text = self.label_input.text
        self.button.toggle = self.toggle_check.active
        self.button.channel = int(self.channel_spinner.text)
        self.dynamic_layout.save_layout()
        self.dynamic_layout.build_layout()
        self.dismiss()

class DynToggleButton(ToggleButton):
    dynamic_layout = ObjectProperty(None)
    toggle = BooleanProperty(True)
    channel = NumericProperty(0)

    def set_properties(self, ref, channel):
        self.dynamic_layout = ref
        self.channel = channel

    def on_press(self):
        if self.dynamic_layout.modify_mode:
            self.state = 'normal'

class DynButton(Button):
    dynamic_layout = ObjectProperty(None)
    toggle = BooleanProperty(False)
    channel = NumericProperty(0)

    def set_properties(self, ref, channel):
        self.dynamic_layout = ref
        self.channel = channel

    def on_press(self):
        if self.dynamic_layout.modify_mode:
            self.state = 'normal'

class IndicatorButton(Button):
    channel = NumericProperty(0)

    def set_properties(self, ref, channel):
        self.channel = channel

    def on_press(self):
        self.state = 'normal'

if __name__ == '__main__':

    MainApp().run()
