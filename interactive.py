from chords import *

with open('greendolphin.txt') as f:
    text = f.read()
greendolphin = ChordChartMaker(text)
print 'greendolphin = ChordChartMaker(text)'


with open('blues.txt') as f:
    text = f.read()
blues = ChordChartMaker(text)
print 'blues = ChordChartMaker(text)'
