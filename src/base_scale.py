import numpy as np

from .music_constants import base_notes


class BaseScale:
    def __init__(self, tonic):
        self.tonic = tonic[:1]
        self.accident = tonic[1:]
        self.notes = base_notes[base_notes.index(self.tonic):] + base_notes[:base_notes.index(self.tonic)]

    def calculate_accidents_from_difference(self, note, difference):
        if difference > 0:
            return '#'*abs(difference - note.count('b'))
        elif difference < 0:
            return 'b'*abs(difference - note.count('#'))
        else:
            if "#" in note:
                return "#"
            if "b" in note:
                return "b"
            else:
                return ''
            
    def debug_mixed_accidents(self, notes):
        return [note.replace('#b', '').replace('b#', '') for note in notes]