import ply.yacc as yacc
import ply.lex as lex
from chords_lexer import tokens
from chords import Song, Section, Measure, Chord


# It's important for these rules to be in a top-down order
def p_song(p):
    '''song : song section
            | section'''
    if len(p) == 2:
        p[0] = Song(p[1])
    else:
        p[1].append(p[2])
        p[0] = p[1]
    print 'Song:\n', p[0]


def p_section(p):
    '''section : SECTION_NAME measure_sequence'''
    p[2].name = p[1]
    p[0] = p[2]
    print 'Section:', p[0]


def p_measure_sequence(p):
    '''measure_sequence : measure_sequence measure
                        | measure'''
    if len(p) == 2:
        p[0] = Section(p[1])
    elif len(p) == 3 and type(p[2]) is Measure:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[2].name = p[1]
        p[0] = p[2]
    print 'Measure sequence:', p[0]


def p_measure(p):
    '''measure : chord_sequence barline
               | barline chord_sequence barline'''
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
    #print 'Measure:', p[0]


def p_barline(p):
    '''barline : SINGLE_BARLINE
               | DOUBLE_BARLINE
               | LEFT_REPEAT
               | RIGHT_REPEAT'''
    # TODO: Think about if I need to write a Barline class


def p_chord_sequence(p):
    '''chord_sequence : chord_sequence chord
                      | chord'''
    if len(p) == 2:
        p[0] = Measure(p[1])
    elif len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    #print 'Chord sequence:', p[0]


def p_chord(p):
    '''chord : triad
             | seventh_chord
             | slash_chord'''
    p[0] = p[1]
    #print 'Chord:', p[0]


def p_slash_chord(p):
    '''slash_chord : triad SLASH NOTE
                   | seventh_chord SLASH NOTE'''
    p[1].bass_note = p[3]
    p[0] = p[1]
    #print 'Slash chord:', p[0], '\t',


# I'm having problems dealing with UPPER_STRUCTURE here:
def p_seventh_chord(p):
    '''seventh_chord : triad SEVEN
                     | triad SIX
                     | triad UPPER_STRUCTURE
                     | triad SEVENTH_QUALITY SEVEN
                     | triad SEVENTH_QUALITY UPPER_STRUCTURE'''
    if len(p) == 3:
        p[1].upper_structure = p[2]
    elif len(p) == 4:
        p[1].seventh_quality = p[2]
        p[1].upper_structure = p[3]
    p[0] = p[1]
    #print 'Seventh chord:', p[0], '\t',


def p_triad(p):
    '''triad : NOTE
             | NOTE TRIAD_QUALITY'''
    p[0] = Chord(p[1])
    if len(p) == 3:
        p[0].triad_quality = p[2]
    #print 'Triad:', p[0], '\t',


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input:", p


parser = yacc.yacc()
