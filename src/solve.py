import solveutils
import scramble 
import cube.vectors as vc


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
        if cube.count_solved('corner') == 7:
            cube.print_cube()
        if cube.is_permuted(corner_buffer):
            try: 
                info = cube.cycle_break(corner_buffer)
            except:
                info = cube.flip_or_twist(corner_buffer)    
        else:
            info = cube.solve_piece(corner_buffer)
        log(corner_log, info)
        
    if cube.corner_parity:
        cube.pseudoswap(edge_buffer, (0, 2, 1)) 
    
    while cube.count_solved('edge') < 12:
        if cube.is_permuted(edge_buffer):
            try: 
                info = cube.cycle_break(edge_buffer)
            except:
                info = cube.flip_or_twist(edge_buffer)
        else:
            info = cube.solve_piece(edge_buffer)
        log(edge_log, info)
    
    print(scram) 
    print(corner_log, edge_log)
    
def test(scram):
    edge_log = {}
    cube = solveutils.Solver()
    cube = scramble.scramble(cube, scram)
    while cube.count_solved('edge') < 12:
        if cube.is_permuted((1, 2, 0)):
            try: 
                info = cube.cycle_break((1, 2, 0))
            except:
                info = cube.flip_or_twist((1, 2, 0))
        else:
            info = cube.solve_piece((1, 2, 0))
        log(edge_log, info)
        
    print(scram, edge_log)
            
def main():
    with open('scrambles.txt') as f:
        scrams = f.read().splitlines()
    
    for scram in scrams:
        solve(scram)
    
if __name__ == "__main__":
    main()