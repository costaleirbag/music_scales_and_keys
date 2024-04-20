import numpy as np
from .scale import Scale

class Key:
    def __init__(self, scale):
        # initialize with a Scale object
        self.scale = scale
        self.chords = self.generate_chords()

    def distance_from_intervals(note1, note2):
        return min(12 - (note2 - note1), note2 - note1)

    def calculate_chord(self, root, intervals):
        chord_name = root
        
        intervals = np.array(intervals) - intervals[0] + 1

        if intervals[1] == 4:
            chord_name += "m"
        if intervals[3] == 12:
            chord_name += "7M"
        elif intervals[3] == 11:
            chord_name += "7"
        if intervals[2] == 7:
            chord_name += "(b5)"
        if intervals[2] == 9:
            chord_name += "(#5)"
        return chord_name

    def generate_chords(self, type='thirds'):
        chords = []
        num_notes = 4 # Tetrads
        if type == "thirds":
            n_steps = 2

        n_notes = len(self.scale.notes)

        for root in range(n_notes):
            intervals = [(self.scale.semitones_from_tonic[(i * n_steps + root) % n_notes] + 12 * \
                          ((i * n_steps + root) // n_notes)) for i in range(num_notes)]
            chord = self.calculate_chord(self.scale.notes[root], intervals)
            chords.append(chord)    
        return chords
