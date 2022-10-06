import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
NP -> Adj NP | N | Det N | Det Adj NP | NP P NP | NP Adv | Adv NP
VP -> V | VP Adv | Adv VP | V NP | V P NP
"""
# Det N | Det Adj NP instead of Det NP to avoid Det Det N
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            # print flattened version of the np tree
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    s = sentence.lower()
    word_list = nltk.word_tokenize(s)

    alphabets = []
    for i in range(26):
        alphabets.append(chr(ord('a') + i))

    for word in word_list:
        if any(char in alphabets for char in word):
            continue
        word_list.remove(word)

    return word_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # ///////////////////////////////////////////////////////////////////////
    # works on the crucial fact that a smallest NP must have length exactly 3
    # ///////////////////////////////////////////////////////////////////////
    smallest_nps = []
    for subtree in tree.subtrees(lambda t: t.height() == 3):
        if subtree.label() != 'NP':
            continue
        smallest_nps.append(subtree)
    return smallest_nps


if __name__ == "__main__":
    main()

'''
### Alternate Construction for np_chunk(tree): ###
def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    smallest_nps = []
    for child in tree:  # child = subtree with root connected to root node of tree
        smallest_nps.extend(get_smallest(child))
    return smallest_nps

    # Note: list1.extend(list2) adds list2 to the end of list1. list1 + list2 does the same thing


def get_smallest(tree):
    """
    input: a tree with label NP
    return list of all smallest np_chunks(also trees) in tree.
    ### works on the crucial fact that a smallest NP must have length exactly 3 ###
    """
    if tree.height() == 3 and tree.label() == 'NP':
        return [tree]

    smallest_chunks = []
    for child in tree:
        if tree.height() == 2:  # ex if tree = (V sat). would fail if condition and reach here.
            continue
        smallest_chunks.extend(get_smallest(child))
    return smallest_chunks

Note: why the height == 2 constraint:
ex. tree := (N holmes). then height = 2(N and holmes) and N -- holmes vertically in tree. so child becomes holmes, a string now. but get_smallest takes tree object as input.
string.height() not defined, so how will it check the if condition
'''
