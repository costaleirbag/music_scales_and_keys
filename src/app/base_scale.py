import numpy as np

from app.music_constants import base_notes


class BaseScale:
    def __init__(self, tonic):
        self.tonic = tonic[:1]
        self.accidental = tonic[1:]
        self.notes = base_notes[base_notes.index(self.tonic):] + base_notes[:base_notes.index(self.tonic)]

    def calculate_accidentals_from_difference(self, note, difference):
        if difference > 0:
            return '#'*abs(difference - note.count('b'))
        elif difference < 0:
            return 'b'*abs(note.count('#') + difference - note.count('b'))
        else:
            if "#" in note:
                return "#"
            if "b" in note:
                return "b"
            else:
                return ''
            
    def debug_mixed_accidentals(self, notes):
        return [note.replace('#b', '').replace('b#', '') for note in notes]