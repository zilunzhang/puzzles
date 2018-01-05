from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str=
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"
        # new property
        # record the extension history
        self._path = [self._from_word]

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool
        >>> puzzle_1 = WordLadderPuzzle('abs', 'cat', {'cat', 'abs', 'dog'})
        >>> puzzle_2 = WordLadderPuzzle('abs', 'cat', {'dog', 'cat', 'abs'})
        >>> puzzle_1 == puzzle_2
        True
        >>> puzzle_3 = WordLadderPuzzle('abs', 'cat', {'laugh', 'happy'})
        >>> puzzle_3 == puzzle_1
        False
        >>> puzzle_4 = WordLadderPuzzle('dog', 'cat', {'cat', 'abs', 'dog'})
        >>> puzzle_4 == puzzle_1
        False
        """
        return type(self) == type(other) and \
            self._from_word == other._from_word and \
            self._to_word == other._to_word and \
            self._word_set == other._word_set

    def __str__(self):
        """
        Return a human-readable string representing WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str
        >>> puzzle_1 = WordLadderPuzzle('abs', 'cat', {'cat', 'abs', 'dog'})
        >>> print(puzzle_1)
        Solving word ladder from abs->cat
        >>> puzzle_2 = WordLadderPuzzle('dog', 'one', {'cat', 'one', 'dog'})
        >>> print(puzzle_2)
        Solving word ladder from dog->one
        """
        return "Solving word ladder from {}->{}".format(self._from_word,
                                                        self._to_word)

    def __repr__(self):
        """
        Return representation of WordLadderPuzzle (self) as string that
        can be evaluated into an equivalent WordLadderPuzzle.

        @type self: WordLadderPuzzle
        @rtype: str
        >>> puzzle_1 = WordLadderPuzzle('abs', 'cat', {'cat', 'abs', 'dog'})
        >>> puzzle_1
        abs -> cat
        >>> puzzle_2 = WordLadderPuzzle('dog', 'one', {'cat', 'one', 'dog'})
        >>> puzzle_2
        dog -> one
        """
        return "{} -> {}".format(self._from_word, self._to_word)

    def extensions(self):
        """
        Return list of legal extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        >>> puzzle_1 = WordLadderPuzzle('ok', 'ko', {'oo', 'kk', 'ok', 'ko'})
        >>> result = puzzle_1.extensions()
        >>> print(result[0])
        Solving word ladder from kk->ko
        >>> print(result[1])
        Solving word ladder from oo->ko
        >>> ws = {'live', 'lave', 'noon', 'move', 'lope', 'bomb', 'love'}
        >>> puzzle_2 = WordLadderPuzzle('love', 'bomb', ws)
        >>> result_2 = puzzle_2.extensions()
        >>> print(result_2[0])
        Solving word ladder from move->bomb
        >>> print(result_2[1])
        Solving word ladder from lave->bomb
        >>> print(result_2[2])
        Solving word ladder from live->bomb
        >>> print(result_2[3])
        Solving word ladder from lope->bomb
        """
        result = []
        for i in range(len(self._from_word)):
            for j in range(len(self._chars)):
                # check if character of self._from_word at current index equals
                # to character of self._chars at current index
                if self._from_word[i] != self._chars[j]:
                    # change current character of self._from_word to current
                    # character of self._chars
                    new_word = self._from_word[:i] + self._chars[j] + \
                               self._from_word[i+1:]
                    if new_word in self._word_set and \
                            new_word not in self._path:
                        new_puzzle = WordLadderPuzzle(new_word, self._to_word,
                                                      self._word_set)
                        result.append(new_puzzle)
                        new_puzzle._path = self._path + [new_word]
        return result

    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool
        >>> ws = {'live', 'lave', 'noon', 'move', 'lope', 'bomb', 'love'}
        >>> puzzle_1 = WordLadderPuzzle('bomb', 'bomb', ws)
        >>> puzzle_1.is_solved()
        True
        >>> puzzle_2 = WordLadderPuzzle('lope', 'bomb', ws)
        >>> puzzle_2.is_solved()
        False
        """
        return self._from_word == self._to_word

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
