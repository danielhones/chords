tokens = (
    'NOTE',
    'TRIAD_QUALITY',
    'SEVENTH_QUALITY',
    'SIX',
    'SEVEN',
    'UPPER_STRUCTURE',
    'SLASH',
    'SINGLE_BARLINE',
    'DOUBLE_BARLINE',
    'RIGHT_REPEAT',
    'LEFT_REPEAT',
    'SECTION_NAME',
    'SPACE',
)
# TODO: Figure out the best, most specific regex for upper structure
t_TRIAD_QUALITY = r'min|mi|m|\-|dim|o|\+|aug|5'
t_NOTE = r'[A-G][#b]?'
t_SIX = r'6'
t_SEVEN = r'7'
t_UPPER_STRUCTURE = r'[b#]?9|[b#]?11|[b#]?13|[b#]5|sus4|sus2|alt|ALT|Alt'
t_SLASH = r'/'
t_SINGLE_BARLINE = r'\|'
t_DOUBLE_BARLINE = r'\|\|'
t_RIGHT_REPEAT = r':\|\|'
t_LEFT_REPEAT = r'\|\|:'
t_SECTION_NAME = r'\(.+\)'
t_SPACE = ' \t'

t_ignore = '\n'


# This needs to be before TRIAD_QUALITY because TRIAD_QUALITY matches 'm'
def t_SEVENTH_QUALITY(t):
    r'maj|ma|M|o|dim'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
