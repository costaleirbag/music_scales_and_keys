from app.scale import Scale
from app.key import Key
from app.modes import Modes
from typing import Union, List, Optional

class Music:
    def __init__(self, tonic: Union[str, List[str]], intervals: Union[str, List[str]] = None):
        self.scale = Scale(tonic, intervals)
        self.key = Key(self.scale)
        self.modes = Modes(self.scale)

    # Direct access to the composed objects
    def __getattr__(self, name):
        # Check Scale, Key, and Modes for the requested method
        if hasattr(self.scale, name):
            return getattr(self.scale, name)
        elif hasattr(self.key, name):
            return getattr(self.key, name)
        elif hasattr(self.modes, name):
            return getattr(self.modes, name)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

if __name__ == "__main__":
    music = Music("C D E F G A B".split(' '))
    print(music.notes)
    print(music.chords)
    print(music.modes.notes)
