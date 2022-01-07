#!/usr/bin/env python3

import cube as cb
import scramble
import vectors as vc
import numpy as np

class Solver(cb.Cube):
    def __init__(self):
        super().__init__()
        self.edge_parity = False
        self.corner_parity = False

    def count_solved_pieces(self):
        counter = 0 
        for piece in self.cube.flatten():
            if self.is_solved(piece.pos):
                counter += 1
        return counter

    def where_to(self, index):
        pos = tuple(self.cube[index].pos)
        return pos, tuple(self.cube[pos].ori)

    def swap_piece(self, pos1, pos2, ori=0):
        # Pass in the 1st and 2nd pieces coordinates
        # However, this doesn't tell us the orientation of the piece
        # If we have a certain piece we have to shoot to, we know the orientation
        # If we are breaking, we have to specify the orientation as a 3tuple
        # We have to somehow get that 3tuple
        v1, v2 = vc.pos_to_vector(pos1), vc.pos_to_vector(pos2)
    
        swap_type = vc.swap_type(v1, v2) 
        
        if swap_type == 1:
            self.swap_colors(pos1, pos2, 0, 2)
        if swap_type == 2:
            self.cube[pos1].ori = np.roll(self.cube[pos1].ori, 1)
            self.cube[pos2].ori = np.roll(self.cube[pos2].ori, -1)
        if swap_type == 3:
            self.swap_colors(pos1, pos2, 1, 2)
        self.swap_pos(pos1, pos2)
        
    def solve_piece(self, p):
        o = self.cube[p].ori
        pos, ori = self.where_to(p)
        self.swap_pos(p, pos)
        self.cube[p].ori, self.cube[pos].ori = self.put_colors(o, ori)
        if self.cube[p].is_edge():
            self.edge_parity = not self.edge_parity
        else:
            self.corner_parity = not self.corner_parity    
        
        return vc.get_name(vc.pos_to_vector(p)), vc.get_name(vc.pos_to_vector(pos))    
    
    def put_colors(self, a, b):
        a, b = np.array(a), np.array(b)
        tmp1, tmp2 = [0, 0, 0], [0, 0, 0]
        for i in range(3):
            tmp1[i], tmp2[a[i]] = b[a[i]], a[i]
        a, b = np.array(tmp1), np.array(tmp2)
        return a, b
                
            
    def swap_colors(self, pos1, pos2, a, b):
        pos1, pos2 = tuple(pos1), tuple(pos2)
        first = self.cube[pos1]
        second = self.cube[pos2]
        for x in (first, second):
            x.ori[a], x.ori[b] = x.ori[b], x.ori[a]
        self.cube[pos1], self.cube[pos2] = first, second 
            
        
    def swap_pos(self, pos1, pos2):
        pos1, pos2 = tuple(pos1), tuple(pos2)
        self.cube[pos1], self.cube[pos2] = self.cube[pos2], self.cube[pos1]
        
    def rotate_pieces(self, pos1, pos2, k, relparity=True):
        self.cube[pos1].ori = np.roll(self.cube[pos1].ori, k)
        if relparity:
            k = -k
        self.cube[pos2].ori = np.roll(self.cube[pos2].ori, k)
        
        # -1 refers to x, 1 refers to z
    
    def is_permuted(self, pos):
        pos = tuple(pos)
        return True if pos == tuple(self.cube[pos].pos) else False
        
        
    def is_solved(self, pos):
        pos = tuple(pos)
        if self.is_permuted(pos) and tuple(self.cube[pos].pos).count(1) <= 1 \
        and tuple(self.cube[pos].ori) == (0, 1, 2): 
            return True
        else:
            return False   
       
        
def solve(scram, **kwargs):
    cube = Solver()
    cube = scramble.scramble(cube, scram)
    
    a = vc.get_vector('UFR') + np.array([1, 1, 1])
    b = vc.get_vector('UF') + np.array([1, 1, 1])
    a = tuple(a)
    b = tuple(b)
    
    while not cube.is_permuted(a):
        print(cube.solve_piece(a))
        print(cube.count_solved_pieces())
    print(cube.corner_parity)
    while not cube.is_permuted(b):
        print(cube.solve_piece(b))
        print(cube.count_solved_pieces())
    print(cube.edge_parity)
        
    cube.print_cube()
 
if __name__ == "__main__":
    solve("U' R2 D L2 F2 U B2 F2 U2 F2 U B L' B D F' R' U' F' R2")