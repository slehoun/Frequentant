#!/usr/bin/python3
# Simple script to convert frequency to musical pitch.

from math import log2


def pitch(freq):
    A4 = 440
    double_pedal_C = A4*pow(2, -4.75)
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    half_steps = round(12*log2(freq/double_pedal_C))
    octave = half_steps // 12
    note = half_steps % 12
    return notes[note] + str(octave)

