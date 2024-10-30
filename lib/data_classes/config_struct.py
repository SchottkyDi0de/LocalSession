from pydantic import BaseModel

class Window(BaseModel):
    size_x: int
    size_y: int
    transparent: bool
    transparency: float

class Font(BaseModel):
    static_text: str
    dynamic_text: str
    static_text_size: int
    dynamic_text_size: int
    static_text_color: str
    battles_label: str
    winrate_label: str
    accuracy_label: str
    avg_damage_label: str

class ConfigStruct(BaseModel):
    replays_path: str
    window: Window
    font: Font
