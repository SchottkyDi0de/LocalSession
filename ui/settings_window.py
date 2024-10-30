from typing import TYPE_CHECKING
from tkinter import font

from customtkinter import (
    CTkToplevel,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkImage,
    StringVar,
    CTkButton,
    filedialog,
    CTkComboBox,
    CTkScrollableFrame
)
from PIL import Image

from lib.utils.resources import resource_path
from settings.settings import _settings

if TYPE_CHECKING:
    from main import App


class SettingsWindow(CTkToplevel):
    def __init__(self, master: 'App', **kwargs):
        super().__init__(master, **kwargs)
        self.minsize(300, 200)
        self.after(250, lambda: self.iconbitmap(resource_path('assets/ui/app_logo.ico')))
        self.title("Settings")
        self.root_layer = CTkScrollableFrame(self)
        self.root_layer.pack(fill="both", expand=True)
        
        self.folder_frame = CTkFrame(self.root_layer)

        self.curr_folder_label = CTkLabel(
            self.folder_frame,
            text=f"Current folder: {_settings.get_by_key('replays_path')}",
            wraplength=280
        )

        self.choose_folder_btn = CTkButton(
            self.folder_frame,
            text="Choose replays folder",
            command=self.choose_folder
        )
        
        self.folder_frame.pack(side="top", expand=True, fill="both")
        self.curr_folder_label.pack(side="top")
        self.choose_folder_btn.pack(side='top')
        
        self.font_settings_frame = CTkFrame(self.root_layer)
        
        self.static_font_label = CTkLabel(
            self.font_settings_frame,
            text="Static font"
        )
        self.dynamic_font_label = CTkLabel(
            self.font_settings_frame,
            text="Dynamic font"
        )
        
        self.static_font_input_field = CTkComboBox(
            self.font_settings_frame,
            values=list(font.families()),
            command=self.set_static_font
        )
        self.dynamic_font_input_field = CTkComboBox(
            self.font_settings_frame,
            values=list(font.families()),
            command=self.set_dynamic_font
        )
        self.dynamic_font_input_field.set(_settings.db['font']['dynamic_text'])
        self.static_font_input_field.set(_settings.db['font']['static_text'])
        
        self.font_size_settings_frame = CTkFrame(self.root_layer)
        self.font_size_settings_frame.pack(side="top", expand=True, fill="both")

        self.dynamic_font_size_label = CTkLabel(
            self.font_size_settings_frame,
            text="Dynamic text font size"
        )
        
        self.static_font_size_label = CTkLabel(
            self.font_size_settings_frame,
            text="Static text font size"
        )
        
        self.static_font_size_input_field = CTkComboBox(
            self.font_size_settings_frame,
            values=['5', '7', '9', '12', '16', '21', '28'],
            command=self.set_static_font_size
        )
        self.dynamic_font_size_input_field = CTkComboBox(
            self.font_size_settings_frame,
            values=['5', '7', '9', '12', '16', '21', '28'],
            command=self.set_dynamic_font_size
        )
        
        self.static_font_size_label.pack(side="top")
        self.static_font_size_input_field.pack(side="top")
        self.dynamic_font_size_label.pack(side="top")
        self.dynamic_font_size_input_field.pack(side="top")
        
        self.dynamic_font_size_input_field.set(_settings.db['font']['dynamic_text_size'])
        self.static_font_size_input_field.set(_settings.db['font']['static_text_size'])
        
        self.font_settings_frame.pack(side="top", expand=True, fill="both")
        self.static_font_label.pack(side="top")
        self.static_font_input_field.pack(side="top")
        self.dynamic_font_label.pack(side="top")
        self.dynamic_font_input_field.pack(side="top")
        
        self.text_settings_frame = CTkFrame(self.root_layer)
        
        self.btls_label_text = CTkLabel(self.text_settings_frame, text="Battles label text")
        self.wr_label_text = CTkLabel(self.text_settings_frame, text="Winrate label text")
        self.ac_label_text = CTkLabel(self.text_settings_frame, text="Accuracy label text")
        self.avg_dmg_label_text = CTkLabel(self.text_settings_frame, text="Average damage label text")
        
        self.btls_label_val = StringVar(self, value='')
        self.wr_label_val = StringVar(self, value='')
        self.ac_label_val = StringVar(self, value='')
        self.avg_dmg_label_val = StringVar(self, value='')
        
        self.btls_input_field = CTkEntry(self.text_settings_frame, textvariable=self.btls_label_val)
        self.wr_input_field = CTkEntry(self.text_settings_frame, textvariable=self.wr_label_val)
        self.ac_input_field = CTkEntry(self.text_settings_frame, textvariable=self.ac_label_val)
        self.avg_dmg_input_field = CTkEntry(self.text_settings_frame, textvariable=self.avg_dmg_label_val)
        
        self.btls_input_field.insert(0, _settings.db['font']['battles_label'])
        self.wr_input_field.insert(0, _settings.db['font']['winrate_label'])
        self.ac_input_field.insert(0, _settings.db['font']['accuracy_label'])
        self.avg_dmg_input_field.insert(0, _settings.db['font']['avg_damage_label'])
        
        self.btls_label_text.pack(side="top")
        self.btls_input_field.pack(side="top")
        self.wr_label_text.pack(side="top")
        self.wr_input_field.pack(side="top")
        self.ac_label_text.pack(side="top")
        self.ac_input_field.pack(side="top")
        self.avg_dmg_label_text.pack(side="top")
        self.avg_dmg_input_field.pack(side="top")
        
        self.text_settings_frame.pack(side="top", expand=True, fill="both")

        self.save_btn = CTkButton(
            self.root_layer,
            text='',
            image=CTkImage(Image.open(resource_path("assets/ui/save_btn.png"))),
            width=28,
            command=self.save_settings
        )
        self.save_btn.pack(side='bottom', anchor='se')

    def choose_folder(self):
        path = filedialog.askdirectory()
        
        if path != '':
            _settings.set('replays_path', path)
            self.curr_folder_label.configure(text=f"Current folder: {path}")
            
    def set_static_font(self, value: str):
        _settings.db['font']['static_text'] = value
        
    def set_dynamic_font(self, value: str):
        _settings.db['font']['dynamic_text'] = value
        
    def set_static_font_size(self, value: str):
        _settings.db['font']['static_text_size'] = int(value)
        
    def set_dynamic_font_size(self, value: str):
        _settings.db['font']['dynamic_text_size'] = int(value)
        
    def save_settings(self):
        _settings.db['font']['battles_label'] = self.btls_input_field.get()
        _settings.db['font']['winrate_label'] = self.wr_input_field.get()
        _settings.db['font']['accuracy_label'] = self.ac_input_field.get()
        _settings.db['font']['avg_damage_label'] = self.avg_dmg_input_field.get()
        _settings.db.commit()
        
        self.master: 'App'
        self.master.update_all_widgets()
        self.destroy()
        print('Core: Settings saved')
        print('UI: Settings window closed')
