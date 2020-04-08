#!/usr/bin/python3
'''
Chord theory
'''

__author__ = "VW Freeh"

import argparse
import logging
import logging.handlers


from notes import Notes, bNotes, nNotes, nextNote, getNoteIdx


# diatonic major is WWHWWWH
MajorScale = [0, 2, 2, 1, 2, 2, 2, 1]
# natural minor WHWWHWW
MinorScale = [0, 2, 1, 2, 2, 1, 2, 2]


def showNotes(args):
    # args.logger.info(str(args))
    print('Notes in the {}{} scale'.format(args.root,
                                           'm' if args.minor else ''))

    # which notes
    if len(args.root) > 1 and args.root[1].lower() == 'b':
        notes = bNotes
    elif args.root.lower() == 'f':
        notes = bNotes
    else:
        notes = Notes

    if args.pentatonic:
        assert True, "TBD"
    elif args.minor:
        scale = MinorScale
    else:
        scale = MajorScale

    note = getNoteIdx(args.root)

    for i, skip in enumerate(scale):
        if args.full and skip > 1:
            print()
        note = (note + skip) % nNotes
        print('{} - {}'.format(i+1, notes[note]))


def showChords(args):
    def chordNotes(root, notes, seq):
        n = []
        for l in seq:
            n.append(notes[(root + l) % nNotes])
        return ', '.join(n)

    # which notes
    if len(args.root) > 1 and args.root[1].lower() == 'b':
        noteNames = bNotes
    else:
        noteNames = Notes

    if args.minor:
        scale = MinorScale
    else:
        scale = MajorScale

    rootIdx = getNoteIdx(args.root)
    x = rootIdx
    notes = []
    for l in scale[1:]:
        notes.append(noteNames[x % nNotes])
        x += l

    print('Notes in the {}{} scale: {}'.format(args.root.title(),
                                               'm' if args.minor else '',
                                               ', '.join(notes)))
    print('Chords')

    # format string: number, name, notes
    fmt = '{:>5s} {:5s} {}'
    if args.minor:
        # minor
        print(fmt.format("i", notes[0]+'m',
                         chordNotes(rootIdx, noteNames, [0, 3, 7])))
        print(fmt.format('ii0', notes[1]+'dim',
                         chordNotes(rootIdx+2, noteNames, [0, 3, 6])))
        print(fmt.format('III', notes[2],
                         chordNotes(rootIdx+3, noteNames, [0, 4, 7])))
        print(fmt.format("iv", notes[3]+'m',
                         chordNotes(rootIdx+5, noteNames, [0, 3, 7])))
        print(fmt.format("v", notes[4]+'m',
                         chordNotes(rootIdx+7, noteNames, [0, 3, 7])))
        print(fmt.format('VI', notes[5],
                         chordNotes(rootIdx+8, noteNames, [0, 4, 7])))
        print(fmt.format('VII', notes[6],
                         chordNotes(rootIdx+10, noteNames, [0, 4, 7])))
    else:
        # major
        print(fmt.format("I", notes[0],
                         chordNotes(rootIdx, noteNames, [0, 4, 7])))
        print(fmt.format('ii', notes[1]+'m',
                         chordNotes(rootIdx+2, noteNames, [0, 3, 7])))
        print(fmt.format('iii', notes[2]+'m',
                         chordNotes(rootIdx+4, noteNames, [0, 3, 7])))
        print(fmt.format("IV", notes[3],
                         chordNotes(rootIdx+5, noteNames, [0, 4, 7])))
        print(fmt.format("V", notes[4],
                         chordNotes(rootIdx+7, noteNames, [0, 4, 7])))
        print(fmt.format('vi', notes[5]+'m',
                         chordNotes(rootIdx+9, noteNames, [0, 3, 7])))
        print(fmt.format('vii0', notes[6]+'dim',
                         chordNotes(rootIdx+11, noteNames, [0, 3, 6])))


def main():
    '''
    show notes in a scale
    '''
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-d', '--debug', action="count",
                        help='set debug level')
    parser.add_argument('-v', '--verbose', action="count",
                        help='set verbose level')
    parser.add_argument('-l', '--logfile', type=str, default='-',
                        help='set log file (default stderr "-")')

    parser.add_argument('--pentatonic', '--dia',
                        action='store_true', default=False,
                        help='show pentatonic scale (default: diatonic)')
    parser.add_argument('--minor', '--min', '-m',
                        action='store_true', default=False,
                        help='show minor (default is major)')
    parser.add_argument('--full', action='store_true', default=False,
                             help='show skipped notes (default=False)')
    parser.add_argument('root', type=str, action='store',
                             help='scale root')

    parser.add_argument('-c', '--chords', '--chord',
                        action='store_true', default=False,
                        help='show chords (default is notes)')

    args = parser.parse_args()

    logger = logging.getLogger()
    if args.logfile == '-':
        # send to stderr
        hdlr = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
    else:
        hdlr = logging.handlers.RotatingFileHandler(args.logfile,
                                                    maxBytes=2**24,  # 4MB
                                                    backupCount=5)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    setattr(args, 'logger', logger)

    if args.chords:
        showChords(args)
    else:
        showNotes(args)


if __name__ == "__main__":
    main()
