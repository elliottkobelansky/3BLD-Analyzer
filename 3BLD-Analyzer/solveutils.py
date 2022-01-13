from cube.swap import CubePrimitives
from cube.search import SearchCube
import cube.vectors as vc
import numpy as np

class Solver(CubePrimitives, SearchCube):
    def solve_piece(self, buffer):
        pos = self.cube[buffer].pos
        buffer, pos, axis = self.log(buffer, pos)
        self.solve_ori(buffer, pos)
        self.swap_pos(buffer, pos)
        self.change_parity(buffer)
        return buffer, pos, axis
     
    def cycle_break(self, buffer, ori=0):
        pos = self.find_unpermuted_piece(buffer)
        if not pos:
            raise Exception("No piece to break to.")
        o = self.get_o(buffer, pos, True)
        self.swap_ori(buffer, pos)
        self.swap_pos(buffer, pos)
        self.change_parity(buffer)
        return self.log(buffer, pos, o)
    
    def flip_or_twist(self, buffer):
        piece_type = vc.piece_type(buffer)
        flipped_piece = self.find_flipped_piece(buffer)
        flipped_ori = tuple(self.cube[flipped_piece].ori)
        if piece_type == 'edge':
            self.flip_edges(buffer, flipped_piece)
        if piece_type == 'corner':
            xtoy = True if flipped_ori.index(1) == 0 else False
            self.twist_corners(buffer, flipped_piece, xtoy)
        return self.log(buffer, flipped_piece, 1)
    
    def log(self, buffer, pos, axis=None, ct=None):
        axis = self.cube[buffer].ori[1] if not axis else axis
        return buffer, pos, axis
    
    def pseudoswap(self, pos1, pos2):
        pos1, axis1 = self.find_piece(pos1)
        pos2, axis2 = self.find_piece(pos2)
        ori_swap_type = vc.edge_ori_swap_type(pos1, pos2, axis1, axis2)
        self.swap_ori(pos1, pos2)
        self.swap_pos(pos1, pos2)
        if ori_swap_type:
            self.flip_edges(pos1, pos2)

    def flip_edges(self, pos1, pos2):
        p1, a1 = self.cube[pos1].ori, pos1.index(1)
        p2, a2 = self.cube[pos2].ori, pos2.index(1)
        for p, a in zip((p1, p2), (a1, a2)):
            axis1, axis2 = {0, 1, 2} - {a}
            p[axis1], p[axis2] = p[axis2], p[axis1]     
        self.cube[pos1].ori, self.cube[pos2].ori = p1, p2
        
    def twist_corners(self, pos1, pos2, xtoy=True):
        k1, k2 = (-1, 1) if xtoy == True else (1, -1)
        ori1 = self.cube[pos1].ori
        ori2 = self.cube[pos2].ori
        k1 = -k1 if vc.swap_type(pos1, pos2) == 1 else k1
        ori1[:] = np.roll(ori1, k1)
        ori2[:] = np.roll(ori2, k2)
        self.cube[pos1].ori, self.cube[pos2].ori = ori1, ori2