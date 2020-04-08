# support file

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


def getNotes(pnotes, offset, frets):
    notes = []
    for i in range(frets):
        note = Notes[(i+offset) % nNotes]
        if note in pnotes:
            notes.append(note)
        else:
            notes.append(' ')
    return notes
