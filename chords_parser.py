import ply.yacc as yacc
from chords_lexer import tokens


def p_triad(p):
    '''triad : NOTE
             | NOTE TRIAD_QUALITY'''


def p_seventh(p):
    '''seventh : SEVEN
               | SEVENTH_QUALITY SEVEN
               | SEVENTH_QUALITY UPPER_STRUCTURE
               | SIX'''


def p_seventh_chord(p):
    '''seventh_chord : triad seventh
                     | triad seventh UPPER_STRUCTURE'''


def p_root_chord(p):
    '''chord : triad
             | seventh_chord'''


def p_slash_chord(p):
    '''slash_chord : root_chord SLASH NOTE'''


def p_chord(p):
    '''chord : root_chord SPACE
             | slash_chord SPACE'''


def p_chord_sequence(p):
    '''chord_sequence : chord
                      | chord chord_sequence'''


def p_barline(p):
    '''barline : SINGLE_BARLINE
               | DOUBLE_BARLINE
               | LEFT_REPEAT
               | RIGHT_REPEAT'''


def p_measure(p):
    '''measure : chord_sequence barline
               | barline chord_sequence barline'''


def p_section(p):
    '''section : SECTION_NAME section
               | measure section
               | measure DOUBLE_BARLINE'''




# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()
