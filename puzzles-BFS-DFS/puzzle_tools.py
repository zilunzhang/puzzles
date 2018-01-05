"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    def dfs(puzzle_1, seen):
        if puzzle_1.fail_fast():
            return None
        elif puzzle_1.is_solved():
            return PuzzleNode(puzzle_1)
        else:
            cur_node = PuzzleNode(puzzle_1)
            for extension in puzzle_1.extensions():
                    # check if current extension has been used
                    if str(extension) not in seen:
                        seen.add(str(extension))
                        child = dfs(extension, seen)
                        # check whether child is None
                        # if it doesn't find the solution, child would always
                        # be None
                        if child:
                            # we found solution, build reference between child
                            # and parent until the first node
                            child.parent = cur_node
                            cur_node.children.append(child)
                            # we call return here, so the for loop in every
                            # recursion step would stop, hence each node only
                            # has one child (we only append it once)
                            return cur_node
    seen_ = set()
    seen_.add(str(puzzle))
    return dfs(puzzle, seen_)


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    # helper function
    def get_path(node):
        """
        Get the root_node with the path to the target node.

        @type node: PuzzleNode
        @rtype: PuzzleNode
        """
        current_node_ = node
        while current_node_.puzzle is not None and \
                current_node_.parent is not None:
            current_node_.parent.children = [current_node_]
            current_node_ = current_node_.parent
        return current_node_

    root_node = PuzzleNode(puzzle)
    pending_que = [root_node]
    seen = set()
    while pending_que:
        current_node = pending_que.pop(0)
        if current_node.puzzle.is_solved():
            return get_path(current_node)

        elif str(current_node.puzzle) not in seen:
            if not current_node.puzzle.fail_fast():
                seen.add(str(current_node.puzzle))
                for ext in current_node.puzzle.extensions():
                    if str(ext) not in seen:
                        child_node = PuzzleNode(ext, parent=current_node)
                        pending_que.append(child_node)


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
