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
        self.cornerlog = {}
        self.edgelog = {}
    
    def count_solved(self, piecetype=None):
        counter = 0
        for piece in self.cube.flatten():
            if self.is_solved(piece.pos):
                piece_type = vc.piece_type(piece.pos)
                if not piecetype or piece_type == piecetype: 
                        counter += 1
        return counter

    def where_to(self, buffer):
        return self.cube[buffer].pos

    def swap_piece(self, buffer, pos, ori=0, ct=False):
        # Pass in the 1st and 2nd pieces coordinates
        # However, this doesn't tell us the orientation of the piece
        # If we have a certain piece we have to shoot to, we know the orientation
        # If we are breaking, we have to specify the orientation as a 3tuple
        # We have to somehow get that 3tuple
        swap_type = vc.swap_type(buffer, pos)
        o = self.cube[buffer].ori[1]
        
        if swap_type == 1:
            self.swap_colors(buffer, pos, 0, 2)
        if swap_type == 2:
            self.cube[buffer].ori = np.roll(self.cube[buffer].ori, 1)
            self.cube[pos].ori = np.roll(self.cube[pos].ori, -1)
        if swap_type == 3:
            o = self.cube[pos1].ori[2]
            self.cube[buffer].ori = np.roll(self.cube[buffer].ori, -1)
            self.cube[pos].ori = np.roll(self.cube[pos].ori, 1)
        if swap_type == 4:
            if pos1.index(1) == 1:
                o = self.cube[buffer].ori[2]
            self.swap_colors(buffer, pos, 1, 2)
        self.swap_pos(buffer, pos)
        if ct:
            o = 1
        self.add_to_log(buffer, pos, o)
        
        return 
    
       
    def solve_piece(self, buffer):
        pos = self.where_to(buffer)
        self.add_to_log(buffer, pos)
        self.put_colors(buffer, pos)
        self.swap_pos(buffer, pos)
        self.change_parity(buffer)
        return
       
    def change_parity(self, buffer):
        piecetype = vc.piece_type(buffer) 
        if piecetype == 'corner':
            self.corner_parity = not self.corner_parity
        if piecetype == 'edge':
            self.edge_parity = not self.edge_parity
    
    def put_colors(self, buffer, pos):
        a, b = self.cube[buffer].ori, self.cube[pos].ori
        tmp1, tmp2 = [0, 0, 0], [0, 0, 0]
        for i in range(3):
            tmp1[i], tmp2[a[i]] = b[a[i]], a[i]
        self.cube[buffer].ori, self.cube[pos].ori = b, a
                
    def swap_colors(self, pos1, pos2, a, b):
        first = self.cube[pos1].ori
        second = self.cube[pos2].ori
        self.print_cube()
        for x in (first, second):
            x[a], x[b] = x[b], x[a]
        self.cube[pos2].ori, self.cube[pos1].ori = first, second
        
    def swap_pos(self, pos1, pos2):
        self.cube[pos1], self.cube[pos2] = self.cube[pos2], self.cube[pos1]
        
    def rotate_pieces(self, pos1, pos2, k, relparity=True):
        self.cube[pos1].ori = np.roll(self.cube[pos1].ori, k)
        if relparity:
            k = -k
        self.cube[pos2].ori = np.roll(self.cube[pos2].ori, k)
        
        # -1 refers to x, 1 refers to z
    
    def is_permuted(self, pos):
        return True if pos == self.cube[pos].pos else False
        
    def is_solved(self, pos):
        if self.is_permuted(pos) and self.cube[pos].pos.count(1) <= 1 \
        and tuple(self.cube[pos].ori) == (0, 1, 2): 
            return True
        else:
            return False   
        
    def find_unsolved_piece(self, buffer):
        buffer_type = vc.piece_type(buffer)
        for piece in self.cube.flatten():
            if buffer_type == vc.piece_type(piece.pos):
                if not self.is_permuted(piece.pos) \
                    and piece.pos != self.cube[buffer].pos:
                    return piece.pos
                
    def find_flipped_piece(self, buffer):
        buffer_type = vc.piece_type(buffer)
        for piece in self.cube.flatten():
            pos = piece.pos
            if buffer_type == vc.piece_type(pos):
                if not self.is_solved(pos) \
                   and self.is_permuted(pos) \
                   and pos != self.cube[buffer].pos:
                       return piece.pos
                   
    def add_to_log(self, buffer, pos, axis=None):
        buffer_name = vc.get_name(buffer)
        axis = self.cube[buffer].ori[1] if not axis else axis
        piecetype = vc.piece_type(buffer)
        pos = vc.get_name(pos, axis)
        if piecetype == 'corner':
            try: 
                self.cornerlog[buffer_name].append(pos)
                return
            except:
                self.cornerlog[buffer_name] = [pos]
                return
        elif piecetype == 'edge':
            try:
                self.edgelog[buffer_name].append(pos)
                return
            except:
                self.edgelog[buffer_name] = [pos]
                return
                
    def alg_count(self):
        count = 0
        for bufferlog in self.cornerlog.values():
            count += len(bufferlog)
        for bufferlog in self.edgelog.values():
            count += len(bufferlog)
        return int(count / 2)
        
       
        
def solve(scram, **kwargs):
    cube = Solver()
    print(scram)
    cube = scramble.scramble(cube, scram)
    
    a = vc.get_vector('UFR')
    b = vc.get_vector('UF')
    a = tuple(a)
    b = tuple(b)
    
    def solve_pieces(buffer):
        piecetype = vc.piece_type(buffer)
        if (piecetype == 'corner' and cube.count_solved('corner') == 8) \
           or (piecetype == 'edge' and cube.count_solved('edge') == 12):
            return 0
        if not cube.is_permuted(buffer):
            cube.solve_piece(buffer)
            cube.count_solved()
            return solve_pieces(buffer)
        return 1
                
    
    while cube.count_solved('corner') < 8:
        if cube.is_permuted(a):
            cycle_break = cube.find_unsolved_piece(a)
            if cycle_break:
                cube.swap_piece(a, cycle_break, ct=True)
            elif not cycle_break:
                twisted_piece = cube.find_flipped_piece(a)
                cube.swap_piece(a, twisted_piece, ct=True)
        solve_pieces(a)
    
     
    while cube.count_solved('edge') < 12:
        if cube.is_permuted(b):
            cycle_break = cube.find_unsolved_piece(b)
            if cycle_break:
                cube.swap_piece(b, cycle_break, ct=True)
            elif not cycle_break:
                flipped_piece = cube.find_flipped_piece(b)
                cube.swap_piece(b, flipped_piece, ct=True)
        solve_pieces(b)
            
    
    print(cube.cornerlog, cube.edgelog)
    print(cube.alg_count())
    return cube.alg_count()
 
if __name__ == "__main__":
    with open('scrambles.txt') as f:
        scrams = f.readlines()
        
    algcounts = np.array([])
    for scram in scrams:
        algcounts = np.append(algcounts, solve(scram))
    print(np.average(algcounts))