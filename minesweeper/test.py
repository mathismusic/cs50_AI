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
            knowledge = self.knowledge.copy()
            # get new sentences
            for sentence1 in knowledge:
                for sentence2 in knowledge:
                    if (not sentence1.cells == sentence2.cells
                            and sentence1.cells.issubset(sentence2.cells)):
                        cells = sentence2.cells - sentence1.cells
                        # don't use var = count here as count is already a var
                        new_count = sentence2.count - sentence1.count
                        self.knowledge.append(Sentence(cells, new_count))

            '''for sentence1 in knowledge:
                for sentence2 in knowledge:
                    if (not sentence1.cells == sentence2.cells
                            and sentence1.cells.issubset(sentence2.cells)):
                        cells = sentence2.cells - sentence1.cells
                        # don't use var = count here as count is already a var
                        new_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(cells, new_count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(Sentence(cells, new_count))
            '''
            # add info
            for sentence in self.knowledge.copy():

                # collect obvious information ie known_mines and known_safes
                print(f"line212: {sentence.known_mines()}")
                print(len(sentence.known_mines())

                if len(sentence.known_mines()) != 0:

                    print(f"line 214: {sentence.known_mines()}")
                    # copy so that set size is constant during iteration
                    for mine in sentence.known_mines().copy():

                        print(mine)
                        # add to mines, update self.knowledge's sentences as well
                        self.mines.add(mine)  # NOT self.mark_mine, we don't want to sum over all sentences.
                        sentence.mark_mine(mine)

                if not sentence.known_safes() == set():  # not elif as both clauses are not necessarily disjoint. Both can run one after the other
                    for safe in sentence.known_safes().copy():
                        self.safes.add(safe)
                        sentence.mark_safe(safe)

                ''' integrate cell wise information into sentences. In different loop to access the new sets of safes, mines.'''

                # all previously safe cells to be removed from sentences with them
                # these sentences could be created if a previously safe cell is neighbor of the current move cell

                knowledge = self.knowledge.copy()
                for sentence in self.knowledge:  # we are mutating the sentences, so self.knowledge is required.
                    if not sentence.cells == set():
                        # for cell in self.moves_made:  (Not required as moves_made is a subset of safes)
                        #    sentence.mark_safe(cell)  # moves_made cells are safe
                        for cell in self.safes:
                            sentence.mark_safe(cell)
                        for cell in self.mines:
                            sentence.mark_mine(cell)

            # some 'set() = 0' sentences are created if all are mines, for example or if all are safe.
            # nonzero sets are in sentence.cells only if undecidable.
            # this is very efficient. the knowledge is getting all the information possible taken out.
            # clean self.knowledge: let's remove all set() = 0 sentences in self.knowledge.
            knowledge2 = knowledge.copy()
            if knowledge2 == []:
                print("Yes!")
                return
            for sentence in knowledge2:
                if sentence.cells == set():

                    # keep editing self.knowledge & knowledge (knowledge too as we have to check the next if condition)
                    # iterate over constant knowledge2
                    self.knowledge.remove(sentence)
                    knowledge.remove(sentence)

            # finish and return if no more stuff to add
            null_sentence = Sentence(set(), 0)
            if knowledge == self.knowledge:
                while null_sentence in self.knowledge:
                    self.knowledge.remove(null_sentence)  # remove(x) removes first instance of element x from list
                return
            else:
                while null_sentence in self.knowledge:
                    self.knowledge.remove(null_sentence)  # remove(x) removes first instance of element x from list
                while null_sentence in knowledge:
                    knowledge.remove(null_sentence)  # remove(x) removes first instance of element x from list
                knowledge = self.knowledge.copy()


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
ai.add_knowledge(4, 2)
# prints ai.knowledge[i] as str ie prints str(ai.knowledge[2]) ie {3} = 0, nice!
for i in range(len(ai.knowledge)):  # by def do nothing if len = 0
    print(f"knowledge[{i}] = {ai.knowledge[i]}")

print(f"safe = {ai.safes}")
print(f"mines = {ai.mines}")         # 0  1 y 2 _ 3 n(add_knowledge(4, 2) gives {3} = 0) 4 n 5 y 6
print(f"moves_made = {ai.moves_made}")
print(f"safe move = {ai.make_safe_move()}")
ai.add_knowledge(3, 2)  #so 0 y, 2 y, total: y = 0, 1, 2, 5  n = 3, 4
for i in range(len(ai.knowledge)):
    print(f"knowledge[{i}] = {ai.knowledge[i]}")
print(f"safe = {ai.safes}")
print(f"mines = {ai.mines}")
print(f"moves_made = {ai.moves_made}")
print(f"safe move = {ai.make_safe_move()}")
