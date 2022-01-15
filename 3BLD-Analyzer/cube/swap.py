from cube.skeleton import CubeSkeleton
import cube.vectors as vc
import numpy as np


class CubePrimitives(CubeSkeleton):
    def __init__(self):
        super().__init__()
        self.edge_parity = False
        self.corner_parity = False

    def change_parity(self, pos):
        """
        Change a piece type's parity.

        Since the buffer is passed in, the piece type is determined
        automatically.

        Parameters
        ----------
        pos : tuple
            3-tuple containing the coordinates of the piece of which you
            want to change it's piece type's parity.

        Returns
        -------
        int
            Zero on success.
        """
        piecetype = vc.piece_type(pos)
        if piecetype == "corner":
            self.corner_parity = not self.corner_parity
            return 0
        elif piecetype == "edge":
            self.edge_parity = not self.edge_parity
            return 0
        raise Exception("Failed to change the parity of the buffer.")

    def swap_pos(self, pos1, pos2):
        """
        Swaps the positions of 2 pieces.

        Parameters
        ----------
        pos1 : tuple
            3-tuple representing the position of the first piece.
        pos2 : tuple
            3-tuple representing the position of the second piece.

        Returns
        -------
        int
            Zero on success.
        """
        self.cube[pos1].pos, self.cube[pos2].pos = (
            self.cube[pos2].pos,
            self.cube[pos1].pos,
        )
        return 0

    def solve_ori(self, pos1, pos2):
        """
        Solves a pieces orientation into place.

        The first position is the piece that gets its colors solved
        into the second pieces orientation.

        Parameters
        ----------
        pos1 :
            3-tuple representing the position of the first piece.
        pos2 :
            3-tuple representing the position of the second piece.
            This is the piece that gets its colors solved.

        Returns:
        -------
        int
            Zero on success.
        """
        a, b = self.cube[pos1].ori, self.cube[pos2].ori
        tmp1, tmp2 = [0, 0, 0], [0, 0, 0]
        # On each axis:
        for i in range(3):
            # Look at where that axis needs to go and swap it into
            # the correct axis on the second ori.
            tmp1[i], tmp2[a[i]] = b[a[i]], a[i]
        a, b = tmp1, tmp2
        self.cube[pos1].ori, self.cube[pos2].ori = a, b
        return 0

    def swap_ori(self, pos1, pos2):
        """
        Swaps the orientations of 2 pieces.

        Takes into account the relative positions of the pieces.

        Parameters
        ----------
        pos1 : tuple
            3-tuple representing the position of the first piece.
        pos2 : tuple
            3-tuple representing the position of the second piece.

        Returns
        -------
        int
            Zero on success.
        """
        swap_type = vc.swap_type(pos1, pos2)
        color_swaps = {
            # Since '0' swap types share all their color's axis,
            # the colors positions in each orientation will not change.
            0: lambda: None,
            # '1' swap types are 2 pieces that are swappable with a
            # U or D move. When this move is pseudo-applied (only those
            # 2 pieces are changing), the colors facing in the x and z
            # direction will swap.
            1: lambda: self.swap_ori_axis(pos1, pos2, 0, 2),
            # '2' swap types are from an M slice edge to an E slice edge.
            # rotating one piece's orientation one way and the other
            # piece's orientation in the opposite way does the trick.
            2: lambda: self.roll_ori(pos1, pos2, -1),
            # This is the opposite of 2 since '3' are from E to M.
            3: lambda: self.roll_ori(pos1, pos2, 1),
            # '3' swap types are from S slice to E slice. They are
            # swappable with a R or L move. When this move is
            # pseudo-applid, the colors facing in the y and z direction
            # will swap.
            4: lambda: self.swap_ori_axis(pos1, pos2, 1, 2),
        }
        # Swap the pieces orientations (the rotation/color changing
        # stil has to be applied)
        self.cube[pos1].ori, self.cube[pos2].ori = (
            self.cube[pos2].ori,
            self.cube[pos1].ori,
        )
        # Apply the axis changing stuff
        color_swaps[swap_type]()
        return 0

    def roll_ori(self, pos1, pos2, k):
        """
        Roll the orientation of 2 pieces in opposite directions.

        Parameters
        ----------
        pos1 : tuple
            3-tuple representing the position of the first piece.
        pos2 : tuple
            3-tuple representing the position of the second piece.
        k : int
            1 or -1. Direction in which to roll the array.

        Returns
        -------
        int
            Zero on success.
        """
        self.cube[pos1].ori = np.roll(self.cube[pos1].ori, k)
        self.cube[pos2].ori = np.roll(self.cube[pos2].ori, -k)
        return 0

    def swap_ori_axis(self, pos1, pos2, axis1, axis2):
        """
        Swap the stickers of each of 2 pieces on 2 axis.

        Parameters
        ----------
        pos1 : tuple
            3-tuple representing the position of the first piece.
        pos2 : tuple
            3-tuple representing the position of the second piece.
        axis1 : int
            The first axis on which to swap the stickers. (0, 1, or 2)
        axis2 : int
            The second axis on which to swap the stickers. (0, 1, or 2)

        Returns
        -------
        int
            Zero on success.
        """
        first = self.cube[pos1].ori
        second = self.cube[pos2].ori
        for x in (first, second):
            x[axis1], x[axis2] = x[axis2], x[axis1]
        self.cube[pos1].ori, self.cube[pos2].ori = first, second
        return 0

    def get_o(self, buffer, pos, ct=False):
        swap_type = vc.swap_type(buffer, pos)
        if ct:
            return 1
        if swap_type == 3:
            o = self.cube[buffer].ori[2]
        if swap_type == 4:
            if pos.index(1) == 1:
                o = self.cube[buffer].ori[2]
        else:
            o = self.cube[buffer].ori[1]
        return o
