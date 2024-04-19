import numpy as np

from .base_scale import BaseScale
from .music_constants import catalog, base_intervals
from .music_helper import MusicHelper


class Scale(BaseScale):

    def __init__(self, tonic, intervals=None):
        if isinstance(tonic, str):
            super().__init__(tonic)

            if isinstance(intervals, str):
                self.intervals = catalog[intervals.lower()]
            else:
                self.intervals = intervals

            self.music_helper = MusicHelper(self.intervals)
            self.generate_scale()  # here we call generate_scale during initialization
            self.generate_modes()
        
        if isinstance(tonic, list):
            self.notes = tonic
            self.distances = self.calculate_distances_from_notes()
            self.semitones_from_tonic = np.cumsum([1] + self.distances)
            self.intervals = self.calculate_intervals_from_semitones()
            

    def calculate_distances(self):
        semitones = np.array(self.music_helper.calculate_semitones_from_tonic())
        self.semitones_from_tonic = semitones
        distances = semitones[1:] - semitones[:-1]
        self.distances = distances
        return self.distances

    def generate_scale(self):
        distances = self.calculate_distances()
        for i in range(len(self.notes) - 1):
            if "E" in self.notes[i] or "B" in self.notes[i]:    
                difference = distances[i] - 1
            else:
                difference = distances[i] - 2
            self.notes[i+1] += self.calculate_accidents_from_difference(self.notes[i], difference)

        self.notes = [note + self.accident for note in self.notes]
        self.notes = self.debug_mixed_accidents(self.notes)

    def calculate_distances_from_notes(self):
        distances = []

        for i in range(len(self.notes) - 1):
            root = self.notes[i][0]
            accidents1 = self.notes[i][1:]
            accidents2 = self.notes[i+1][1:]

            if np.isin(root, ['E', 'B']):
                distance = 1
            else:
                distance = 2
            
            distance += (accidents2.count('#') - accidents1.count('#')) + (accidents1.count('b') - accidents2.count('b'))
            
            distances.append(distance)

        return distances
    
    def calculate_intervals_from_semitones(self):
        intervals_difference = - np.array(list(base_intervals.values())) + np.array(self.semitones_from_tonic)

        intervals = ['b' * -i + str(j+1) if i < 0 else '#' * i + str(j+1) if i > 0 else str(j+1) for j, i in enumerate(intervals_difference)]

        return intervals
    
    def generate_modes(self):
        modes = []
        for i in range(len(self.notes)):
            mode = self.notes[i:] + self.notes[:i]
            modes.append(mode)
        
        self.modes = modes

        return modes