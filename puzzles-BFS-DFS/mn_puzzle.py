from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle
        @rtype: bool
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle1 = MNPuzzle(start_grid, target_grid)
        >>> puzzle2 = MNPuzzle(start_grid, target_grid)
        >>> puzzle1 == puzzle2
        True
        >>> puzzle3 = MNPuzzle(target_grid, start_grid)
        >>> puzzle1 == puzzle3
        False
        """
        return all([type(self) == type(other),
                    self.from_grid == other.from_grid,
                    self.to_grid == other.to_grid])

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle = MNPuzzle(start_grid, target_grid)
        >>> print(puzzle)
        * 2 3
        1 4 5
        <BLANKLINE>
        >>> from_grid = (("1", "2", "3"), ("*", "5", "6"))
        >>> to_grid = (("1", "2", "3"), ("5", "6", "*"))
        >>> puzzle_1 = MNPuzzle(from_grid, to_grid)
        >>> print(puzzle_1)
        1 2 3
        * 5 6
        <BLANKLINE>
        """
        grid = self.from_grid
        result = ""
        for i in range(len(grid)):
            result += " ".join(grid[i]) + "\n"
        return result

    def __repr__(self):
        """
        Return representation of nxm puzzle (self) as string that
        can be evaluated into an equivalent n x m puzzle.

        @type self: MNPuzzle
        @rtype: string
        >>> grid1 = (('A', 'C', 'B', 'D'), ('F', 'E', 'G', 'H'),
        ... ('M', 'N', 'O', '*'))
        >>> grid2 = (('A', 'B', 'C', 'D'), ('E', 'F', 'G', 'H'),
        ... ('M', 'N', 'O', '*'))
        >>> MNP = MNPuzzle(grid1, grid2 )
        >>> MNP.__repr__()
        'This is a 3 X 4 NMPuzzle'
        """

        row_length = self.m
        col_length = self.n

        return "This is a {} X {} NMPuzzle".format(col_length, row_length)

    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> start_grid = (("1", "2", "3", "*"), ("4", "5", "6", "7"))
        >>> target_grid = (("1", "2", "3", "4"), ("5", "6", "7", "*"))
        >>> puzzle = MNPuzzle(start_grid, target_grid)
        >>> L = puzzle.extensions()
        >>> len(L)
        2
        >>> print(L[0])
        1 2 * 3
        4 5 6 7
        <BLANKLINE>
        >>> print(L[1])
        1 2 3 7
        4 5 6 *
        <BLANKLINE>
        """
        def transform(grid_):
            """
            Transpose between tuple-grid and list-grid.

            @type grid_: tuple(tuple(str)) | list[list[str]]
            @rtype: list[list[str]] | tuple(tuple(str))
            """
            # tuple-grid -> list-grid
            if isinstance(grid_, tuple):
                return [list(row) for row in grid_]
            # list-grid -> tuple-grid
            if isinstance(grid_, list):
                return tuple(tuple(row) for row in grid_)

        grid = transform(self.from_grid)
        extension = []
        # <l>: length of col
        l = len(grid)
        # <w>: length of row
        w = len(grid[0])
        # get the Y-coordinate for the point
        for y in range(l):
            # get the X-coordinate for the point
            for x in range(w):
                # we only consider the area around "*"
                if grid[y][x] == "*":
                    # (*)(a) -> (a)(*)
                    if x + 1 < w:
                        new_grid = [list(row) for row in grid]
                        new_grid[y][x] = new_grid[y][x + 1]
                        new_grid[y][x + 1] = "*"
                        extension.append(MNPuzzle(transform(new_grid),
                                                  self.to_grid))
                    # (a)(*) -> (*)(a)
                    if x - 1 >= 0:
                        new_grid = [list(row) for row in grid]
                        new_grid[y][x] = new_grid[y][x - 1]
                        new_grid[y][x - 1] = "*"
                        extension.append(MNPuzzle(transform(new_grid),
                                                  self.to_grid))
                    # (*) -> (a)
                    # (a) -> (*)
                    if y + 1 < l:
                        new_grid = [list(row) for row in grid]
                        new_grid[y][x] = new_grid[y + 1][x]
                        new_grid[y + 1][x] = "*"
                        extension.append(MNPuzzle(transform(new_grid),
                                                  self.to_grid))
                    # (a) -> (*)
                    # (*) -> (a)
                    if y - 1 >= 0:
                        new_grid = [list(row) for row in grid]
                        new_grid[y][x] = new_grid[y - 1][x]
                        new_grid[y - 1][x] = "*"
                        extension.append(MNPuzzle(transform(new_grid),
                                                  self.to_grid))
        return extension

    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool
        >>> start_grid = (("1", "2", "3", "4"), ("5", "6", "7", "*"))
        >>> target_grid = (("1", "2", "3", "4"), ("5", "6", "7", "*"))
        >>> puzzle_1 = MNPuzzle(start_grid, target_grid)
        >>> puzzle_1.is_solved()
        True
        >>> start_grid_1 = (("1", "2", "3", "*"), ("4", "5", "6", "7"))
        >>> puzzle_2 = MNPuzzle(start_grid_1, target_grid)
        >>> puzzle_2.is_solved()
        False
        """
        return self.from_grid == self.to_grid

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
