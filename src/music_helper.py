import numpy as np
from .music_constants import base_intervals


class MusicHelper:
    def __init__(self, intervals):
        self.intervals = intervals

    def calculate_semitones_from_tonic(self):
        semitones = []
        for interval in self.intervals:
            semitones.append(self.calculate_semitones(interval))
        self.semitones_from_tonic = semitones
        return self.semitones_from_tonic

    def calculate_semitones(self, interval):
        interval_root = base_intervals[interval[-1]]
        accidents = interval[:-1]
        for accident in accidents:
            if accident == '#':
                interval_root += 1
            elif accident == 'b':
                interval_root -= 1
        return interval_root