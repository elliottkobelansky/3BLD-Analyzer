import numpy as np
import cube as cb

            
def get_vector(name):
    name.upper()
    v = [1, 1, 1]
    for letter in name:
        v[cb.FACES[letter]['axis']] = cb.FACES[letter]['pos'] + 1
    return tuple(v)

def get_name(v, o=1):
    x, y, z = v
    face_names = {
        'x': {0: 'R', 1: '', 2: 'L'},
        'y': {0: 'D', 1: '', 2: 'U'},
        'z': {0: 'F', 1: '', 2: 'B'}
    }
    v = [face_names['y'][y], face_names['z'][z], face_names['x'][x]]
    if o == 2:
        v[0], v[1] = v[1], v[0]
    if o == 0:
        v[0], v[1], v[2] = v[2], v[0], v[1]
    return "".join(v)

            
def corner_swap_type(v1, v2):
    v1 = np.array(v1) - np.array([1, 1, 1]) 
    v2 = np.array(v2) - np.array([1, 1, 1])
    v_sum = v1 + v2
    if np.count_nonzero(v_sum == 0) == 2:
        return 0
    else:
        return 1
    
def edge_swap_type(v1, v2):
    slices = v1.index(1), v2.index(1)
    s1, s2 = min(slices), max(slices)
    if s1 == s2:
        return 0
    if s1 == 0:
        if s2 == 2:
            return 1
        else:
            return 2 if slices[0] == 0 else 3
    else: 
        return 4
    
def piece_type(v=tuple):
    v = tuple(v)
    zeros = v.count(1)
    types = {0: 'corner', 1: 'edge', 2: 'center', 3: 'core'}
    return types[zeros]

def swap_type(v1, v2):
    type1, type2 = piece_type(v1), piece_type(v2)
    if type1 != type2:
        raise TypeError('Cannot swap two pieces of different types.')
    if type1 == type2 == 'corner':
        return corner_swap_type(v1, v2)
    if type1 == type2 == 'edge':
        return edge_swap_type(v1, v2)
    else:
        raise TypeError('Can only swap corners and edges.')
