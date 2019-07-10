#!/usr/bin/python
'''
Fretboard: learn notes on a guitar.

Shows notes on the guitar. Three major modes: (1) individual notes;
(2) notes in a chord; and (3) the notes in a pentatonic scale
'''
__author__ = "VW Freeh"

import argparse

Roots = ['E', 'B', 'G', 'D', 'A', 'E']
Notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
bNotes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
nNotes = len(Notes)

nextNote = lambda note, plus:\
           Notes[(Notes.index(note.title()) + plus) % nNotes]
majorNotes = lambda n:\
             (Notes[n], Notes[(n+4)%nNotes], Notes[(n+7)%nNotes], )
minorNotes = lambda n:\
             (Notes[n], Notes[(n+3)%nNotes], Notes[(n+7)%nNotes], )
seventhNotes = lambda n:\
               (Notes[n], Notes[(n+4)%nNotes], Notes[(n+7)%nNotes],
                Notes[(n+10)%nNotes], )
augNotes = lambda n:\
           (Notes[n], Notes[(n+4)%nNotes], Notes[(n+8)%nNotes], )


def getNotes(pnotes, offset, frets):
    notes = []
    for i in range(frets):
        note = Notes[(i+offset) % nNotes]
        if note in pnotes:
            notes.append(note)
        else:
            notes.append(' ')
    return notes


def run(args):
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


def main():
    '''
    Show notes on guitar fret board by (1) note, (2), chord, or (3) scale.
    '''

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-f', '--frets', type=int, default=12,
                        help='select number of frets (default=12)')
    parser.add_argument('-c', '--chord', action='store_true', default=False,
                        help='show all notes in given chord')
    parser.add_argument('--major', '--maj', action='store_true', default=False,
                        help='show major (the default for chord)')
    parser.add_argument('--minor', '--min', action='store_true', default=False,
                        help='show minor(default for pentatonic')
    parser.add_argument('--seventh', '--7', action='store_true',
                        default=False,
                        help='in chord mode: show major 7th')
    parser.add_argument('--aug', action='store_true', default=False,
                        help='in chord mode: show augmented')
    parser.add_argument('--scale', action='store_true', default=False,
                        help='show diatonic scale ')
    parser.add_argument('--pentatonic', '--pent',
                        action='store_true', default=False,
                        help='show pentatonic scale '
                        '(default is minor scale; use --major to change)')
    parser.add_argument('notes', type=str, action='store', nargs="*")

    args = parser.parse_args()
    if args.chord and args.scale:
        raise parser.error('select either "chord" or "scale" not both')

    if args.pentatonic:
        args.scale = True

    nflags = sum([args.major, args.minor, args.seventh, args.aug])
    if args.chord:
        #        setattr(args, 'seventh', args.__dict__['7'])
        if len(args.notes) != 1:
            parser.error('must select {} chord'.format(
                'a' if len(args.notes) == 0 else 'only one'))
        if nflags > 1:
            parser.error('too many chord types')
        chord = args.notes[0].title()
        try:
            idx = Notes.index(chord)
        except ValueError:
            try:
                idx = bNotes.index(chord)
            except ValueError:
                parser.error('unknown chord "{}"'.format(args.notes[0]))
        if nflags == 0 or args.major:
            args.notes = majorNotes(idx)
            print('n', idx, args.notes)
            sup = 'Maj'
        elif args.minor:
            args.notes = minorNotes(idx)
            sup = 'Min'
        elif args.seventh:
            args.notes = seventhNotes(idx)
            sup = '7'
        elif args.aug:
            args.notes = augNotes(idx)
            sup = 'Aug'
        print('Chord: {}{} -- {}\n'.format(chord, sup, ', '.join(args.notes)))
    elif args.scale:
        if len(args.notes) != 1:
            parser.error('must select {} scale'.format(
                'a' if len(args.notes) == 0 else 'only one'))
        scale = args.notes[0].title()
        try:
            idx = Notes.index(scale)
        except ValueError:
            try:
                idx = bNotes.index(scale)
            except ValueError:
                parser.error('unknown note "{}"'.format(args.notes[0]))
        if args.pentatonic:
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
        else:
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

        print('Scale: {} -- {}\n'.format(scale, ', '.join(args.notes)))
    elif args.notes == []:
        # no notes given. show all notes
        args.notes = Notes
        print('Fretboard -- All notes\n')
    else:
        for i in range(len(args.notes)):
            args.notes[i] = args.notes[i].title()
        print('Notes: {}\n'.format(', '.join(args.notes)))

    args.frets += 1
    run(args)


if __name__ == "__main__":
    main()
