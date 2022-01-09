#!/usr/bin/env python3

import cube as cb
import vectors as vc
import numpy as np

class Solver(cb.Cube):
    def __init__(self):
        super().__init__()
        self.edge_parity = False
        self.corner_parity = False
    
    def solve_piece(self, buffer):
        pos = self.cube[buffer].pos
        buffer, pos, axis = self.log(buffer, pos)
        self.put_colors(buffer, pos)
        self.swap_pos(buffer, pos)
        self.change_parity(buffer)
        return buffer, pos, axis
     
    def cycle_break(self, buffer, ori=0):
        pos = self.find_unsolved_piece(buffer)
        if not pos:
            pos = self.find_flipped_piece(buffer)
        swap_type = vc.swap_type(buffer, pos)
        o = self.get_o(buffer, pos, True)
        self.color_swap(buffer, pos)
        self.swap_pos(buffer, pos)
        return self.log(buffer, pos, o)
    
    def swap_pos(self, pos1, pos2):
        self.cube[pos1], self.cube[pos2] = self.cube[pos2], self.cube[pos1]
 
    def color_swap(self, buffer, pos):
        swap_type = vc.swap_type(buffer, pos)
        color_swaps = {
            0: lambda: None,
            1: lambda: self.swap_colors(buffer, pos, 0, 2),
            2: lambda: self.roll_ori(buffer, pos, 1),
            3: lambda: self.roll_orI(buffer, pos, -1),
            4: lambda: self.swap_colors(buffer, pos, 1, 2)
        }
        color_swaps[swap_type]()
       
    def get_o(self, buffer, pos, ct=False):
        swap_type = vc.swap_type(buffer, pos)
        if ct:
            return 1
        if swap_type == 3:
            o =  self.cube[buffer].ori[2]
        if swap_type == 4:
            if pos.index(1) == 1:
                o = self.cube[buffer].ori[2]
        else:
            o = self.cube[buffer].ori[1]
        return o
        
    def roll_ori(self, buffer, pos, k):
        self.cube[buffer].ori = np.roll(self.cube[buffer].ori, k)
        self.cube[pos].ori = np.roll(self.cube[pos].ori, -k)
        
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
        a, b = tmp1, tmp2
        self.cube[buffer].ori, self.cube[pos].ori = b, a
                
    def swap_colors(self, pos1, pos2, a, b):
        first = self.cube[pos1].ori
        second = self.cube[pos2].ori
        for x in (first, second):
            x[a], x[b] = x[b], x[a]
        self.cube[pos2].ori, self.cube[pos1].ori = second, first
       
    def find_unsolved_piece(self, buffer):
        buffer_type = vc.piece_type(buffer)
        for piece in self.cube.flatten():
            pos = piece.pos
            if buffer_type == vc.piece_type(pos):
                if not self.is_permuted(pos) \
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
                   
    def rotate_pieces(self, pos1, pos2, k, relparity=True):
        self.cube[pos1].ori = np.roll(self.cube[pos1].ori, k)
        if relparity:
            k = -k
        self.cube[pos2].ori = np.roll(self.cube[pos2].ori, k)
        
        # -1 refers to x, 1 refers to z
        
    def count_solved(self, piecetype=None):
        counter = 0
        for piece in self.cube.flatten():
            if self.is_solved(piece.pos):
                piece_type = vc.piece_type(piece.pos)
                if not piecetype or piece_type == piecetype: 
                        counter += 1
        return counter
    
    def is_permuted(self, pos):
        return True if pos == self.cube[pos].pos else False
        
    def is_solved(self, pos):
        if self.is_permuted(pos) and self.cube[pos].pos.count(1) <= 1 \
        and tuple(self.cube[pos].ori) == (0, 1, 2): 
            return True
        else:
            return False   
        
    def log(self, buffer, pos, axis=None):
        axis = self.cube[buffer].ori[1] if not axis else axis
        return buffer, pos, axis