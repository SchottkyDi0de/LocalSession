from collections.abc import Callable
from time import sleep
from pathlib import Path
from threading import Thread
from datetime import datetime
from dataclasses import dataclass
from cacheout import FIFOCache

from lib.replay_parser.parser import ReplayParser
from settings.settings import _settings

_parser = ReplayParser()

@dataclass
class NewFileEvent:
    new_file_path: Path
    event_timestamp: datetime


class FileWatchDog:
    def __init__(self, event_handler: Callable) -> None:
        self.deferred_replays = FIFOCache(maxsize=50, ttl=2400)
        self.STOP = False
        self.watch_delay = 1
        self.deferred_watch = 10
        self.deferred_watch_delay = 0.5
        self.target_path = _settings.db['replays_path']
        self.event_handler = event_handler
        self._init_iter = True
        
        self.deferred_thread = Thread()
        
        self.watch_thread = Thread(target=self.watch, daemon=True)
        self.deferred_watch_thread = Thread(target=self.deferred_replay_checker, daemon=True)
        
        self.deferred_watch_thread.start()
        self.watch_thread.start()
        print('Threading: File checker started, deferred replay checker started')
        
    def deferred_replay_checker(self):
        while not self.STOP:
            keys = self.deferred_replays.keys()
            
            for key in keys:
                sleep(self.deferred_watch_delay)
                value = self.deferred_replays.get(key=key)
                if value is not None:
                    try:
                        _parser.parse(value)
                    except Exception:
                        pass
                    else:
                        self.deferred_replays.delete(key=key)
                        self.event_handler(NewFileEvent(value, datetime.now()))
                        print(f'Event: deferred replay file {value} loaded')
                    
            sleep(self.deferred_watch)
        
    def set_deferred_replay(self, replay_path: Path) -> None:
        if replay_path in self.deferred_replays.values():
            return
        
        self.deferred_replays.add(key=len(self.deferred_replays.keys()), value=replay_path)
        print('Event: the replay has been deferred until the data is fully loaded')
        
    def stop_watch(self) -> None:
        self.STOP = True
    
    def watch(self) -> None:
        
        old_files = []
        while not self.STOP:
            sleep(self.watch_delay)
            
            files = [path for path in Path(self.target_path).glob('*.wotbreplay') if path.is_file()]
            ...
            if not self._init_iter:
                if len(old_files) == 0:
                    old_files = files.copy()
                    continue
                
                for path in files:
                    if path not in old_files:
                        self.event_handler(NewFileEvent(path, datetime.now()))
                        print(f'Event: new replay {path} found')

            old_files = files.copy()
            
            if self._init_iter:
                self._init_iter = False
