from chords import *

with open('greendolphin.txt') as f:
    text = f.read()
greendolphin = ChordChart(text)

with open('blues.txt') as f:
    text = f.read()
blues = ChordChart(text)

