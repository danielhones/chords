from chords import *

with open('greendolphin.txt') as f:
    text = f.read()
greendolphin = ChordChart(text)

x = Chord('C#maj13#11/F')
y = Chord('F7')
