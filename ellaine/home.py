from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.garden.filebrowser import FileBrowser
from kivy.uix.popup import Popup
from pathlib import Path
import os.path

import os
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

import note
import wave
import process
import bash_record

global stud_file
global prof_file
stud_file = ""
prof_file = ""

class HomeWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(HomeWidget, self).__init__(**kwargs)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

        record_stud = Button(
             id="record_stud",
             size_hint=(0.3, 0.06),
             pos_hint={'center_x': .5, 'center_y': .6},
             text="Record the student",
             background_normal='',
             background_color=[0, 0, 0, 1]
        )
    
        self.add_widget(record_stud)
        
        record_prof = Button(
             id="record_prof",
             size_hint=(0.35, 0.06),
             pos_hint={'center_x': .5, 'center_y': .5},
             text="Record the professional",
             background_normal='',
             background_color=[0, 0, 0, 1]
        )
    
        self.add_widget(record_prof)

        upload_stud = Button(
             id="upload_stud",
             size_hint=(0.4, 0.06),
             pos_hint={'center_x': .5, 'center_y': .4},
             text="Upload the student recording",
             background_normal='',
             background_color=[0, 0, 0, 1]
        )
    
        self.add_widget(upload_stud)
        
        upload_prof = Button(
             id="upload_prof",
             size_hint=(0.4, 0.06),
             pos_hint={'center_x': .5, 'center_y': .3},
             text="Upload the professional recording",
             background_normal='',
             background_color=[0, 0, 0, 1]
        )
    
        self.add_widget(upload_prof)

        process = Button(
             id="process",
             size_hint=(0.1, 0.06),
             pos_hint={'center_x': .5, 'center_y': .2},
             text="Process",
             background_normal='',
             background_color=[0.5, 0.5, 0.6, 0.7]
        )
        
        self.add_widget(process)

        quit = Button(
            id="quit",
            size_hint=(0.1, 0.06),
            pos_hint={'center_x': .9, 'center_y': .05},
            text="Quit",
            background_normal='',
            background_color=[0.5, 0.5, 0.6, 0.7]
        )

        process.bind(on_release=self.process_callback)
        quit.bind(on_release=self.quit_callback)
        upload_stud.bind(on_release=self.open_stud_file_btn_pressed)
        upload_prof.bind(on_release=self.open_prof_file_btn_pressed)
        record_stud.bind(on_release=self.bash_record_stud)
        record_prof.bind(on_release=self.bash_record_prof)

        self.add_widget(quit)

    def process_callback(self, instance):
        if stud_file == "" or prof_file == "":
            print("Select both files.")
            print(stud_file)
            print(prof_file)
        else:
            self.add_widget(
                process.ProcessWidget(
                    id="process",
                    stud=stud_file,
                    prof=prof_file,
                    size_hint=(1, 1),
                    pos_hint={'center_x': .5, 'center_y': .5})
                )
    
    def quit_callback(self, instance):
        quit()

    def bash_record_stud(self, *args):
        global stud_file
        bash_record.record_stud()
        stud_file = 'stud.wav'
    
    def bash_record_prof(self, *args):
        global prof_file
        bash_record.record_prof()
        prof_file = 'prof.wav'

    def open_stud_file_btn_pressed(self, *args):
        user_path = '~/Downloads/ece5725_final_project/ellaine'
        self._fbrowser = FileBrowser(select_string='Open',favorites=[(user_path, 'Documents')])
        self._fbrowser.bind(on_success=self._stud_file_load,
                            on_canceled=self._cancel_popup)

        self._popup = Popup(title='Open File', content=self._fbrowser,
                            size_hint=(0.9, 0.9), auto_dismiss=False)

        self._popup.open()
    
    def open_prof_file_btn_pressed(self, *args):
        self._fbrowser = FileBrowser(select_string='Open')
        self._fbrowser.bind(on_success=self._prof_file_load,
                            on_canceled=self._cancel_popup)

        self._popup = Popup(title='Open File', content=self._fbrowser,
                            size_hint=(0.9, 0.9), auto_dismiss=False)

        self._popup.open()
    
    def _cancel_popup(self, instance):
        print('cancelled, Close self.')
        self._popup.dismiss()
    
    def _stud_file_load(self, instance):
        print("in stud file load")
        global stud_file
        stud_file = os.path.basename(instance.filename)
        print(stud_file)
        self._popup.dismiss()

    def _prof_file_load(self, instance):
        print("in prof file load")
        global prof_file
        prof_file = os.path.basename(instance.filename)
        print(prof_file)
        self._popup.dismiss()

    def update_rect(self, *kargs):
        self.rect.pos = self.pos
        self.rect.size = self.size


