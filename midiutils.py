import re

# Adapted from note_name_to_number function:
# https://github.com/craffel/pretty-midi/blob/master/pretty_midi/utilities.py#L293

def note_name_to_midi_note_number(note_name):


    # Map note name to the semitone
    pitch_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    
    # Does AutoSampler always use sharps? If not, does it use 'b' for flats?
    acc_map = {'#': 1, '': 0, 'b': -1, '!': -1}

    # Reg exp will raise an error when the note name is not valid
    try:
        # Extract pitch, octave, and accidental from the supplied note name
        match = re.match(r'^(?P<note>[A-Ga-g])(?P<accidental>[#b!]?)(?P<octave>[+-]?\d+)$',
                         note_name)

        pitch = match.group('note').upper()
        offset = acc_map[match.group('accidental')]
        octave = int(match.group('octave'))
    except:
        raise ValueError('Improper note format: {}'.format(note_name))

    return 12*(octave + 1) + pitch_map[pitch] + offset