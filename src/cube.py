import numpy as np

FACES = {
    'L': {
        'axis': 0,
        'pos': 1,
        'preview': lambda x: np.flip(x)
    },
    'R': {
        'axis': 0,
        'pos': -1,
        'preview': lambda x: np.flipud(x)
    },
    'D': {
        'axis': 1,
        'pos': -1,
        'preview': lambda x: np.rot90(x, -1)
    },
    'U': {
        'axis': 1,
        'pos': 1,
        'preview': lambda x: np.fliplr(np.rot90(x))
    },
    'F': {
        'axis': 2,
        'pos': -1,
        'preview': lambda x: np.rot90(np.flipud(x))
    },
    'B': {
        'axis': 2,
        'pos': 1,
        'preview': lambda x: np.rot90(x)
    }
}


class Piece:
    """
    A piece on a Rubik's Cube.
    
    Attributes
    ----------
    solved_pos : tuple
        A 3-tuple representing the x, y, and z components of where
        the piece is located on a solved cube. See the ``Cube`` object's
        documentation for how these axis are defined.
    pos : tuple
        A 3-tuple represeting the x, y, and z components of where
        the piece is located on the cube (meaning, this value changes
        when the piece is moved). See the ``Cube`` object's
        documentation for how these axis are defined.
    ori : array_like
        The x, y, and z parts of the piece's orientation. The three
        values in this array represent to which axis the x/y/z facing
        part of the piece belongs. For example: (1, 2, 0) would mean that
        the part of the piece facing in the x direction belongs to the
        (1) y axis, the part of the piece facing in the y direction belongs
        to the (2) z axis, and the part of the piece facing in the
        z direction belongs to the (0) x axis.
    """
    def __init__(self, x, y, z):
        """ 
        Creates the piece object.
        
        
        """
        self.solved_pos = (x, y, z)
        self.pos = (x, y, z)
        self.ori = np.array([0, 1, 2])
        
    def get_color(self, axis):
        """
        Get the color of the piece object along a given axis.
        
        Specifying an axis allows to precise what the sticker of 
        interest is. The colors are represented not by acutal colors, but
        by what face the sticker belongs to. This allows for 
        orientation-neutrality, with the goal to accommodate all users.

        Parameters
        ----------
        axis : int
            The axis along which to retrieve the color. The x, y, and z
            axis correspond to the numbers 0, 1, and 2, respectively.
            
        Returns
        -------
        color : str or None
            One letter that gives the face to which the sticker belongs,
            or None if retrieving the color of an edge along an axis that
            does not have a color (e.g. x-axis of UF).
        
        Notes
        -----
        Mostly used for debugging at the moment.
        """
        colors = {
            0: {0: 'R', 1: None, 2: 'L'},
            1: {0: 'D', 1: None, 2: 'U'},
            2: {0: 'F', 1: None, 2: 'B'}
            }
        axis_of_color = self.ori[axis]
        solved_position = self.solved_pos[axis_of_color]
        return colors[axis_of_color][solved_position]
    

class Cube:
    def __init__(self):
        self.cube = np.ndarray((3, 3, 3), dtype=Piece)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.cube[x, y, z] = Piece(x, y, z)
                     
    def do_move(self, face, clockwise=True):
        """ 
        Do a 90-degree turn on the cube.

        Parameters
        ----------
        face : str
            One letter corresponding to the face that would like to be
               turned. Either U, F, R, B, L, D
        clockwise : bool, optional
            The direction in which the turn will be performed. The default,
            True, will do the turn in the clockwise direction. Using False
            will do the turn in the counter-clockwise direction. To do a
            180-degree turn, simply use this function two times, with any
            `clockwise` value (X2 is the same as X2').
            
        Returns
        -------
        None 
        
        Notes
        -----
        This function is only used for parsing and applying human scrambles
        to the cube. The actual solving is done by swapping pieces, not by 
        doing moves.
        """
        k = 1 if clockwise == True else -1
        # Because of the way numpy handles arrays and the way the cube
        # is in real life, these faces have to be rotated in the
        # opposite direction
        k = -k if face in {'D', 'L', 'B'} else k
        
        index = self.get_index(face)
        self.cube[index] = np.rot90(self.cube[index], k)
        # After swapping positions, it is also important to swap the
        # two colors of each piece that is being turned on the two axis
        # that are not being turned. 
        # For example, when doing a U move, UFR moves to UFL. The 'F' sticker
        # in UFR moves to the 'L' sticker of UFL, and the 'R' sticker in
        # UFR moves to the 'F' sticker of UFL. This also applies to edges.
        axis1, axis2 = {0, 1, 2} - {FACES[face]['axis']}
        for piece in self.cube[index].flatten():
            piece.ori[axis1], piece.ori[axis2] \
            = piece.ori[axis2], piece.ori[axis1] 
    
    def get_index(self, face):
        """
        Given a face, return an index to that face.
        
        This index allows access to all the pieces on the face of 
        the cube, allowing for turns to be applied to specific faces.
        
        Parameters
        ----------
        face : str
            One letter corresponding to a face on a cube. Either
            U, F, R, B, L, or D.
        
        Returns
        -------
        index : tuple
            An index that can be applied to the cube attribute to access 
            all the pieces on the given face.
        """
        index = [slice(None), slice(None), slice(None)]
        index[FACES[face]['axis']] = FACES[face]['pos'] + 1
        return tuple(index)

    def print_cube(self):
        """ 
        Prints the current state of the cube to stdout.
        
        Used for debugging purposes. The faces printed, in order are:
        U, F, L, R, B, D.
        
        Returns
        -------
        None 
        """
        for face in ['U', 'F', 'L', 'R', 'B', 'D']:
            axis = FACES[face]['axis']
            index = self.get_index(face)
            namepieces = np.vectorize(lambda x: x.get_color(axis))
            preview = FACES[face]['preview'](self.cube[index])
            print(namepieces(preview), '\n')