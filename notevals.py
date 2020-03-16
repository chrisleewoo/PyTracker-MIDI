def display_note(value):
#take value % 12
    if value == 0:
        displayed_note = ' '
        return displayed_note
    key = value % 12
    if key == 0:
        displayed_note = 'C '
    elif key == 1:
        displayed_note = 'C#'
    elif key == 2:
        displayed_note = 'D '
    elif key == 3:
        displayed_note = 'D#'
    elif key == 4:
        displayed_note = 'E '
    elif key == 5:
        displayed_note = 'F '
    elif key == 6:
        displayed_note = 'F#'
    elif key == 7:
        displayed_note = 'G '
    elif key == 8:
        displayed_note = 'G#'
    elif key == 9:
        displayed_note = 'A '
    elif key == 10:
        displayed_note = 'A#'
    else:
        displayed_note = 'B '

    #then take value / key to get the octave number
    displayed_note += str( int(value/12) ) # rounds down, hopefully
    return displayed_note