from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = [["#", "*", "*", "*", "#"], ["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = [["#", "*", "*", "*", "#"], ["*", "*", "*", "*", "*"]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp1.__eq__(gpsp2)
        True
        >>> grid3 = [["#", "*", "*", "*", "#"], ["*", "*", ".", "*", "*"]]
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> gpsp1.__eq__(gpsp3)
        False
        """
        return type(self) == type(other) and \
            self._marker == other._marker and \
            self._marker_set == other._marker_set

    def __repr__(self):
        """
        Return representation of GridPegSolitairePuzzle (self) as string that
        can be evaluated into an equivalent GridPegSolitairePuzzle.
        @type self: GridPegSolitairePuzzle
        @rtype: string

        >>> grid1 = [["#", "*", "*", "*", "#"], ["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> gpsp1.__repr__()
        'This is a 2 X 5 peg solitaire'
        >>> grid2 = [["*", "*", "*", "*", "*"], ["*", "*", ".", "*", "*"],
        ... ["*", "*", "*", "*", "*"]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.__repr__()
        'This is a 3 X 5 peg solitaire'
        """

        row_length = len(self._marker)
        col_length = len(self._marker[0])

        return "This is a {} X {} peg solitaire".format(row_length, col_length)

    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitairePuzzle
        self.

        @type self: GridPegSolitairePuzzle
        @rtype: string
        >>> grid1 = [["#", "*", "*", "*", "#"], ["*", "*", "*", "*", "*"]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> print(gpsp1)
        # * * * #
        * * * * *
        <BLANKLINE>
        >>> grid2 = [["#", "*", ".", "*", "#"], ["*", "*", ".", "*", "*"]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> print(gpsp2)
        # * . * #
        * * . * *
        <BLANKLINE>
        """
        result = ""
        for i in range(len(self._marker)):
            result += " ".join(self._marker[i]) + "\n"
        return result

    def is_solved(self):
        """
        Return True iff there is only one '*' in the configuration.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = [["#", ".", ".", "*", "#"], [".", ".", ".", ".", "."]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> gpsp1.is_solved()
        True
        >>> grid2 = [["#", ".", ".", "*", "#"], [".", "*", ".", ".", "."]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.is_solved()
        False
        """
        count = 0
        for row in self._marker:
            for element in row:
                if element == "*":
                    count += 1
        if count == 1:
            return True

        return False

    def extensions(self):
        """
        Return legal extensions of GridPegSolitairePuzzle consist of
        all configurations.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid1 = [["#", ".", ".", "*", "#"], [".", ".", ".", "*", "."],
        ... [".", ".", ".", ".", "."]]
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> L2 = gpsp1.extensions()
        >>> print(L2[0])
        # . . . #
        . . . . .
        . . . * .
        <BLANKLINE>
        >>> grid2 = [["#", ".", ".", "*", "#"], [".", ".", ".", ".", "."],
        ... [".", ".", ".", ".", "."]]
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp2.extensions()
        []
        """
        extension = []
        grid_ = self._marker
        # <l>: length of col
        l = len(grid_)
        # <w>: length of row
        w = len(grid_[0])
        # get the Y-coordinate for the point
        for y in range(l):
            # get the X-coordinate for the point
            for x in range(w):
                # we only consider the area around "."
                if grid_[y][x] == ".":
                    # (. * *) -> (* . .)
                    if x + 2 < w:
                        if grid_[y][x + 1] == "*" and grid_[y][x + 2] == "*":
                            new_grid = [list(row) for row in grid_]
                            new_grid[y][x], new_grid[y][x + 1],\
                                new_grid[y][x + 2] = "*", ".", "."
                            extension.append(GridPegSolitairePuzzle(
                                new_grid, self._marker_set))
                    # (* * .) -> (. . *)
                    if x - 2 >= 0:
                        if grid_[y][x - 1] == "*" and grid_[y][x - 2] == "*":
                            new_grid = [list(row) for row in grid_]
                            new_grid[y][x - 2], new_grid[y][x - 1],\
                                new_grid[y][x] = ".", ".", "*"
                            extension.append(GridPegSolitairePuzzle(
                                new_grid, self._marker_set))
                    # (.)    (*)
                    # (*) -> (.)
                    # (*)    (.)
                    if y + 2 < l:
                        if grid_[y + 1][x] == "*" and grid_[y + 2][x] == "*":
                            new_grid = [list(row) for row in grid_]
                            new_grid[y][x], new_grid[y + 1][x],\
                                new_grid[y + 2][x] = "*", ".", "."
                            extension.append(GridPegSolitairePuzzle(
                                new_grid, self._marker_set))
                    # (*)    (.)
                    # (*) -> (.)
                    # (.)    (*)
                    if y - 2 >= 0:
                        if grid_[y - 1][x] == "*" and grid_[y - 2][x] == "*":
                            new_grid = [list(row) for row in grid_]
                            new_grid[y - 2][x], new_grid[y - 1][x],\
                                new_grid[y][x] = ".", ".", "*"
                            extension.append(GridPegSolitairePuzzle(
                                new_grid, self._marker_set))
        return extension

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
