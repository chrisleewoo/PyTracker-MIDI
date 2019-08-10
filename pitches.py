"""
Author: Chris Wootton
Definition of musical pitches 
This takes advantage of the fact that going up one octave 
exactly doubles the note's frequency
"""

import math

class Pitch:
    value = None
    display_note = None
    frequency = None

    def __init__(self):
        self.display_note = '---'
        self.frequency = 0

    def update(self, value):
        if value == self.value:
            return
        self.value = value
        self.fill(value)

    def fill(self, value):
        noteval = value % 12  #this is the key, regardless of octave
        
        if noteval == 0:
            self.display_note = 'c {octave}' .format(octave = value//12)
            self.frequency = 16.35 * ( 1 + (value//12) )
        elif noteval == 1:
            self.display_note = 'c#{octave}'  .format(octave = value//12)
            self.frequency = 17.32 * ( 1 + (value//12) )
        elif noteval == 2:
            self.display_note = 'd {octave}'  .format(octave = value//12)
            self.frequency = 18.35 * ( 1 + (value//12) )
        elif noteval == 3:
            self.display_note = 'd#{octave}' .format(octave = value//12)
            self.frequency = 19.45 * ( 1 + (value//12) )
        elif noteval == 4:
            self.display_note = 'e {octave}' .format(octave = value//12)
            self.frequency = 20.60 * ( 1 + (value//12) )
        elif noteval == 5:
            self.display_note = 'f {octave}' .format(octave = value//12)
            self.frequency = 21.83 * ( 1 + (value//12) )
        elif noteval == 6:
            self.display_note = 'f#{octave}' .format(octave = value//12)
            self.frequency = 23.12 * ( 1 + (value//12) )
        elif noteval == 7:
            self.display_note = 'g {octave}' .format(octave = value//12)
            self.frequency = 24.50 * ( 1 + (value//12) )
        elif noteval == 8:
            self.display_note = 'g#{octave}'  .format(octave = value//12)
            self.frequency = 25.96 * ( 1 + (value//12) )
        elif noteval == 9:
            self.display_note = 'a {octave}'  .format(octave = value//12)
            self.frequency = 27.50 * ( 1 + (value//12) )
        elif noteval == 10:
            self.display_note = 'a#{octave}'  .format(octave = value//12)
            self.frequency = 29.14 * ( 1 + (value//12) )
        elif noteval == 11:
            self.display_note = 'b {octave}' .format(octave = value//12)
            self.frequency = 30.87 * ( 1 + (value//12) )