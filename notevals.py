def display_note(value):
#take value % 12
    if value == 0:
        displayed_note = ' '
        return displayed_note
    key = value % 12
    if key == 0:
        displayed_note = 'c '
    elif key == 1:
        displayed_note = 'c#'
    elif key == 2:
        displayed_note = 'd '
    elif key == 3:
        displayed_note = 'd#'
    elif key == 4:
        displayed_note = 'e '
    elif key == 5:
        displayed_note = 'f '
    elif key == 6:
        displayed_note = 'f#'
    elif key == 7:
        displayed_note = 'g '
    elif key == 8:
        displayed_note = 'g#'
    elif key == 9:
        displayed_note = 'a '
    elif key == 10:
        displayed_note = 'a#'
    else:
        displayed_note = 'b '

    #then take value / key to get the octave number
    displayed_note += str( int(value/12) ) # rounds down, hopefully
    return displayed_note