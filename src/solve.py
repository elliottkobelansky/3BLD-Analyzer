import solveutils
import scramble 
import vectors as vc


def log(log, info):
    buffer, pos, o = info
    buffer = vc.get_name(buffer)
    pos = vc.get_name(pos, o)
    try:
        log[buffer].append(pos)
    except:
        log[buffer] = [pos]

def solve(scram):
    cube = solveutils.Solver()
    cube = scramble.scramble(cube, scram)
    corner_log = {}
    edge_log = {}
    
    
    edge_buffer = vc.get_vector('UF')
    corner_buffer = vc.get_vector('UFR')
    
    while cube.count_solved('corner') < 8:
        if cube.is_permuted(corner_buffer):
            info = cube.cycle_break(corner_buffer)
            log(corner_log, info)
        info = cube.solve_piece(corner_buffer)
        log(corner_log, info)
        
        
    if cube.corner_parity:
        cube.pseudoswap(edge_buffer, (0, 2, 1)) 
    
    while cube.count_solved('edge') < 12:
        if cube.is_permuted(edge_buffer):
            info = cube.cycle_break(edge_buffer)
            log(edge_log, info)
        info = cube.solve_piece(edge_buffer)
        log(edge_log, info)
    
    print(scram) 
    print(corner_log, edge_log)
    
def test():
    cube = solveutils.Solver()
    cube.pseudoswap((1, 2, 0), (0, 2, 1))
    cube.print_cube()

def main():
    with open('scrambles.txt') as f:
        scrams = f.read().splitlines()
    
    scrams = ["L2 U' F2 U' B' F2 L' B F' L2 B R2 U2 L F' L2 D' B2"]
    for scram in scrams:
        solve(scram)
    
if __name__ == "__main__":
    main()