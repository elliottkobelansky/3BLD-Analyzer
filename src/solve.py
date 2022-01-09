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
        
    while cube.count_solved('edge') < 12:
        if cube.is_permuted(edge_buffer):
            info = cube.cycle_break(edge_buffer)
            log(edge_log, info)
        info = cube.solve_piece(edge_buffer)
        log(edge_log, info)
        
    print(scram, corner_log, edge_log, end='\n\n\n\n')
    

def main():
    with open('scrambles.txt') as f:
        scrams = f.readlines()
    
    for scram in scrams:
        solve(scram)    

if __name__ == "__main__":
    main()