import cube.vectors as vc

class SearchCube:
    def find_unpermuted_piece(self, buffer):
        """ 
        Finds an unpermuted piece on the cube that is not the buffer.
        
        An unpermuted piece is one that is in the wrong position.
        Note that a flipped edge (one that is in the right position,
        but not in the correct orientation) is considered 'permuted'.
        
        Parameters
        ----------
        buffer : tuple
            3-tuple representing the position of the buffer on the
            cube.
            
        Returns
        -------
        position : tuple
            A 3-tuple representing the position of the unpermuted
            piece.
        """
        buffer_type = vc.piece_type(buffer)
        for piece in self.cube.flatten():
            pos = piece.pos
            if buffer_type == vc.piece_type(pos):
                if not self.is_permuted(pos) \
                    and piece.pos != self.cube[buffer].pos:
                    return piece.pos
                
    def find_flipped_piece(self, buffer):
        """
        Finds a flipped piece on the cube that is not the buffer.
        
        A flipped piece is one that is in the correct position, but
        wrongly oriented.
        
        Parameters
        ----------
        buffer : tuple
            3-tuple representing the position of the buffer on the cube.
        
        Returns
        -------
        position : tuple
            3-tuple representing the position of the flipped piece.
        
        Notes
        -----
        The word 'flipped' piece refers to both flipped edges and twisted
        corners. Naming the function accordingly would be redundant.
        """
        buffer_type = vc.piece_type(buffer)
        for piece in self.cube.flatten():
            pos = piece.pos
            if buffer_type == vc.piece_type(pos):
                if not self.is_solved(pos) \
                   and self.is_permuted(pos) \
                   and pos != self.cube[buffer].pos:
                       return piece.pos   
                   
    def count_solved(self, piecetype=None):
        """
        Counts the number of pieces that are solved.
        
        Parameters
        ----------
        piecetype : string or None
            Either 'corner', 'edge', or None. This specifies the 
            to count only those type of pieces.
        
        Returns
        -------
        count : int
            The amount of solved pieces.
        """
        counter = 0
        for piece in self.cube.flatten():
            if self.is_solved(piece.pos):
                this_pieces_type = vc.piece_type(piece.pos)
                if not piecetype or this_pieces_type == piecetype: 
                        counter += 1
        return counter
    
    def is_permuted(self, pos):
        """
        Determines if a piece is permuted.
        
        Permuted means that the piece is in the correct position,
        regardless if the piece's orientation is correct.
        
        Parameters
        ----------
        pos : tuple
            3-tuple representing the position of the piece.
        
        Returns
        -------
        bool
            True if the piece is permuted, False if not.
        """
        return True if pos == self.cube[pos].pos else False
        
    def is_solved(self, pos):
        """ 
        Determines if a piece is solved.
        
        Parameters
        ----------
        pos : tuple
            3-tuple representing the position of the piece.
            
        Returns
        -------
        bool
            True if the piece is solved, False if notParameters
        ----------
        pos : tuple
            3-tuple representing the position of the piece.
            
        Returns
        -------
        bool
            True if the piece is solved, False if not.
        """
        # 'pos.count(1) <= 1' makes sure that center pieces and the core
        # piece is never considered, because they are always solved.
        if self.cube[pos].pos.count(1) <= 1 \
            and self.is_permuted(pos) \
            and tuple(self.cube[pos].ori) == (0, 1, 2):
                return True
        else:
            return False   
        
    def find_piece(self, pos):
        """ 
        Finds a specific piece on the cube.
        
        Parameters
        ----------
        pos : tuple
            3-tuple representing the position of the piece
            on a solved cube.
        
        Returns
        -------
        position : tuple
            3-tuple representing the position of the piece
            on the current cube.
        axis : int
            The axis on which the piece has it's U/D face sticker
            (or in E-slice edge's cases, the None sticker.)
        """
        for piece in self.cube.flatten():
            # self.cube[piece.pos].pos indicates where the given
            # piece needs to go. For example, if we are looking
            # for the UR piece, and we index the cube with the DR piece's 
            # coordinates and see UR, it means UR is in DR.
            if self.cube[piece.pos].pos == pos:
                return piece.pos, \
                       tuple(self.cube[piece.pos].ori).index(1)
 