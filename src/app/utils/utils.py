import numpy as np
from typing import Union, List, Optional
from app.base_scale import BaseScale
from app.music_constants import catalog, base_intervals, base_notes
from app.music_helper import MusicHelper

def reorder_notes(notes: List[str], tonic: str) -> List[str]:
    """
    Reorders notes by looking at the non accidental letters, following the cyclic order of the notes:
    C, D, E, F, G, A, B, C, D, E, F, G, A, B, ...
    Example:
    reorder_notes(["D", "C#", "E", "B", "A", "F#", "G#"], "C#") -> ["C#", "D", "E", "F#", "G#", "A", "B"]

    :param notes: A list of notes to be reordered.
    :param tonic: The tonic note.
    :return: A list of reordered notes.
    """
    # Define the order of the notes in the musical scale
    scale_order = base_notes

    # Extract the non-accidental part of the tonic
    tonic_base = tonic[0]

    # Find the index of the tonic's base note in the scale order
    tonic_index = scale_order.index(tonic_base)

    # Create a new order starting from the tonic's base note
    reordered_scale = scale_order[tonic_index:] + scale_order[:tonic_index]

    # Create a helper function to get the base note from a given note
    def base_note(note: str) -> str:
        return note[0]

    # Sort the notes based on their position in the reordered scale
    sorted_notes = sorted(notes, key=lambda note: reordered_scale.index(base_note(note)))

    return sorted_notes

def calculate_distances_from_notes(notes: List[str]) -> List[int]:
        """
        Calculates distances from notes.

        :return: Returns a list of distances.
        """
        distances = []
        for i in range(len(notes) - 1):
            root = notes[i][0]
            accidents1 = notes[i][1:]
            accidents2 = notes[i+1][1:]
            distance = 1 if np.isin(root, ['E', 'B']) else 2
            distance += (accidents2.count('#') - accidents1.count('#')) + (accidents1.count('b') - accidents2.count('b'))
            distances.append(distance)
        return distances

def distance_from_intervals(note1, note2):
    return min(12 - (note2 - note1), note2 - note1)
    
