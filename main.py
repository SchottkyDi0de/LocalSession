import traceback
from customtkinter import (
    CTkButton, 
    CTkFrame, 
    CTkLabel, 
    CTkImage, 
    CTkFont,
    CTk
)
from typing import Tuple

import PIL.Image

from ui.settings_window import SettingsWindow
from replay_parser.parser import ReplayParser
from lib.watchdog.handle_replays import FileWatchDog, NewFileEvent
from settings.settings import _settings
from lib.utils.resources import resource_path


class SessionStorage:
    battles: int = 0
    wins: int = 0
    damage_dealt: int = 0
    hits: int = 0
    shots: int = 0

    wr: float = 0.0
    ac: float = 0.0
    avg_dmg: int = 0
    
    def save_divide(self, dividend: int, divisor: int, return_int: bool = False, default: float = 0.0):
        try:
            res = dividend / divisor
        except ZeroDivisionError:
            return default
        
        if return_int:
            return int(res)
        else:
            return res
    
    def compute(self):
        self.wr = self.save_divide(self.wins, self.battles, default=0.0) * 100
        self.ac = self.save_divide(self.hits, self.shots, default=0.0) * 100
        self.avg_dmg = self.save_divide(self.damage_dealt, self.battles, return_int=True, default=0)
        
    def delete_session(self):
        print('Core: Session cleared')
        self.battles = 0
        self.wins = 0
        self.damage_dealt = 0
        self.hits = 0
        self.shots = 0
        self.wr = 0.0
        self.ac = 0.0
        self.avg_dmg = 0


_session_storage = SessionStorage()


class StatsLabelContainer(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.btls_container = CTkFrame(self, height=30)
        self.wr_container = CTkFrame(self, height=30)
        self.ac_container = CTkFrame(self, height=30)
        self.avg_dmg_container = CTkFrame(self, height=30)
        
        self.btls_container.pack(side="top", fill="x")
        self.wr_container.pack(side="top", fill="x")
        self.ac_container.pack(side="top", fill="x")
        self.avg_dmg_container.pack(side="top", fill="x")
        
        
class App(CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.wm_attributes("-topmost", True)
        self.attributes("-alpha", 0.6)
        self.minsize(230, 120)
        self.title('Local Session')
        self.frame = CTkFrame(self)
        self.frame.pack(fill='both', expand=True)
        self.iconbitmap(resource_path("assets/ui/app_logo.ico"))
        self.parser = ReplayParser()
        
        self.static_stats_font = CTkFont(
            family=_settings['font']['static_text'], 
            size=_settings['font']['static_text_size'], 
            weight="bold"
        )
        self.stats_font = CTkFont(
            family=_settings['font']['dynamic_text'], 
            size=_settings['font']['dynamic_text_size'],
            weight="bold"
        )
        
        self.stats_container = StatsLabelContainer(self.frame)
        
        self.settings_btn = CTkButton(
            self.stats_container.btls_container,
            width=28,
            text="",
            hover=False,
            command=self.open_settings,
            fg_color="grey",
            image=CTkImage(PIL.Image.open(resource_path("assets/ui/settings_btn_cog.png")), size=(20, 20)),
        )
        
        self.settings_btn.pack(side='right', anchor='ne')
        
        self.static_btls_label = CTkLabel(
            self.stats_container.btls_container,
            text=_settings['font']['battles_label'],
            font=self.static_stats_font
        )
        self.static_wr_label = CTkLabel(
            self.stats_container.wr_container,
            text=_settings['font']['winrate_label'],
            font=self.static_stats_font
        )
        self.static_ac_label = CTkLabel(
            self.stats_container.ac_container,
            text=_settings['font']['accuracy_label'],
            font=self.static_stats_font
        )
        self.static_avg_dmg_label = CTkLabel(
            self.stats_container.avg_dmg_container,
            text=_settings['font']['avg_damage_label'],
            font=self.static_stats_font
        )
        
        self.btls_label = CTkLabel(
            self.stats_container.btls_container,
            text=f"{_session_storage.battles}",
            font=self.stats_font,
            text_color='#9D89E6'
        )
        
        self.wr_label = CTkLabel(
            self.stats_container.wr_container,
            text=f"{_session_storage.wr:2.2f} %",
            font=self.stats_font,
            text_color='#9D89E6'
        )
        
        self.ac_label = CTkLabel(
            self.stats_container.ac_container,
            text=f"{_session_storage.ac:2.2f} %",
            font=self.stats_font,
            text_color='#9D89E6'
        )
        
        self.avg_dmg_label = CTkLabel(
            self.stats_container.avg_dmg_container,
            text=f"{int(_session_storage.avg_dmg)}",
            font=self.stats_font,
            text_color='#9D89E6'
        )
        
        self.del_session_btn = CTkButton(
            self.stats_container.avg_dmg_container,
            width=28,
            text="",
            hover=False,
            command=self.delete_session,
            fg_color="grey",
            image=CTkImage(PIL.Image.open(resource_path("assets/ui/delete_session.png")), size=(20, 20)),
        )
        
        self.static_btls_label.pack(side='left')
        self.static_wr_label.pack(side='left')
        self.static_ac_label.pack(side='left')
        self.static_avg_dmg_label.pack(side='left')
        
        self.btls_label.pack(side='left', anchor='nw')
        self.wr_label.pack(side='left', anchor='nw')
        self.ac_label.pack(side='left', anchor='nw')
        self.avg_dmg_label.pack(side='left', anchor='nw')
        
        self.del_session_btn.pack(side='right', anchor='se')
        
        self.stats_container.pack(side="top", fill="x")
        
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        
        self.settings_window = None
        
        self.after(1000, self.run_watcher)
        
    def delete_session(self):
        _session_storage.delete_session()
        self.update_values()
        
    def open_settings(self):
        
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
            print('UI: Settings window opened')
        else:
            self.settings_window.focus()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, _):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        
    def update_all_widgets(self):
        self.stats_font = CTkFont(
            family=_settings.db['font']['dynamic_text'], 
            size=_settings.db['font']['dynamic_text_size'],
            weight="bold"
        )
        self.static_stats_font = CTkFont(
            family=_settings.db['font']['static_text'], 
            size=_settings.db['font']['static_text_size'],
            weight="bold"
        )
        self.static_btls_label.configure(
            text=_settings.db['font']['battles_label'],
            font=self.static_stats_font
        )
        
        self.static_wr_label.configure(
            text=_settings.db['font']['winrate_label'],
            font=self.static_stats_font,
        )
        self.static_ac_label.configure(
            text=_settings.db['font']['accuracy_label'],
            font=self.static_stats_font
        )
        self.static_avg_dmg_label.configure(
            text=_settings.db['font']['avg_damage_label'],
            font=self.static_stats_font
        )
        self.btls_label.configure(
            font=self.stats_font,
        )
        
        self.wr_label.configure(
            font=self.stats_font,
        )
        self.ac_label.configure(
            font=self.stats_font,
        )
        self.avg_dmg_label.configure(
            font=self.stats_font,
        )

        self.update()
        
    def update_values(self):
        self.btls_label.configure(text=f"{_session_storage.battles}")
        self.avg_dmg_label.configure(text=f"{int(_session_storage.avg_dmg)}")
        self.wr_label.configure(text=f"{_session_storage.wr:2.2f} %")
        self.ac_label.configure(text=f"{_session_storage.ac:2.2f} %")
        self.update()
        
    def run_watcher(self):
        self.watcher = FileWatchDog(event_handler=self.on_replay_event)

    def on_replay_event(self, event: NewFileEvent):
        try:
            replay_data = self.parser.parse(event.new_file_path)
        except Exception:
            print(f"Failed to parse {event.new_file_path}")
            if ('ZIP' in traceback.format_exc()) and ('invalid Zip archive' not in traceback.format_exc()):
                self.watcher.set_deferred_replay(event.new_file_path)
            
            return
        
        print(f"Data successfully loaded from {event.new_file_path}")
        _session_storage.battles += 1
        _session_storage.wins += 1 if replay_data.winner_team_number == replay_data.author.team_number else 0
        _session_storage.damage_dealt += replay_data.author.damage_dealt
        _session_storage.hits += replay_data.author.n_hits
        _session_storage.shots += replay_data.author.n_shots
        _session_storage.compute()
        self.update_values()
        print('Core: Session calculated')

if __name__ == "__main__":
    app = App()
    app.mainloop()
