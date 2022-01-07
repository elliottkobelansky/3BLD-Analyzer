import numpy as np
import cube as cb

VECTORS = []
for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            VECTORS.append(np.array([x, y, z]))
            
def pos_to_vector(pos):
    return pos - np.array([1, 1, 1])
 
def get_vector(name):
    name.upper()
    v = [0, 0, 0]
    for letter in name:
        v[cb.FACES[letter]['axis']] = cb.FACES[letter]['pos']
    return np.array(v)

def get_name(v):
    x, y, z = v
    face_names = {
        'x': {-1: 'R', 0: '', 1: 'L'},
        'y': {-1: 'D', 0: '', 1: 'U'},
        'z': {-1: 'F', 0: '', 1: 'B'}
    }
    v = [face_names['y'][y], face_names['z'][z], face_names['x'][x]]
    return "".join(v)

            
def corner_swap_type(v1, v2):
    v_sum = v1 + v2
    if np.count_nonzero(v_sum == 0) == 2:
        return 0
    else:
        return 1
    
def edge_swap_type(v1, v2):
    slices = np.where(v1 == 0)[0][0], np.where(v2 == 0)[0][0]
    s1, s2 = min(slices), max(slices)
    if s1 == s2:
        return 0
    if s1 == 0:
        return 1 if s2 == 2 else 2
    else: 
        return 3
    
def piece_type(v):
    zeros = np.count_nonzero(v == 0) 
    types = {0: 'Corner', 1: 'Edge', 2: 'Center', 3: 'Core'}
    return types[zeros]

def swap_type(v1, v2):
    type1, type2 = piece_type(v1), piece_type(v2)
    if type1 != type2:
        return TypeError('Cannot swap two pieces of different types.')
    if type1 == type2 == 'Corner':
        return corner_swap_type(v1, v2)
    if type1 == type2 == 'Edge':
        return edge_swap_type(v1, v2)
    else:
        return TypeError('Can only swap corners and edges.')
