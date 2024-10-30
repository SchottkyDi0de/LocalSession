import elara
import os
from pathlib import Path

from lib.data_classes.config_struct import ConfigStruct


_default_settings = {
    "replays_path": "C:/Users/",
    "window": {
        "size_x": 200,
        "size_y": 100,
        "transparent": True,
        "transparency": 0.6
    },
    "font": {
        "static_text": "Consolas",
        "dynamic_text": "Consolas",
        "static_text_size": 16,
        "dynamic_text_size": 16,
        "static_text_color": "white",
        "battles_label": "BTLS: ",
        "winrate_label": "WR:   ",
        "accuracy_label": "AC:   ",
        "avg_damage_label": "DMG:  "
    }
}

documents = Path(os.path.expanduser('~'))\
    .joinpath('Documents')\
    .joinpath('LocalSession')\
    .joinpath('Settings')\
    .joinpath('settings.eldb')

if not documents.exists():
    documents.parent.mkdir(exist_ok=True, parents=True)

os.chmod(documents.parent, 0o777, follow_symlinks=True)

class Settings:
    def __init__(self) -> None:
        self.db = elara.exe(documents)
        _ = self.db['window']
        
        if _ is not None:
            try:
                _ = ConfigStruct.model_validate(self.db.retdb())
            except Exception:
                self.db['window'] = _default_settings['window']
                self.db['replays_path'] = _default_settings['replays_path']
                self.db['font'] = _default_settings['font']
                self.db.commit()
            else:
                print(f'Core: Settings loaded from {documents}')
        else:
            self.db['window'] = _default_settings['window']
            self.db['replays_path'] = _default_settings['replays_path']
            self.db['font'] = _default_settings['font']
            self.db.commit()
            print('Core: Loaded default settings')

    def get(self) -> ConfigStruct:
        return ConfigStruct.model_validate(self.db.retdb())
    
    def get_by_key(self, key):
        return self.db.get(key)

    def set(self, key, value):
        self.db.set(key, value)
        self.db.commit()
        
    def get_raw(self) -> dict:
        return self.db.retdb()

    def __setitem__(self, key, value):
        self.set(key, value)
        self.db.commit()

    def __getitem__(self, key):
        return self.get_by_key(key)

_settings = Settings()
