import cube.vectors as vc

class SearchCube:
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
        
    def find_edge(self, pos):
        for piece in self.cube.flatten():
            if self.cube[piece.pos].pos == pos:
                return piece.pos, \
                       tuple(self.cube[piece.pos].ori).index(1)
 