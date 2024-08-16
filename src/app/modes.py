import numpy as np
from app.scale import Scale
from app.key import Key

class Modes:
    def __init__(self, scale):
        # initialize with a Scale object
        self.scale = scale
        self.notes = scale.modes
        self.tonic = self.notes[0][0]
        self.generate_intervals()
        self.generate_chords()

    def generate_intervals(self):
        intervals = []
        for mode in self.notes:
            intervals.append(Scale(mode).intervals)
        self.intervals = intervals

    def generate_chords(self):
        chords = []
        for mode in self.intervals:
            #from pdb import set_trace; set_trace()
            chords.append(Key(Scale(self.tonic, mode)).chords)
        self.chords = chords