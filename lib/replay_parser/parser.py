import os
import pathlib
import subprocess
from threading import Thread
import traceback

from lib.data_classes.replay_data import ReplayData


_EXE = 'parser.exe' if os.name == 'nt' else 'parser'
_PATH = 'lib/replay_parser/bin/' + _EXE
_ARGUMENT = 'battle-results'


class PathNotExists(Exception):
    pass


class ReplayParserError(Exception):
    pass


class ReplayParser:
    def __init__(self) -> None:
        self.res: ReplayData = None
        self.exc: Exception = None
    
    def parse(self, replay_path: str, save_json: bool = False) -> ReplayData:
        """
        Parse a replay file and return the parsed data.
        
        Args:
            replay_path (str): The path to the replay file.
            auto_clear (bool, optional): Whether to automatically delete the replay file after parsing. Defaults to True.
            save_json (bool, optional): Whether to save the parsed data as a JSON file. Defaults to False.
        
        Returns:
            ReplayData: The parsed replay data.
        
        Raises:
            PathNotExists: If the specified replay file does not exist.
            ReplayParserError: If an error occurs while parsing the replay file.
        
        """
        def _parse_in_thread():
            self.res = None
            self.exc = None
            
            path = pathlib.PurePath(replay_path)
            if not pathlib.Path(replay_path).exists():
                print(f'Path {replay_path} does not exist')
                self.exc = PathNotExists(replay_path)

            replay_parser = subprocess.Popen([_PATH, _ARGUMENT, str(path)], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            try:
                stdout, stderr = replay_parser.communicate(timeout=5)
            except subprocess.TimeoutExpired():
                print(f'Failed to parse replay {replay_path}, TIMEOUT EXCEEDED')
                self.exc = ReplayParserError(f'Failed to parse replay {replay_path}, TIMEOUT EXCEEDED')
                return
            except Exception():
                print(f'Failed to parse replay {replay_path}, unknown error')
                print(traceback.format_exc())
                self.exc = ReplayParserError(f'Failed to parse replay {replay_path}, unknown error')
                return
            finally:
                replay_parser.terminate()

            if replay_parser.returncode != 0:
                self.exc = ReplayParserError(stderr.decode('utf-8'))
                return
            
            if save_json:
                with open(f'{replay_path}.json', 'w') as f:
                    f.write(stdout.decode('utf-8'))

            self.res = ReplayData.model_validate_json(stdout)
            
        thread = Thread(target=_parse_in_thread)
        thread.start()
        thread.join()
        
        if self.exc is not None:
            raise self.exc
        
        return self.res
