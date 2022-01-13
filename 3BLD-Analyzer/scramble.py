import re


def scramble(cube, scramble):
    moves = scramble.split()
    
    for move in moves:
        face = move[0]
        if re.search("^[UFRBLD].?2$", move):
            movetype = "180"
        elif re.search("^[UFRBLD].?\'$", move):
            movetype = "CCW"
        elif re.search("^[UFRBLD]$", move):
            movetype = "CW"
        
        if movetype == "180":
            [cube.do_move(face) for i in range(2)]
        elif movetype == "CCW":
            cube.do_move(face, False)
        elif movetype == "CW":
            cube.do_move(face)

    return cube 