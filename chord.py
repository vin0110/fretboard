#!/usr/bin/python3
'''
Chord theory
'''

__author__ = "VW Freeh"

import argparse
import logging
import logging.handlers

Notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
bNotes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
nNotes = len(Notes)

nextNote = lambda note, plus:\
    Notes[(Notes.index(note.title()) + plus) % nNotes]


def getNoteIdx(note):
    '''returns index of note; raises ValueError if not found'''
    note = note.title()
    try:
        return Notes.index(note)
    except ValueError:
        return bNotes.index(note)


# diatonic major is WWHWWWH
MajorScale = [0, 2, 2, 1, 2, 2, 2, 1]
# natural minor WHWWHWW
MinorScale = [0, 2, 1, 2, 2, 1, 2, 2]


def scale(args):
    # args.logger.info(str(args))
    print('Notes in the {}{} scale'.format(args.root,
                                           'm' if args.minor else ''))

    # which notes
    if len(args.root) > 1 and args.root[1].lower() == 'b':
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


def main():
    '''
    blah, blah
    '''
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-d', '--debug', action="count",
                        help='set debug level')
    parser.add_argument('-v', '--verbose', action="count",
                        help='set verbose level')
    parser.add_argument('-l', '--logfile', type=str, default='-',
                        help='set log file (default stderr "-")')

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands',
        dest='sub', )
    subparsers.required = True

    # subparser for scale
    scaleParser = subparsers.add_parser(
        'scale',
        description='Show scales.',
        help='show scales')
    scaleParser.add_argument('--pentatonic', '--dia',
                             action='store_true', default=False,
                             help='show pentatonic scale (default: diatonic)')
    scaleParser.add_argument('--minor', '--min', '-m',
                             action='store_true', default=False,
                             help='show minor (default is major)')
    scaleParser.add_argument('--full', action='store_true', default=False,
                             help='show skipped notes (default=False)')
    scaleParser.add_argument('root', type=str, action='store',
                             help='scale root')

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

    sub = args.sub
    if sub == 'scale':
        scale(args)
    else:
        assert True, 'should not get here'


if __name__ == "__main__":
    main()
