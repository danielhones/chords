"""
'|Cmaj7...|Fmaj7.Fmin7.|'


"""

import json
import re


SPACE = '&nbsp;'
MAJOR_SYMBOL = '&#x25b3;'
MINOR_SYMBOL = '-'
DIM_SYMBOL = '&#x25E6;'
FLAT_SIGN = '&#x266d;'
SHARP_SIGN = '&#x266f;'
BAR_LINE = '|'


class ChordChart(object):
    def __init__(self, raw_text):
        self.metadata = {
            'title': '',
            'artist': '',
            'album': '',
            'url': None,
            'form': None,
        }
        self.change_text(raw_text)

    def change_text(self, new_text):
        self.text = new_text
        self.parse_metadata()
        self.parse_chart()
        self.make_html()

    def parse_metadata(self):
        for label in self.metadata:
            look_for = re.compile(r'%s: (?P<value>[^\n]+)' % label, re.IGNORECASE)
            match = look_for.search(self.text)
            if match:
                value = match.group('value')
                self.metadata[label] = value

    def parse_chart(self):
        
        pass

    def make_html(self):
        pass

    def get_json(self):
        pass
    
    def make_json(self):
        metadata, remaining_text = parse_metadata(text)
        chords = parse_chords(remaining_text)
        return make_json(metadata, chords)
    

        
    def parse_chords(self):
        sections = separate_sections(text)
        for section in sections:
            pass
        
        #text = re.sub(r"\s+", "", text, flags=re.UNICODE) # Remove all whitespace
        #clean_text = text.replace('.', SPACE)
        measures = [x for x in clean_text.split(BAR_LINE) if x != '']
        return measures

            
def pretty_print(data):
    print json.dumps(data, indent=4, separators=(',', ': '))
