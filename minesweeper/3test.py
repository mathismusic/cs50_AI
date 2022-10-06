import random
import copy

class Sentence():
    # A Logical statement about a Minesweeper game.

    """A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    # a_sentence = Sentence(set of some cells, count of #mines in those cells)
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    # check equality of two sentences
    def __eq__(self, other):

        # checking eq of count is redundant though
        return self.cells == other.cells and self.count == other.count

    # sentence written as a string as 'set(cells) = count'
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # return cells and set sentence to 'set() = 0' for easier cleaning of self.knowledge
        if len(self.cells) == self.count:
            mines_found = copy.copy(self.cells) # and not mines_found = self.cells, then in next step mines_found becomes set()
            self.cells = set()
            self.count = 0
            return mines_found
        else:
            return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            safes_found = copy.copy(self.cells)
            self.cells = set()
            return safes_found
        else:
            return set()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if cell not in it, then do nothing. Also, count >= 1 is ensured if cell is in it as it's a mine
        if cell in self.cells:

            # pop() removes arbitrary element and takes no arg, remove removes particular element
            self.cells.remove(cell)

            self.count -= 1  # count \geq 1 as it's given that cell is a mine.
            # notice the new sentence formed is shorter and different

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:  # else nothing to do
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # (List of sentences) about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates self.knowledge and self.mines
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates self.knowledge and self.safes
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # called in runner.py, line 214. given the cell and #mines in neighbors
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        (safe cell <- cell), (how many neighboring cells <- count) have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # self is placeholder for the minesweeperAI-class object, whenever a fn in the class calls another fn in the class

        # marks cell as move+safe cell and updates self.knowlege that cell is safe
        self.moves_made.add(cell)
        self.mark_safe(cell)  # all sentences in self.knowledge mark cell as safe ie delete cell, also cell added to self.safes as well

        '''neighbor_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue  # move to next pair(i,j)

                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cells.add(cell)
            '''
        neighbor_cells = {cell + 1, cell - 1, cell - 3}
        self.knowledge.append(Sentence(neighbor_cells, count))

        # get all possible new sentences
        ''' This is incorrect:
        Why? at the end of the loop knowledge is getting appended, which increases its size.
        Now, say A = B + C, A, B, C sets. Let x.cells = A, y.cells = B, knowledge = [x, y]
        Then first: s1 = x, s2 = x (1st elem of list). moves to next iteration
        s1 = x, s2 = y. moves into the if condition and knowledge = [A, B, C] now. ([x, y, z] actually). Size of knowledge has increased.
        now s1 = x, s2 = z. moves into if and knowledge = [A, B, C, B]
        keeps repeating as [A, B, C, B, C, B, ...].

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                print(str(sentence1))
                if (not sentence1.cells == sentence2.cells
                    and sentence1.cells.issubset(sentence2.cells)):
                    cells = sentence2.cells - sentence1.cells
                    # don't use var = count here as count is already a var
                    new_count = sentence2.count - sentence1.count
                    self.knowledge.append(Sentence(cells, new_count))

                The key idea here is to make a copy of knowledge and then iterate for s1, s2 in the copy.
                In the if we append original knowledge, as is required.
                    '''
        '''knowledge2 = self.knowledge.copy()
        for sentence1 in knowledge2:
            for sentence2 in knowledge2:
                if (not sentence1.cells == sentence2.cells
                    and sentence1.cells.issubset(sentence2.cells)):
                    cells = sentence2.cells - sentence1.cells
                    # don't use var = count here as count is already a var
                    new_count = sentence2.count - sentence1.count
                    self.knowledge.append(Sentence(cells, new_count))
        '''
        # The above is implemented in the while loop to keep getting new sentences when possible
        # add in info about new mines/safes

        while True:
            print("Hi")
            knowledge = copy.deepcopy(self.knowledge)  # some sentences got modified with shallow copy
            for i in range(len(knowledge)):
                print(f"knowledge2[{i}] = {knowledge[i]}")

            # get new sentences
            for sentence1 in knowledge:
                for sentence2 in knowledge:
                    if (not sentence1.cells == sentence2.cells
                            and sentence1.cells.issubset(sentence2.cells) and sentence1.cells != set()):
                        new_cells = sentence2.cells - sentence1.cells
                        # don't use var = count here as count is already a var
                        new_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(new_cells, new_count)
                        self.knowledge.append(new_sentence)
                        self.knowledge.remove(sentence2)

            for i in range(len(self.knowledge)):
                print(f"knowledge[{i}] = {self.knowledge[i]}")
            print("now to collect info: ")

            # add info
            for sentence in self.knowledge:

                # collect obvious information ie known_mines and known_safes
                for mine in sentence.known_mines():

                    # add to mines, update self.knowledge's sentences as well
                    self.mines.add(mine)  # NOT self.mark_mine, we don't want to sum over all sentences.
                    sentence.mark_mine(mine)

                for safe in sentence.known_safes():
                    self.safes.add(safe)
                    sentence.mark_safe(safe)


                # we are mutating the sentences here, so self.knowledge is required in the first loop and not a copy. the size of self.knowledge is same though
                if not sentence.cells == set():  # just for speed
                    # for cell in self.moves_made:  (Not required as moves_made is a subset of safes)
                    #    sentence.mark_safe(cell)
                    for cell in self.safes:
                        sentence.mark_safe(cell)
                    for cell in self.mines:
                        sentence.mark_mine(cell)

            null_sentence = Sentence(set(), 0)
            while null_sentence in self.knowledge:
                self.knowledge.remove(null_sentence)

            for i in range(len(knowledge)):
                print(f"knowledgecopy[{i}] = {knowledge[i]}")
            for i in range(len(ai.knowledge)):
                print(f"knowledge[{i}] = {ai.knowledge[i]}")

            if len(knowledge) == len(self.knowledge):
                if len(knowledge) == 0:
                    return  # this needs to be taken care as it won't go into for loop if len = 0 as nothing to iterate over
                for i in range(len(knowledge)):
                    if knowledge[i].cells != self.knowledge[i].cells:
                        break
                    # so now they are equal objects ie nothing happened from start of the while loop ie no new knowledge
                    # null_sentences could still be there, so cleanup, then finish
                    null_sentence = Sentence(set(), 0)
                    while null_sentence in self.knowledge:
                        self.knowledge.remove(null_sentence)
                    return


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if self.safes == set():
            return None  # default return val for a fn, also see runner.py line181
        '''for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines and (i, j) in self.safes:
                    return (i, j)
        '''
        for i in range(8):
            if i not in self.moves_made and i not in self.mines and i in self.safes:
                return i
        # no further action req here, like add (i, j) to self.move_made etc. see runner.py line214 and minesweeper.py add_knowledge, they take care of doing this


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # note that this fn is only called when self.safes is a subset of self.moves_made, so it chooses a 'new' cell
        sample_space = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    sample_space.append((i, j))

        return random.choice(sample_space)


        raise NotImplementedError



sentence = Sentence({1, 4, 5}, 2)

ai = MinesweeperAI(8, 8)
ai.knowledge.append(sentence)
ai.add_knowledge(4, 2)  # so safes = 4, mines = {}, mm = 4, added sentence = {1, 3, 5} = 2, new sentence formed = {3} = 0
for i in range(len(ai.knowledge)):
    print(f"knowledge[{i}] = {ai.knowledge[i]}")
print(f"safe = {ai.safes}")
print(f"mines = {ai.mines}")
print(f"moves_made = {ai.moves_made}")
print(ai.make_safe_move())
ai.add_knowledge(3, 2)
for i in range(len(ai.knowledge)):
    print(f"knowledge[{i}] = {ai.knowledge[i]}")
print(f"safe = {ai.safes}")
print(f"mines = {ai.mines}")
print(f"moves_made = {ai.moves_made}")
print(ai.make_safe_move())

class Sentence():
    # A Logical statement about a Minesweeper game.

    """A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    # a_sentence = Sentence(set of some cells, count of #mines in those cells)
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    # check equality of two sentences
    def __eq__(self, other):

        # checking eq of count is redundant though
        return self.cells == other.cells and self.count == other.count

    # sentence written as a string as 'set(cells) = count'
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        # is 'else return set()' valid?
        else:
            return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:

            # pop() removes arbitrary element and takes no arg, remove removes particular element
            self.cells.remove(cell)

            self.count -= 1  # count \geq 1 as it's given that cell is a mine.


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:  # else nothing to do
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # (List of sentences) about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates self.knowledge and self.mines
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates self.knowledge and self.safes
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # called in runner.py, line 214. given the cell and #mines in neighbors
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        (safe cell <- cell), (how many neighboring cells <- count) have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # self is placeholder for the minesweeperAI-class object, whenever a fn in the class calls another fn in the class

        # marks cell as move+safe cell and updates self.knowlege that cell is safe
        self.moves_made.add(cell)
        self.mark_safe(cell)  # all sentences mark cell as safe

        neighbor_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue  # move to next pair(i,j)

                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cells.add(cell)

        self.knowledge.append(Sentence(neighbor_cells, count))


        # Now get all possible new sentences
        ''' This is incorrect:
        Why? at the end of the loop knowledge is getting appended, which increases its size.
        Now, say A = B + C, A, B, C sets. Let x.cells = A, y.cells = B, knowledge = [x, y]
        Then first: s1 = x, s2 = x (1st elem of list). moves to next iteration
        s1 = x, s2 = y. moves into the if condition and knowledge = [A, B, C] now. ([x, y, z] actually)
        now s1 = x, s2 = z. moves into if and knowledge = [A, B, C, B]
        keeps repeating as [A, B, C, B, C, B, ...].

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                print(str(sentence1))
                if (not sentence1.cells == sentence2.cells
                    and sentence1.cells.issubset(sentence2.cells)):
                    cells = sentence2.cells - sentence1.cells
                    # don't use var = count here as count is already a var
                    new_count = sentence2.count - sentence1.count
                    self.knowledge.append(Sentence(cells, new_count))

                The key idea here is to make a copy of knowledge and then iterate for s1, s2 in the copy.
                In the if we append original knowledge, as is required.
                    '''
        knowledge2 = self.knowledge.copy()
        for sentence1 in knowledge2:
            for sentence2 in knowledge2:
                if (not sentence1.cells == sentence2.cells
                    and sentence1.cells.issubset(sentence2.cells)):
                    cells = sentence2.cells - sentence1.cells
                    # don't use var = count here as count is already a var
                    new_count = sentence2.count - sentence1.count
                    self.knowledge.append(Sentence(cells, new_count))

        # add in info about new mines/safes
        for sentence in self.knowledge:
            if sentence.known_mines() != set():  # equality of sets ie is known mines non empty
                for mine in sentence.known_mines():
                    self.mines.add(mine)
            if sentence.known_safes() != set():
                for safe in sentence.known_safes():
                    self.safes.add(safe)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print(self.safes)
        if self.safes == set():
            return None  # default return val for a fn, also see runner.py line181
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines and (i, j) in self.safes:
                    return (i, j)

        # no further action req here, like add (i, j) to self.move_made etc. see runner.py line214 and minesweeper.py add_knowledge, they take care of doing this

        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # note that this fn is only called when self.safes is a subset of self.moves_made, so it chooses a 'new' cell
        sample_space = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    sample_space.append((i, j))

        return random.choice(sample_space)


        raise NotImplementedError

Implementation: Minesweeper

import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # Now, board[i][j] = True means mine, False means safe

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    # A Logical statement about a Minesweeper game.

    """A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    # a_sentence = Sentence(set of some cells, count of #mines in those cells)
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    # check equality of two sentences
    def __eq__(self, other):

        # checking eq of count is redundant though
        return self.cells == other.cells and self.count == other.count

    # sentence written as a string as 'set(cells) = count'
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # return cells and set sentence to 'set() = 0' for easier cleaning of self.knowledge
        if len(self.cells) == self.count:
            mines_found = copy.copy(self.cells) # and not mines_found = self.cells, then in next step mines_found becomes set()
            self.cells = set()
            self.count = 0
            return mines_found
        else:
            return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            safes_found = copy.copy(self.cells)
            self.cells = set()
            return safes_found
        else:
            return set()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if cell not in it, then do nothing. Also, count >= 1 is ensured if cell is in it as it's a mine
        if cell in self.cells:

            # pop() removes arbitrary element and takes no arg, remove removes particular element
            self.cells.remove(cell)

            self.count -= 1  # count \geq 1 as it's given that cell is a mine.
            # notice the new sentence formed is shorter and different

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:  # else nothing to do
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # (List of sentences) about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates self.knowledge and self.mines
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates self.knowledge and self.safes
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # called in runner.py, line 214. given the cell and #mines in neighbors
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        (safe cell <- cell), (how many neighboring cells <- count) have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # self is placeholder for the minesweeperAI-class object, whenever a fn in the class calls another fn in the class

        # marks cell as move+safe cell and updates self.knowlege that cell is safe
        self.moves_made.add(cell)
        self.mark_safe(cell)  # all sentences in self.knowledge mark cell as safe ie delete cell, also cell added to self.safes as well

        neighbor_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cells.add((i, j))

        print(neighbor_cells)
        # neighbor_cells = {cell + 1, cell - 1, cell - 3}
        self.knowledge.append(Sentence(neighbor_cells, count))

        # get all possible new sentences
        ''' This is incorrect:
        Why? at the end of the loop knowledge is getting appended, which increases its size.
        Now, say A = B + C, A, B, C sets. Let x.cells = A, y.cells = B, knowledge = [x, y]
        Then first: s1 = x, s2 = x (1st elem of list). moves to next iteration
        s1 = x, s2 = y. moves into the if condition and knowledge = [A, B, C] now. ([x, y, z] actually). Size of knowledge has increased.
        now s1 = x, s2 = z. moves into if and knowledge = [A, B, C, B]
        keeps repeating as [A, B, C, B, C, B, ...].

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                print(str(sentence1))
                if (not sentence1.cells == sentence2.cells
                    and sentence1.cells.issubset(sentence2.cells)):
                    cells = sentence2.cells - sentence1.cells
                    # don't use var = count here as count is already a var
                    new_count = sentence2.count - sentence1.count
                    self.knowledge.append(Sentence(cells, new_count))

                The key idea here is to make a copy of knowledge and then iterate for s1, s2 in the copy.
                In the if we append original knowledge, as is required.
                    '''
        '''knowledge2 = self.knowledge.copy()
        for sentence1 in knowledge2:
            for sentence2 in knowledge2:
                if (not sentence1.cells == sentence2.cells
                    and sentence1.cells.issubset(sentence2.cells)):
                    cells = sentence2.cells - sentence1.cells
                    # don't use var = count here as count is already a var
                    new_count = sentence2.count - sentence1.count
                    self.knowledge.append(Sentence(cells, new_count))
        '''
        # The above is implemented in the while loop to keep getting new sentences when possible

        while True:
            print("Hi")
            knowledge = copy.deepcopy(self.knowledge)  # some sentences got modified with shallow copy
            for i in range(len(knowledge)):
                print(f"knowledge2[{i}] = {knowledge[i]}")

            # get new sentences
            for sentence1 in knowledge:
                for sentence2 in knowledge:
                    if (not sentence1.cells == sentence2.cells
                            and sentence1.cells.issubset(sentence2.cells) and sentence1.cells != set()):
                        new_cells = sentence2.cells - sentence1.cells
                        # don't use var = count here as count is already a var
                        new_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(new_cells, new_count)
                        self.knowledge.append(new_sentence)
                        self.knowledge.remove(sentence2)

            for i in range(len(self.knowledge)):
                print(f"knowledge[{i}] = {self.knowledge[i]}")
            print("now to collect info: ")

            # add info
            for sentence in self.knowledge:

                # collect obvious information ie known_mines and known_safes
                for mine in sentence.known_mines():

                    # add to mines, update self.knowledge's sentences as well
                    self.mines.add(mine)  # NOT self.mark_mine, we don't want to sum over all sentences.
                    sentence.mark_mine(mine)

                for safe in sentence.known_safes():
                    self.safes.add(safe)
                    sentence.mark_safe(safe)


                # we are mutating the sentences here, so self.knowledge is required in the first loop and not a copy. the size of self.knowledge is same though
                if not sentence.cells == set():  # just for speed
                    # for cell in self.moves_made:  (Not required as moves_made is a subset of safes)
                    #    sentence.mark_safe(cell)
                    for cell in self.safes:
                        sentence.mark_safe(cell)
                    for cell in self.mines:
                        sentence.mark_mine(cell)

            null_sentence = Sentence(set(), 0)
            while null_sentence in self.knowledge:
                self.knowledge.remove(null_sentence)

            for i in range(len(knowledge)):
                print(f"knowledgecopy[{i}] = {knowledge[i]}")
            for i in range(len(self.knowledge)):
                print(f"knowledge[{i}] = {self.knowledge[i]}")

            if len(knowledge) == len(self.knowledge):
                if len(knowledge) == 0:
                    return  # this needs to be taken care as it won't go into for loop if len = 0 as nothing to iterate over
                for i in range(len(knowledge)):
                    if knowledge[i].cells != self.knowledge[i].cells:
                        break
                    # so now they are equal objects ie nothing happened from start of the while loop ie no new knowledge
                    # null_sentences could still be there, so cleanup, then finish
                    null_sentence = Sentence(set(), 0)
                    while null_sentence in self.knowledge:
                        self.knowledge.remove(null_sentence)
                    return


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if self.safes == set():
            return None  # default return val for a fn, also see runner.py line181
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines and (i, j) in self.safes:
                    return (i, j)
        '''
        for i in range(8):
            if i not in self.moves_made and i not in self.mines and i in self.safes:
                return i'''
        # no further action req here, like add (i, j) to self.move_made etc. see runner.py line214 and minesweeper.py add_knowledge, they take care of doing this


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # note that this fn is only called when self.safes is a subset of self.moves_made, so it chooses a 'new' cell
        sample_space = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    sample_space.append((i, j))

        return random.choice(sample_space)

