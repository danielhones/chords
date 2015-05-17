from chords import *

with open('testchords.txt') as f:
    text = f.read()

ch = ChordChart(text)
