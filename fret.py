#!/usr/bin/python3
'''
Fretboard: learn notes on a guitar.

Shows notes on the guitar. Three major modes: (1) individual notes;
(2) notes in a chord; and (3) the notes in a pentatonic scale
'''
__author__ = "VW Freeh"

import argparse
from random import randint


Roots = ['E', 'B', 'G', 'D', 'A', 'E']
Notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
bNotes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
nNotes = len(Notes)

nextNote = lambda note, plus:\
    Notes[(Notes.index(note.title()) + plus) % nNotes]
majorNotes = lambda n:\
    (Notes[n], Notes[(n+4) % nNotes], Notes[(n+7) % nNotes], )
minorNotes = lambda n:\
    (Notes[n], Notes[(n+3) % nNotes], Notes[(n+7) % nNotes], )
seventhNotes = lambda n:\
    (Notes[n], Notes[(n+4) % nNotes], Notes[(n+7) % nNotes],
     Notes[(n+10) % nNotes], )
augNotes = lambda n:\
    (Notes[n], Notes[(n+4) % nNotes], Notes[(n+8) % nNotes], )


def getNotes(pnotes, offset, frets):
    notes = []
    for i in range(frets):
        note = Notes[(i+offset) % nNotes]
        if note in pnotes:
            notes.append(note)
        else:
            notes.append(' ')
    return notes


def showNotes(args):
    print("|".join([' %-2d ' % (i, ) for i in range(args.frets)]))
    print('+'.join(['-'*4]*args.frets))

    # E string (offset 7)
    eNotes = getNotes(args.notes, 7, args.frets)
    print("|".join([' {:2s} '.format(note) for note in eNotes]))
    # B string (offset 2)
    print("|".join([' {:2s} '.format(note)
                    for note in getNotes(args.notes, 2, args.frets)]))
    # G string (offset 10)
    print("|".join([' {:2s} '.format(note)
                    for note in getNotes(args.notes, 10, args.frets)]))
    # D string (offset 5)
    print("|".join([' {:2s} '.format(note)
                    for note in getNotes(args.notes, 5, args.frets)]))
    # A string (offset 0)
    print("|".join([' {:2s} '.format(note)
                    for note in getNotes(args.notes, 0, args.frets)]))
    # E string again
    print("|".join([' {:2s} '.format(note) for note in eNotes]))


def showTriads(root_name):
    root = (Notes.index(root_name) + 5) % 12  # set for the lo E string
    a = (root + 9) % 12
    e = (root + 1) % 12
    d = (root + 4) % 12
    if a == 0:
        a = 12
    if e == 0:
        e = 12
    if d == 0:
        d = 12
    frets = max(12, a, e+1, d+1) + 1

    print('Triads for {}'.format(root_name))
    fret_str = ["%-2d" % (i, ) for i in range(frets)]
    fret_str[root] = "{:2s}".format(root_name)
    print("|".join([' {} '.format(i) for i in fret_str]))
    print('+'.join(['-'*4]*frets))

    # print E (hi)
    notes = [' '] * frets
    notes[d] = "D"
    print("|".join([' {:2s} '.format(note) for note in notes]))

    # print B
    notes = [' '] * frets
    notes[a] = "A"
    notes[d+1] = "D"
    print("|".join([' {:2s} '.format(note) for note in notes]))

    # print G
    notes = [' '] * frets
    notes[a] = "A"
    notes[e] = "E"
    notes[d] = "D"
    print("|".join([' {:2s} '.format(note) for note in notes]))

    # print D
    notes = [' '] * frets
    notes[a] = "A"
    notes[e+1] = "E"
    print("|".join([' {:2s} '.format(note) for note in notes]))

    # print A
    notes = [' '] * frets
    notes[e+1] = "E"
    print("|".join([' {:2s} '.format(note) for note in notes]))

    # print E (lo)
    notes = [' '] * frets
    print("|".join([' {:2s} '.format(note) for note in notes]))


def showCaged(root_name):
    root = (Notes.index(root_name) + 5) % 12  # set for the lo E string
    c = (root + 4) % 12
    a = (root + 7) % 12
    g = (root + 9) % 12
    e = (root) % 12
    d = (root + 2) % 12
    if c == 0:
        c = 12
    if a == 0:
        a = 12
    if g == 0:
        g = 12
    if e == 0:
        e = 12
    if d == 0:
        d = 12
    frets = max(12, c+3, a+2, g+3, e+2, d+3) + 1
    print(root_name, root, a, e, d, frets)

    print('CAGED for {}'.format(root_name))
    fret_str = ["%-2d " % (i, ) for i in range(frets)]
    fret_str[root] = '{:2} '.format(root_name)
    print("|".join([' {}'.format(i) for i in fret_str]))
    print('+'.join(['-'*4]*frets))

    # print E (hi)
    notes = [[' '] * 2 for i in range(frets)]
    notes[c][0] = "C"
    notes[a][0] = "A"
    notes[g+3][0] = "G"
    if notes[e][0] == ' ':
        notes[e][0] = "E"
    else:
        notes[e][1] = "E"
    if notes[d+2][0] == ' ':
        notes[d+2][0] = "D"
    else:
        notes[d+2][1] = "D"
    print("|".join([' {}{} '.format(*note) for note in notes]))

    # print B
    notes = ['  '] * frets
    notes = [[' '] * 2 for i in range(frets)]
    notes[c+1][0] = "C"
    notes[a+2][0] = "A"
    if notes[g][0] == ' ':
        notes[g][0] = "G"
    else:
        notes[g][1] = "G"
    notes[e][0] = "E"
    if notes[d+3][0] == ' ':
        notes[d+3][0] = "D"
    else:
        notes[d+3][1] = "D"
    print("|".join([' {}{} '.format(*note) for note in notes]))

    # print G
    notes = [[' '] * 2 for i in range(frets)]
    notes[c][0] = "C"
    notes[a+2][0] = "A"
    if notes[g][0] == ' ':
        notes[g][0] = "G"
    else:
        notes[g][1] = "G"
    notes[e+1][0] = "E"
    if notes[d+2][0] == ' ':
        notes[d+2][0] = "D"
    else:
        notes[d+2][1] = "D"
    print("|".join([' {}{} '.format(*note) for note in notes]))

    # print D
    notes = [' '] * frets
    notes = [[' '] * 2 for i in range(frets)]
    notes[c+2][0] = "C"
    notes[a+2][0] = "A"
    if notes[g][0] == ' ':
        notes[g][0] = "G"
    else:
        notes[g][1] = "G"
    notes[e+2][0] = "E"
    if notes[d][0] == ' ':
        notes[d][0] = "D"
    else:
        notes[d][1] = "D"
    print("|".join([' {}{} '.format(*note) for note in notes]))

    # print A
    notes = ['  '] * frets
    notes = [[' '] * 2 for i in range(frets)]
    notes[c+3][0] = "C"
    if notes[a][0] == ' ':
        notes[a][0] = "A"
    else:
        notes[a][1] = "A"
    notes[g+2][0] = "G"
    notes[e+2][0] = "E"
    print("|".join([' {}{} '.format(*note) for note in notes]))

    # print E (lo)
    notes = ['  '] * frets
    notes = [[' '] * 2 for i in range(frets)]
    notes[g+3][0] = "G"
    if notes[e][0] == ' ':
        notes[e][0] = "E"
    else:
        notes[e][1] = "E"
    print("|".join([' {}{} '.format(*note) for note in notes]))


def box(args):
    '''print box pentatonic form 1 through 5'''
    form = args.box

    frets = 5
    if form == 1:
        strings = [
            ['m', ' ', ' ', 'M', ' '],
            ['*', ' ', ' ', '*', ' '],
            ['M', ' ', '*', ' ', ' '],
            ['*', ' ', 'm', ' ', ' '],
            ['*', ' ', '*', ' ', ' '],
            ['m', ' ', ' ', 'M', ' '],
        ]
    elif form == 2:
        strings = [
            [' ', 'M', ' ', 'm', ' '],
            [' ', '*', ' ', '*', ' '],
            ['*', ' ', '*', ' ', ' '],
            ['m', ' ', ' ', 'M', ' '],
            ['*', ' ', ' ', '*', ' '],
            [' ', 'M', ' ', '*', ' '],
        ]
    elif form == 3:
        strings = [
            [' ', '*', ' ', '*', ' '],
            [' ', 'm', ' ', ' ', 'M'],
            ['*', ' ', ' ', '*', ' '],
            [' ', 'M', ' ', '*', ' '],
            [' ', '*', ' ', 'm', ' '],
            [' ', '*', ' ', '*', ' '],
        ]
    elif form == 4:
        strings = [
            ['*', ' ', ' ', '*', ' '],
            [' ', 'M', ' ', '*', ' '],
            ['*', ' ', 'm', ' ', ' '],
            ['*', ' ', '*', ' ', ' '],
            ['m', ' ', ' ', 'M', ' '],
            ['*', ' ', ' ', '*', ' '],
        ]
    elif form == 5:
        strings = [
            [' ', '*', ' ', 'm', ' '],
            [' ', '*', ' ', '*', ' '],
            ['m', ' ', ' ', 'M', ' '],
            ['*', ' ', ' ', '*', ' '],
            [' ', 'M', ' ', '*', ' '],
            [' ', '*', ' ', 'm', ' '],
        ]
    else:
        assert False, 'unknown box form'

    print('Pentatonic form {}'.format(form))
    print("|".join([' {:-2d} '.format(i) for i in range(1, frets+1)]))
    print('+'.join(['-'*4]*frets))

    for string in strings:
        print("|".join([' {}  '.format(note) for note in string]))


def playNoteGame(args):
    '''play guess that note'''
    def showBoard(string, fret):
        divider = '+'.join(['-'*4]*(args.frets+1)) + "+"
        print(" 0 ||" + "|".join(
            [' %-2d ' % (i, ) for i in range(1, args.frets+1)]) + "|")
        print(divider)
        marks = [' '] * (args.frets + 1)
        ticks = ['', '', '*', '', '*', '', '**', '', '*', '', '', '**',
                 '', '', '*', '', '*']
        for i in range(6):
            if string == i:
                marks[fret] = '*'
                print(" {} ||".format(marks[0]) + "|".join(
                    [' {}  '.format(mark) for mark in marks[1:]]) + "|")
            else:
                print("   ||" + "|".join(['    '] * args.frets) + "|")
        print(divider)
        print('   ||' + '|'.join(
            [" {:2s} ".format(tick) for tick in ticks[:args.frets]]) + "|")

    nNotes = 6 * args.frets
    count, correct = 0, 0

    while 1:
        rand = randint(0, nNotes)
        theString, theFret = rand % 6, rand // 6
        showBoard(theString, theFret)
        # what is the note
        theNote = nextNote(Roots[theString], theFret)

        for i in range(3):
            try:
                try:
                    guess = input('Name that note ')
                    guess = guess.title()
                    idx = Notes.index(guess)
                except ValueError:
                    try:
                        idx = bNotes.index(guess)
                    except ValueError:
                        print('unknown note "{}"'.format(guess))
                        continue
                theGuess = Notes[idx]
            except (KeyboardInterrupt, EOFError):
                if count > 0:
                    print('\nStatistics: {:.1f}% {} correct out of {}'.format(
                        correct/count*100, correct, count))
                return

            if theNote == theGuess.title():
                print('correct')
                correct += 1
                break
            else:
                print('incorrect')
        else:
            print('the correct note is ', theNote)

        count += 1


def main():
    '''
    Show notes on guitar fret board by (1) note, (2), chord, or (3) scale.
    '''

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-f', '--frets', type=int, default=12,
                        help='select number of frets (default=12)')
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands',
        dest='sub',
        help='command help')

    # subparser for note
    noteParser = subparsers.add_parser('note', help='show chords')
    noteParser.add_argument('notes', type=str, action='store', nargs="*")

    # subparser for chord
    chordParser = subparsers.add_parser('chord', help='show chords')
    chordParser.add_argument('--minor', '--min', '-m',
                             action='store_true', default=False,
                             help='show minor (default is major)')
    chordParser.add_argument('--seventh', '-7', action='store_true',
                             default=False,
                             help='show major 7th')
    chordParser.add_argument('--aug', '-a', action='store_true', default=False,
                             help='show augmented')
    chordParser.add_argument('root', type=str, action='store',
                             help='chord root')

    # subparser for scale
    scaleParser = subparsers.add_parser('scale', help='show scales')
    scaleParser.add_argument('--diantonic', '--dia',
                             action='store_true', default=False,
                             help='show diatonic scale (default: pentatonic')
    scaleParser.add_argument('--box', action='store', type=int,
                             help='show pentatonic box scales: 1-5')
    scaleParser.add_argument('root', type=str, action='store',
                             help='scale root')

    # subparser for caged
    cagedParser = subparsers.add_parser('caged', help='show caged patterns')
    cagedParser.add_argument('--triads', '--tri', action='store_true',
                             default=False,
                             help='show triads ')

    # subparser for game
    gameParser = subparsers.add_parser('game', help='play name that note game')

    parser.add_argument('notes', type=str, action='store', nargs="*")

    args = parser.parse_args()
    print(args)

    sub = args.sub
    if sub == 'note':
        if args.notes == []:
            # no notes given. show all notes
            args.notes = Notes
            print('Fretboard -- All notes\n')
        else:
            for i in range(len(args.notes)):
                args.notes[i] = args.notes[i].title()
        print('Notes: {}\n'.format(', '.join(args.notes)))

        args.frets += 1
        showNotes(args)

    elif sub == 'chord':
        nflags = sum([args.minor, args.seventh, args.aug])
        #        setattr(args, 'seventh', args.__dict__['7'])
        if nflags > 1:
            parser.error('too many chord types')
        chord = args.root.title()
        try:
            idx = Notes.index(chord)
        except ValueError:
            try:
                idx = bNotes.index(chord)
            except ValueError:
                parser.error('unknown chord "{}"'.format(args.notes[0]))
        if args.minor:
            args.notes = minorNotes(idx)
            sup = 'Min'
        elif args.seventh:
            args.notes = seventhNotes(idx)
            sup = '7'
        elif args.aug:
            args.notes = augNotes(idx)
            sup = 'Aug'
            print('Chord: {}{} -- {}\n'.format(
                chord, sup, ', '.join(args.notes)))
        else:
            args.notes = majorNotes(idx)
            print('n', idx, args.notes)
            sup = 'Maj'

        args.frets += 1
        showNotes(args)

    elif sub == 'scale':
        if args.box:
            box(args)
        else:
            scale = args.root.title()
            try:
                idx = Notes.index(scale)
            except ValueError:
                try:
                    idx = bNotes.index(scale)
                except ValueError:
                    parser.error('unknown note "{}"'.format(args.notes[0]))
            if args.pentatonic:
                adjective = 'Pentatonic'
                if args.major:
                    # major pentatonic scale
                    # Root, +2, +2, +3, +2
                    args.notes = [
                        Notes[idx],
                        Notes[(idx + 2) % nNotes],
                        Notes[(idx + 4) % nNotes],
                        Notes[(idx + 7) % nNotes],
                        Notes[(idx + 9) % nNotes],
                    ]
                    adjective = 'Major ' + adjective
                else:
                    # minor pentatonic scale
                    # Root, +3, +2, +2, +3
                    args.notes = [
                        Notes[idx],
                        Notes[(idx + 3) % nNotes],
                        Notes[(idx + 5) % nNotes],
                        Notes[(idx + 7) % nNotes],
                        Notes[(idx + 10) % nNotes],
                    ]
                    adjective = 'Minor ' + adjective
            else:
                adjective = "Diatonic"
                if args.minor:
                    # minor diatonic scale
                    # Root, +2, +1, +2, +2 +1, +2
                    args.notes = [
                        Notes[idx],
                        Notes[(idx + 2) % nNotes],
                        Notes[(idx + 3) % nNotes],
                        Notes[(idx + 5) % nNotes],
                        Notes[(idx + 7) % nNotes],
                        Notes[(idx + 8) % nNotes],
                        Notes[(idx + 10) % nNotes],
                    ]
                    adjective = 'Minor ' + adjective
                else:
                    # major diatonic scale
                    # Root, +2, +2, +1, +2 +2, +2
                    args.notes = [
                        Notes[idx],
                        Notes[(idx + 2) % nNotes],
                        Notes[(idx + 4) % nNotes],
                        Notes[(idx + 5) % nNotes],
                        Notes[(idx + 7) % nNotes],
                        Notes[(idx + 9) % nNotes],
                        Notes[(idx + 11) % nNotes],
                    ]
                    adjective = 'Major ' + adjective

            print('{} Scale: {} -- {}\n'.format(
                adjective, scale, ', '.join(args.notes)))

            args.frets += 1
            showNotes(args)
    elif sub == 'caged':
        if args.triads:
            showTriads(args.notes[0].title())
        else:
            showCaged(args.notes[0].title())

    elif sub == 'game':
        playNoteGame(args)
    else:
        print('unknown command: {}'.format(sub))
        exit(-1)


if __name__ == "__main__":
    main()
