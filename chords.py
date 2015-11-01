"""
Compile chord charts to JSON

TODO:
- Make Section and Measure inherit from collections.abc so they can be iterated like a normal list

"""

from collections import deque
import re
import json


BAR_LINE = '|'
HEADER_RE = re.compile(r'(?P<label>\w+)[:][ \t](?P<value>[^\n]+)')
START_MEASURE_RE = re.compile(r'\|{0,1}[A-G.][#b]{0,1}')
START_SECTION_RE = re.compile(r'\((?P<sectionname>\w+)\)')


class Song(object):
    def __init__(self, raw_text):
        self.metadata = {
            'title': '',
            'artist': '',
            'album': '',
            'url': None,
            'form': None,
        }
        self.sections = []
        self.change_text(raw_text)

    def change_text(self, new_text):
        self.text = new_text
        self.lines = deque(self.text.splitlines())
        self.parse_lines()

    def parse_lines(self):
        self.parse_metadata()
        while self.lines:
            try:
                next_line = self.lines.popleft()
            except IndexError:
                # Deque is empty
                return
            if START_SECTION_RE.match(next_line) or START_MEASURE_RE.match(next_line):
                self.lines.appendleft(next_line)
                new_section = SongSection(self.lines)  # This mutates the deque
                self.sections.append(new_section)

    def parse_metadata(self):
        match = HEADER_RE.match(self.lines[0])
        while match:
            label = match.group('label').lower()
            value = match.group('value')
            self.metadata[label] = value
            self.lines.popleft()
            match = HEADER_RE.match(self.lines[0])

    def __repr__(self):
        return 'Song(\'%s\')' % self.text

    def __str__(self):
        return self.metadata['title']

    def transpose(self, semitones):
        for section in self.sections:
            for measure in section.measures:
                for chord in measure.chords:
                    chord.transpose(semitones)
        return self

    def get_json(self, pretty=False):
        indent = 4 if pretty else 0
        data = [json.loads(x.get_json()) for x in self.sections]
        return json.dumps(
            {'metadata': self.metadata,
             'chart': data},
            indent=indent)


class SongSection(object):
    def __init__(self, lines):
        if START_SECTION_RE.match(lines[0]):
            self.section_name = lines[0].strip('()')
            lines.popleft()
        else:
            self.section_name = ''
        self.measures = []
        self.parse_lines(lines)
        self.measures[-1].double_barline = True

    def parse_lines(self, lines):
        while lines:
            try:
                next_line = lines[0]
            except IndexError:
                # Deque is empty
                return
            if START_SECTION_RE.match(next_line):
                # This section is done, a new one has been declared
                return
            elif START_MEASURE_RE.match(next_line):
                new_measures = [x for x in next_line.split(BAR_LINE) if x != '']
                for i in new_measures:
                    self.measures.append(Measure(i))
            lines.popleft()

    def get_json(self):
        data = [json.loads(x.get_json()) for x in self.measures]
        data.insert(0, self.section_name)
        return json.dumps(data)


class Measure(object):
    def __init__(self, text):
        self.text = text
        self.chords = []
        self.double_barline = False
        self.parse_text()

    def parse_text(self):
        new_chords = [x for x in self.text.split() if x != '']
        for i in new_chords:
            self.chords.append(Chord(i))
        
    def get_json(self):
        data = [json.loads(x.get_json()) for x in self.chords]
        return json.dumps(data)
            
    def __repr__(self):
        return 'Measure(\'%s\')' % self.text


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

    def __init__(self, text):
        self.text = text
        self.parse_text()

    def parse_text(self):
        # TODO: clean this up a bit
        if self.text == '.':
            self.rootnote = self.SPACE
            self.quality = ''
            self.slashnote = None
            return
        # TODO: Finish this edit, whatever it was:
        root_and_quality_re = re.compile(
            '''
            (?P<rootnote>[A-G][#b]{0,1})
            (?P<quality>[\w#-]*([5-9]|11|13){0,1})
            '''
            , re.IGNORECASE | re.VERBOSE)
        match = root_and_quality_re.match(self.text)
        if match:
            self.rootnote = match.group('rootnote').capitalize()
            self.quality = match.group('quality')
        slash_re = re.compile('%s%s/(?P<slashnote>[A-G][#b]{0,1})' % (self.rootnote, self.quality))
        match = slash_re.match(self.text)
        if match:
            self.slashnote = match.group('slashnote')
        else:
            self.slashnote = None
        self.prettify()

    def prettify(self):
        # TODO: Make this not suck so bad.
        self.rootnote = self.rootnote.replace('#', self.SHARP_SIGN)
        self.rootnote = self.rootnote.replace('b', self.FLAT_SIGN)
        self.quality = self.quality.replace('#', self.SHARP_SIGN)
        self.quality = self.quality.replace('b', self.FLAT_SIGN)
        # There's more nuance needed here, since 'M' could mean major and 'm' could mean minor, as well
        # as a bunch of other ones.  Plus it would be nice to ignore case for 'maj' and 'min', in order
        # to handle typos and people using caps or whatever.
        self.quality = self.quality.replace('maj', self.MAJOR_SYMBOL)
        self.quality = self.quality.replace('min', self.MINOR_SYMBOL)
        self.quality = self.quality.replace('-7'+self.FLAT_SIGN+'5', self.HALF_DIM_SYMBOL+'7')
        self.quality = self.quality.replace('dim', self.DIM_SYMBOL)
        if self.slashnote:
            self.slashnote = self.slashnote.replace('#', self.SHARP_SIGN)
            self.slashnote = self.slashnote.replace('b', self.FLAT_SIGN)

    def get_json(self):
        # There's got to be a more elegant way to do this:
        return json.dumps(
            {'rootnote': self.rootnote,
             'quality': self.quality,
             'slashnote': self.slashnote})

    def transpose(self, semitones):
        # TODO: clean this up
        semitones = int(semitones) % 12
        if self.rootnote == self.SPACE:
            return
        try:
            note_index = self.SHARP_NOTES.index(self.rootnote)
            new_index = (note_index + semitones) % len(self.SHARP_NOTES)
            self.rootnote = self.SHARP_NOTES[new_index]
        except ValueError:
            try:
                note_index = self.FLAT_NOTES.index(self.rootnote)
                new_index = (note_index + semitones) % len(self.FLAT_NOTES)                
                self.rootnote = self.FLAT_NOTES[new_index]                
            except ValueError:
                raise TransposeError('Couldn\'t find',self.rootnote,'in list of notes')
                

        if self.slashnote:
            try:
                note_index = self.SHARP_NOTES.index(self.slashnote)
                new_index = (note_index + semitones) % len(self.SHARP_NOTES)
                self.slashnote = self.SHARP_NOTES[new_index]
            except ValueError:
                try:
                    note_index = self.FLAT_NOTES.index(self.slashnote)
                    new_index = (note_index + semitones) % len(self.FLAT_NOTES)                
                    self.slashnote = self.FLAT_NOTES[new_index]                
                except ValueError:
                    raise TransposeError('Couldn\'t find',self.slashnote,'in list of notes')


        
    
    def __repr__(self):
        return 'Chord(\'%s\')' % self.text

    def __str__(self):
        return self.text


class TransposeError(Exception):
    pass
