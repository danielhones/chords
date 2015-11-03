from chords import *
from chords_parser import parser

a = '(Verse)|D-7 G7 | Cmaj7 C7 | Fmaj7 F-6/Ab | C/G G13 ||'
b = 'C-7  F7/A  G9| F-6/Ab |'
c = 'G7b913'
song = '(Verse)|Eb-7 Ab7 | Dbmaj7 Db7|| (Bridge)|Gbmaj7 Gb-6/A|Db/Ab Ab13||'

parser.parse(a)
