import numpy as np
from pydantic import BaseModel, validator
from typing import Union, List, Optional
from app.base_scale import BaseScale
from app.music_constants import catalog, base_intervals
from app.music_helper import MusicHelper

class Scale(BaseScale):
    """Scale class created from the BaseScale class."""

    def __init__(self, tonic: Union[str, List[str]], intervals: Union[str, List[str]] = None) -> None:
        """
        Initializes a new instance of Scale.

        :param tonic: The tonic of the scale, can be a string or a list of strings. 
                    When a list of notes is provided, there is no need to provide the intervals.
        :param intervals: The intervals of the scale as a list of list or just the name of the scale, as a string.
        """
        if isinstance(tonic, str):
            super().__init__(tonic)
            self.intervals = catalog[intervals.lower()] if isinstance(intervals, str) else intervals
            self.music_helper = MusicHelper(self.intervals)
            self.generate_notes()
            self.generate_modes()

        if isinstance(tonic, list):
            self.notes = tonic
            self.distances = self.calculate_distances_from_notes()
            self.semitones_from_tonic = np.cumsum([1] + self.distances)
            self.intervals = self.calculate_intervals_from_semitones()
            self.generate_modes()


    def calculate_distances(self) -> np.ndarray:
        """
        Calculates distances for the scale.

        :return: Returns a numpy array of distances.
        """
        semitones = np.array(self.music_helper.calculate_semitones_from_tonic())
        self.semitones_from_tonic = semitones
        distances = semitones[1:] - semitones[:-1]
        self.distances = distances
        return self.distances

    def generate_notes(self) -> None:
        """
        Generates notes for the scale.
        """
        distances = self.calculate_distances()
        for i in range(len(self.notes) - 1):
            if "E" in self.notes[i] or "B" in self.notes[i]:    
                difference = distances[i] - 1
            else:
                difference = distances[i] - 2
            self.notes[i+1] += self.calculate_accidents_from_difference(self.notes[i], difference)
        self.notes = [note + self.accident for note in self.notes]
        self.notes = self.debug_mixed_accidents(self.notes)

    def calculate_distances_from_notes(self) -> List[int]:
        """
        Calculates distances from notes.

        :return: Returns a list of distances.
        """
        distances = []
        for i in range(len(self.notes) - 1):
            root = self.notes[i][0]
            accidents1 = self.notes[i][1:]
            accidents2 = self.notes[i+1][1:]
            distance = 1 if np.isin(root, ['E', 'B']) else 2
            distance += (accidents2.count('#') - accidents1.count('#')) + (accidents1.count('b') - accidents2.count('b'))
            distances.append(distance)
        return distances
    
    def calculate_intervals_from_semitones(self) -> List[str]:
        """
        Calculates intervals from semitones.

        :return: Returns a list of string representing intervals.
        """
        intervals_difference = - np.array(list(base_intervals.values())) + np.array(self.semitones_from_tonic)
        intervals = ['b' * -i + str(j+1) if i < 0 else '#' * i + str(j+1) if i > 0 else str(j+1) for j, i in enumerate(intervals_difference)]
        return intervals
    
    def generate_modes(self) -> List[str]:
        """
        Generates modes for the scale.

        :return: Returns a list of string representing modes.
        """
        modes = []
        for i in range(len(self.notes)):
            mode = self.notes[i:] + self.notes[:i]
            modes.append(mode)
        self.modes = modes
        return modes
