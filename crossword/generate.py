import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        # sets up domains for each variable var in self.crossword.variables(Notice it's not variables() as variables is not a fn, it's an object associated with/ it's property of the crossword object)
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():  # dict.items() gives list of (key, value) as an iterable view object
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            length = var.length
            for word in self.domains[var].copy():
                if len(word) != length:
                    self.domains[var].remove(word)
        # no need for any return value

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # equality of Variable objects checked via == was implemented in the __eq__ method in the Variable Class
        # check that x, y not equal(not req as ac3 calls revise when x != y only). Also, self.overlaps in Crossword defined for x != y only.
        if x != y:
            if self.crossword.overlaps[x, y] is None:  # notice square brackets in overlaps
                return False  # x,y are arc-consistent. any value in y works for each value for x
            else:
                a, b = self.crossword.overlaps[x, y]

        Bool = False  # bool with lowercase b is a data type

        # check which words can give a possible y. other words won't give a solution->remove from domain of x
        for word in self.domains[x].copy():
            common_letter = word[a]
            if any((word2[b] == common_letter) for word2 in self.domains[y]):
                continue
            else:
                Bool = True
                self.domains[x].remove(word)
        return Bool

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # equivalent to for x: for y: if x != y: append((x, y)), with the for's and if's written L to R in the same way as while nesting them
            queue = [(x, y) for x in self.crossword.variables for y in self.crossword.variables if x != y]
        else:
            queue = arcs

        for arc in queue:
            x, y = list(arc)  # arc is a generator object, not exactly a tuple. convert it to tuple or list then use tuple assignment
            if not self.revise(x, y):  # notice that ac3 is indirectly, via calling self.revise updating self.domains.
                continue

            # domain of x is the one changing, if domain becomes empty, x can take no value->graph always arc-inconsistent->no solution
            if len(self.domains[x]) == 0:
                return False  # no arc-consistent graph possible

            # append neighbors of x to end of list to check them as well
            for z in self.crossword.neighbors(x):
                queue.append((x, z))  # neighbors(x) is set of all vars st var ^ x != set().

        # made it to an empty queue -> now domains are arc-consistent -> return True
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # check if all vars are assigned to something ie all vars are some or the other key, set(.) works too instead of len(.), but takes longer
        return len(assignment) == len(self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Note that the assignment may not be complete: not all variables will necessarily be present in the assignment.

        # check that all words assigned are distinct.
        if not len(set(assignment.values())) == len(assignment.keys()):
            return False

        # check correct length/node_consistency. We make this fn general: do not assume enforce_node_consistency was called before.
        for var, val in assignment.items():
            if not var.length == len(val):  # val is the string/word assigned to the variable var
                return False

        # check arc-consistency (no conflicting characters)
        for x in assignment:
            for y in assignment:
                # if self.revise(x, y): return False is incorrect as we don't want to modify anything else, we must just check if given assignment is consistent or not with the constraints
                if x == y or self.crossword.overlaps[x, y] is None:
                    continue
                a, b = self.crossword.overlaps[x, y]
                if assignment[x][a] != assignment[y][b]:
                    return False

        # made it till here -> correct length, no conflicting characters, no repeated words => consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # if word was the value of var, then how many total words are ruled out for var's neighbors? Call it p. then sort word in self.domains[var] in increasing order of p
        list_of_tuples = []
        for word in self.domains[var]:
            count = 0
            for neighbor in (self.crossword.neighbors(var) - set(assignment)):  # neighbor is a Variable intersecting var
                a, b = self.crossword.overlaps[var, neighbor]
                char = word[a]
                for word2 in self.domains[neighbor]:
                    if word2[b] != char:  # this particular word in neighbor is ruled out if word is the value of var
                        count += 1
            list_of_tuples.append((count, word))
        sorted_list_of_tuples = sorted(list_of_tuples)  # sorted based on list[i][0] in inc order
        return [elem[1] for elem in sorted_list_of_tuples]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # given: an INcomplete assignment
        list_of_unassigned_vars = set(self.domains) - set(assignment)
        minLen = len(self.crossword.words)
        best_vars = []
        for var in list_of_unassigned_vars:
            if len(self.domains[var]) < minLen:
                minlen = len(self.domains[var])
                best_vars = [var]
            elif len(self.domains[var]) == minLen:
                best_vars.append(var)

        maxDeg = 0
        for var in best_vars:
            if len(self.crossword.neighbors(var)) >= maxDeg:
                maxDeg = len(self.crossword.neighbors(var))
                best_var = var
        return var

    def inferences(self, assignment):

        domain_copy = self.domains.copy()
        for var in assignment:
            self.domains[var] = {assignment[var]}
        other_vars = set(self.domains) - set(assignment)

        # arcs to check for ac. No change in domain of vars in other_vars so the arcs between these vars are still consistent, no need to recheck those arcs.
        arcs = [(x, y) for x in set(self.domains) for y in set(self.domains) if (x != y and (x in assignment or y in assignment))]

        # now run ac3 with arcs.
        if self.ac3():  # ie now all vars are arc-consistent
            for var in other_vars:
                if len(self.domains[var]) == 0:
                    return None
                if len(self.domains[var]) == 1:
                    assignment.update({var: self.domains[var].pop()})
        self.domains = domain_copy  # restore original self.domains (the assignment is just a guess, need not be true)
        return assignment

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        # choose a var. Then we try its values(if there is a solution, then some value for this var gives a complete consistent assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignment_new = assignment.copy()
            assignment_new.update({var: val})
            if self.inferences(assignment_new) is None:
                continue  # this assignment_new doesn't work, try next val
            else:
                assignment_new2 = self.inferences(assignment_new)
            if self.consistent(assignment_new2):
                result = self.backtrack(assignment_new2)
                if result is not None:
                    return result  # result is the complete assignment
        # didn't return and finished checking all vals for var -> no solution with given assignment
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
