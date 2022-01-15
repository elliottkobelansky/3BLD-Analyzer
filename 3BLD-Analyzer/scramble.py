import re

# Rw' -> L'
# Rw -> R
# Fw -> B
# Fw' -> B'
# Uw -> D

# Rw: Fw = U, Uw = B
# Rw': Fw = D, Uw = F
# Rw2: Fw = F, Uw = U
# Fw: Uw = R, Rw = D
# Fw': Uw = L, Rw = U
# Uw: Fw = L, Rw = F
# Uw': Fw = R, Rw = B
#
# 1st move: opposite
# 2nd move: depends on the first, if ' then different, if 2 then same
OPPOMOVE = {"R": "L", "F": "B", "U": "D", "B": "F", "L": "R", "D": "U"}

BROIHO = {
    "R": {"F": "U", "U": "B"},
    "F": {"U": "R", "R": "D"},
    "U": {"F": "L", "R": "F"},
}


def do_move(cube, face, movetype):
    if movetype == "180":
        [cube.do_move(face) for i in range(2)]
    elif movetype == "CCW":
        cube.do_move(face, False)
    elif movetype == "CW":
        cube.do_move(face)


def scramble(cube, scramble):
    moves = scramble.split()
    widemoves = [move for move in moves if "w" in move]
    moves = [move for move in moves if "w" not in move]

    if widemoves:
        move = widemoves[0]
        wideface = move[0]
        realface = OPPOMOVE[wideface]
        realmove = move.replace(f"{wideface}w", realface)
        moves.append(realmove)
        if len(widemoves) == 2:
            secondmove = widemoves[1]
            secondwideface = secondmove[0]
            if "'" in move:
                secondrealface = OPPOMOVE[BROIHO[wideface][secondwideface]]
            elif "2" in move:
                secondrealface = secondwideface
            else:
                secondrealface = BROIHO[wideface][secondwideface]
            secondrealmove = secondmove.replace(f"{secondwideface}w", secondrealface)
            moves.append(secondrealmove)

    for move in moves:
        if "w" in move:
            break
        face = move[0]
        if "2" in move:
            movetype = "180"
        elif "'" in move:
            movetype = "CCW"
        else:
            movetype = "CW"

        do_move(cube, face, movetype)

    return cube


if __name__ == "__main__":
    scramble("", "R U B D Rw' Fw2")
