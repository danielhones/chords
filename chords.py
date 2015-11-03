import chords_lexer
from chords_parser import parser
from ply import lex


class Song(object):
    def __init__(self, text='', title=''):
        self.sections = []
        self.title = title
        self.text = text

    def parse(self):
        return parser.parse(self.text)

    def lex(self):
        lexer = lex.lex(module=chords_lexer)
        lexer.input(self.text)
        tokens = [token for token in iter(lexer.token, None)]
        return tokens

    def __repr__(self):
        return "Song('%s', title='%s')" % (self.text, self.title)

    def __str__(self):
        return 'Song: ' + self.title


class ChordError(Exception):
    pass

class TransposeError(Exception):
    pass
