from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# idea: AKnight equivalent to statement spoken by A is true, so all info is biconditional
# Let AK = AKnight, Ak = AKnave

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind.        # One of the two statements is true, so Ak, BK. It works.
# B says "We are of different kinds."  # id to BKnave \equiv same kind. so given AK <=> SK is true, Bk <=> SK is true ie AK <=> Bk <=> SK is true
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    Biconditional(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."  # clearly Bi(AK, Ak) is false, so that B is a Knave
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(Not(AKnight), Not(AKnave)),
    Or(BKnight, BKnave),
    Or(Not(BKnight), Not(BKnave)),
    Or(CKnight, CKnave),
    Or(Not(CKnight), Not(CKnave)),
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
