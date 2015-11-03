"""
TODO: Make these classes (except for chord) conform to iterable protocol, figure out what's necessary
for that.  __iter__ and next() maybe??
"""


class Song(object):
    def __init__(self, sections):
        # TODO: Think about if metadata - title, artist, album, is necessary in this class
        if type(sections) is list:
            self.sections = sections
        else:
            self.sections = [sections]

    def append(self, item):
        self.sections.append(item)

    def __repr__(self):
        return "Song(%s)" % self.sections

    def __str__(self):
        print len(self.sections)
        return '\n'.join([i for i in map(str, self.sections)])


class Section(object):
    def __init__(self, measures, name=None):
        if type(measures) is list:
            self.measures = measures
        else:
            self.measures = [measures]
        self.name = name

    def append(self, item):
        self.measures.append(item)

    def __str__(self):
        name = ''
        if self.name is not None:
            name = '(%s)\n' % self.name
        return name + ' |'.join(map(str, self.measures)) + ' |'

    def __repr__(self):
        return "Section(%s)" % self.measures


class Measure(object):
    def __init__(self, chords):
        if type(chords) is list:
            self.chords = chords
        else:
            self.chords = [chords]

    def append(self, item):
        self.chords.append(item)

    def __str__(self):
        return ' '.join(map(str, self.chords))

    def __repr__(self):
        return "Measure(%s)", self.chords


# TODO: Do I need a class for barlines?
class Barline(object):
    pass


class Chord(object):
    SPACE = '&nbsp;'
    MAJOR_SYMBOL = '&#x25B5;'
    MINOR_SYMBOL = '-'
    DIM_SYMBOL = '&#x25E6;'
    HALF_DIM_SYMBOL = '&oslash;'
    FLAT_SIGN = '&#x266d;'
    SHARP_SIGN = '&#x266f;'
    SHARP_NOTES = ('C', 'C' + SHARP_SIGN, 'D', 'D' + SHARP_SIGN, 'E', 'F',
                   'F' + SHARP_SIGN, 'G', 'G' + SHARP_SIGN, 'A', 'A' + SHARP_SIGN, 'B')
    FLAT_NOTES = ('C', 'D' + FLAT_SIGN, 'D', 'E' + FLAT_SIGN, 'E', 'F',
                  'G' + FLAT_SIGN, 'G', 'A' + FLAT_SIGN, 'A', 'B' + FLAT_SIGN, 'B')

    def __init__(self, root, triad_quality=None, seventh_quality=None, upper_structure=None, bass_note=None):
        # Think about changing these None's to empty strings.  The None's might not have any significance
        self.root = root
        self.triad_quality = triad_quality
        self.seventh_quality = seventh_quality
        self.upper_structure = upper_structure
        self.bass_note = bass_note

    @property
    def is_slash_chord(self):
        return bool(self.bass_note)

    # TODO: Somewhere in here we need to replace # and b with real sharp and flat signs, as well as
    # diminished symbol, half diminished, etc.
    def sub(self):
        return self.root + self._as_string('triad_quality')

    def sup(self):
        return self._as_string('seventh_quality') + self._as_string('upper_structure')

    def __repr__(self):
        attributes = (self.root,
                      self.triad_quality,
                      self.seventh_quality,
                      self.upper_structure)
        return "Chord('%s', '%s', '%s', '%s')" % attributes

    def __str__(self):
        if self.is_slash_chord:
            return "%s%s/%s" % (self.sub(), self.sup(), self.bass_note)
        else:
            return "%s%s" % (self.sub(), self.sup())

    def _as_string(self, attribute):
        try:
            value = vars(self)[attribute]
        except KeyError:
            return ''
        return '' if value is None else value



class ChordError(Exception):
    pass

class TransposeError(Exception):
    pass
