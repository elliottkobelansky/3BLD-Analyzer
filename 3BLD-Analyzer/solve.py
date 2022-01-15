import solveutils
import scramble
import cube.vectors as vc
import numpy as np

BUFFERORDER = {
    "corner": ["UFR", "UFL", "UBL", "UBR", "DFR", "DFL", "DBR"],
    "edge": ["UF", "UB", "UR", "UL", "DF", "DB", "FR", "FL", "DR", "DL", "BR"],
}

PSEUDOS = {
    "UFR": ("UF", "UR"),
    "UFL": ("UF", "UL"),
    "UBR": ("UB", "UR"),
    "UBL": ("UB", "UL"),
    "DFR": ("DF", "DR"),
    "DFL": ("DF", "DL"),
    "DBR": ("DB", "DR"),
}


def solve(scram):
    cube = solveutils.Solver()
    cube = scramble.scramble(cube, scram)

    edge_buffers = iter(BUFFERORDER["edge"])
    corner_buffers = iter(BUFFERORDER["corner"])
    edge_buffer = vc.get_vector(next(edge_buffers))
    corner_buffer = vc.get_vector(next(corner_buffers))

    cyclebreaks = 0
    flips = 0
    twists = 0
    numcornerbuffers = 1
    numedgebuffers = 1

    while cube.count_solved("corner") < 8:
        if cube.is_permuted(corner_buffer):
            if cube.is_solved(corner_buffer):
                if not cube.corner_parity:
                    corner_buffer = vc.get_vector(next(corner_buffers))
                    continue
            try:
                cube.cycle_break(corner_buffer)
                cyclebreaks += 1
            except:
                cube.flip_or_twist(corner_buffer)
                twists += 1
        else:
            cube.solve_piece(corner_buffer)
    if cube.corner_parity:
        a, b = PSEUDOS[vc.get_name(corner_buffer)]
        a, b = vc.get_vector(a), vc.get_vector(b)
        try:
            if cube.log['UFR'][-1] == 'BUL':
                a = vc.get_name('UB')
                b = vc.get_name('UL')
        except:
            pass
        cube.pseudoswap(a, b)

    # AFTER THIS DONT EDIT SO WE CAN SAVE
    while cube.count_solved("edge") < 12:
        if cube.is_permuted(edge_buffer):
            if cube.is_solved(edge_buffer):
                if not cube.edge_parity:
                    edge_buffer = vc.get_vector(next(edge_buffers))
                    continue
            try:
                cube.cycle_break(edge_buffer)
                cyclebreaks += 1
            except:
                cube.flip_or_twist(edge_buffer)
                flips += 1
        else:
            cube.solve_piece(edge_buffer)

    # print(scram)
    # print(cube.log)
    values = list(map(list, (ele for ele in cube.log.values())))
    values = sum(values, [])
    algs = int(len(values) / 2) + len(list(values)) % 2
    corner_parity = 1 if cube.corner_parity else 0
    buffers = [x for x in cube.log.keys() if x not in {'twist', 'flip'}]
    cornerbuffers = [x for x in buffers if len(x) == 3]
    edgebuffers = [x for x in buffers if len(x) == 2]


    # print(algs)

    return algs, corner_parity, cyclebreaks, flips, twists, len(cornerbuffers)#, len(edgebuffers)


def test():
    x = solve("U2 D F U B R2 L2 D B2 L2 B2 L' F2 D2 R2 U2 R' D2 L F2")
    print(x)


def main():
    data = []
    with open("scrambles.txt") as f:
        scrams = f.read().splitlines()
    for scram in scrams:
        thissolve = solve(scram)
        data.append([x for x in thissolve])
    return data

if __name__ == "__main__":
    test()
