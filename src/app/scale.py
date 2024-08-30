import numpy as np
from typing import Union, List, Optional
from app.base_scale import BaseScale
from app.music_constants import catalog, base_intervals, base_notes
from app.music_helper import MusicHelper
from app.utils import utils

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
            
        if isinstance(tonic, list): 
            # When tonic is not a note but a list of notes
            self.generate_intervals(tonic)
        
        self.generate_modes()
        self.tonic = self.notes[0]
        self.name = self.generate_name()

    def generate_intervals(self, tonic: List[str]) -> None:
        self.notes = tonic
        self.distances = self.calculate_distances_from_notes()
        self.semitones_from_tonic = np.cumsum([1] + self.distances)
        self.intervals = self.calculate_intervals_from_semitones()

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
    
    def generate_name(self) -> Optional[str]:
        """
        Generates the name of the scale by searching the intervals in the catalog.

        :return: Returns the name of the scale.
        """
        for name, intervals in catalog.items():
            if self.intervals == intervals:
                name = f'{self.tonic} {name}'
                if 'ionian' in name:
                    name = name.replace('ionian', 'major')
                return name
        return None
    
    def get_dominant_scale(self, chord_name: 'str') -> BaseScale:
        """
        Gets the dominant scale from a chord name.

        :param chord_name: The chord name.
        :return: Returns the dominant scale.
        """
        chord = generate_chord_notes_from_chord_name(chord_name)
        return self.get_scale_from_dominant_chord_notes(chord)
        
    def get_scale_from_dominant_chord_notes(self, chord: List[str]) -> BaseScale:
        """
        Gets the scale from the dominant chord notes.

        :param dominant: The dominant chord notes.
        :return: Returns the scale notes.
        """
        if isinstance(chord, str):
            chord = chord.split(' ')

        dominant_notes = []
        tonic = chord[0]
        # The dominant scale is the notes from chord + the notes from the scale that are not in the chord
        for note in chord:
            dominant_notes.append(note)
        dominant_roots = [note[0] for note in dominant_notes]
        for note in self.notes:
            note_root = note[0]
            if note_root not in dominant_roots:
                dominant_notes.append(note)
        # Reorder
        dominant_notes = utils.reorder_notes(dominant_notes, tonic)
        dominant_scale = Scale(dominant_notes)
        return dominant_scale
        
    
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
    
    def reorder(self, new_root: str) -> BaseScale:
        """
        Reorders the scale.

        :param new_root: The new root of the scale.
        :return: Returns a new instance of Scale.
        """
        new_notes = utils.reorder_notes(self.notes, new_root)
        return Scale(new_notes)
    

    def __str__(self) -> str:
        return f'{self.name} scale: {self.notes}'
    

def generate_scale_from_chord_name(chord_name: str) -> List['str']:
    """Using the scale class to generate a scale from a chord name.
    The chord name is supposed to be just the root note of the chord."""
    chord_root = chord_name[0]
    tmp_scale = Scale(utils.reorder_notes(base_notes, chord_root))
    chord_intervals = tmp_scale.intervals
    chord_intervals[2], chord_intervals[4], chord_intervals[6] = '3', '5', 'b7'
    tmp_scale = Scale(chord_name, chord_intervals)
    return tmp_scale

def generate_chord_notes_from_chord_name(chord_name: str) -> List[str]:
    return [generate_scale_from_chord_name(chord_name).notes[i] for i in [0, 2, 4, 6]]
