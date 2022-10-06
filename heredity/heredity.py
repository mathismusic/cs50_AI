import csv
import itertools
import sys

# a Dictionary, superb way to create it as well
PROBS = {

    # 1.Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    # 2.Conditional Probability of having Trait given no. of genes
    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # 3.Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        # DictReader returns a CSV Object that iterates over rows, with reader[a title] = the row's entry for that title
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,  # if row["mother"] is there then that else None (blank)
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else  # all in one line
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint unconditional probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # idea: P(...DCBA) = P(A)P(B|A)P(C|BA)..., any event can be A.
    P = 1
    no_genes = set(people) - one_gene - two_genes
    # dict.keys() returns list of keys as a dict_keys object, set(dict) returns set of keys

    p = PROBS["mutation"]

    ''' main idea:
        if f + m == 4:  # use sum as Prob of # of genes is symm in f, m
            probabilities[person]["gene"][2] = (1 - p) ** 2  # or 1-(2p-p^2) by IEP
            probabilities[person]["gene"][1] = 2 * p * (1 - p)  # or 2(p-p^2) by Venn
            probabilities[person]["gene"][0] = p ** 2
        elif f + m = 3:  # => 1, 2 or 2, 1
            probabilities[person]["gene"][2] = (1 - p) / 2  # (1 - p) * p * 0.5 + ((1 - p) ** 2) * 0.5
            probabilities[person]["gene"][1] = 0.5
            probabilities[person]["gene"][0] = p / 2  # p(1-p)0.5 + p.p0.5
        elif f == m == 1:
            probabilities[person]["gene"][2] = 0.25  # 0.25 * ((1 - p) ** 2) + 0.5 * p * (1 - p) + 0.25 * (p ** 2)
            probabilities[person]["gene"][1] = 0.5  # 0.5((1 - p)^2 + p^2) + 0.25 * 2p(1-p) + 0.25 * 2p(1-p)
            probabilities[person]["gene"][0] = 0.25
        elif f + m == 2:  # and not 1, 1. =>2, 0 / 0, 2
            probabilities[person]["gene"][2] = p * (1 - p)  # the gene from 0 has to mutate
            probabilities[person]["gene"][1] = ((1 - p) ** 2) + (p ** 2)
            probabilities[person]["gene"][0] = p * (1 - p)  # gene from 1 has to mutate
            # notice the similarity between this case and f+m=4
        elif f + m == 1:
            probabilities[person]["gene"][2] = p / 2  # 0.5 * (p ** 2) + 0.5 * p * (1 - p)
            probabilities[person]["gene"][1] = 0.5
            probabilities[person]["gene"][0] = (1 - p) / 2
            # just the reverse order of f+m = 3
        elif f + m == 0:
            probabilities[person]["gene"][2] = p ** 2
            probabilities[person]["gene"][1] = 2 * p * (1 - p)
            probabilities[person]["gene"][0] = (1 - p) ** 2
            # just reverse of f+m=4
            '''
    # note that person is the name of the person
    for person in one_gene:
        if people[person]["mother"] is None:  # person is a dict as well, no need of people[person]["mother"]
            P = P * PROBS["gene"][1]
            # if in have_trait as well, then * PROBS["trait"][1] too, taken care later in fn
        else:
            f = NumGenes(people[person]["father"], one_gene, two_genes)
            m = NumGenes(people[person]["mother"], one_gene, two_genes)
            if f + m == 4 or f + m == 0:  # 1,2 or 2,1 same for kid's gene probability ie symm in f,m so use sum
                P = P * (2 * p * (1 - p))
            elif f + m == 3 or f + m == 1 or f == m == 1:
                P = P / 2
            elif f + m == 2:  # so 0,2 or 2,0
                P = P * (((1-p)**2) + (p**2))

        if person in have_trait:
            P = P * PROBS["trait"][1][True]
        else:
            P = P * PROBS["trait"][1][False]

    for person in two_genes:
        if people[person]["mother"] is None:
            P = P * PROBS["gene"][2]
        else:
            f = NumGenes(people[person]["father"], one_gene, two_genes)
            m = NumGenes(people[person]["mother"], one_gene, two_genes)
            if f + m == 4:
                P = P * ((1-p)**2)
            elif f + m == 3:
                P = P * (1-p) * 0.5
            elif f == m == 1:
                P = P / 4
            elif f + m == 2:
                P = P * p * (1-p)
            elif f + m == 1:
                P = P * p * 0.5
            elif f + m == 0:
                P = P * (p**2)

        if person in have_trait:
            P = P * PROBS["trait"][2][True]
        else:
            P = P * PROBS["trait"][2][False]

    for person in no_genes:
        if people[person]["mother"] is None:
            P = P * PROBS["gene"][0]
        else:
            f = NumGenes(people[person]["father"], one_gene, two_genes)
            m = NumGenes(people[person]["mother"], one_gene, two_genes)
            if f + m == 4:
                P = P * (p**2)
            elif f + m == 3:
                P = P * p * 0.5
            elif f == m == 1:
                P = P / 4
            elif f + m == 2:
                P = P * p * (1-p)
            elif f + m == 1:
                P = P * (1-p) * 0.5
            elif f + m == 0:
                P = P * ((1-p)**2)

        if person in have_trait:
            P = P * PROBS["trait"][0][True]
        else:
            P = P * PROBS["trait"][0][False]

    return P


def NumGenes(person, one_gene, two_genes):
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # idea: keeping adding the joint prob values for each set of possibilities of parents' genes. By law of tot prob, this is just the req P
    # basically P(A) = P(A(BCDE)) + ABCDE' + ABCD'E + ... AB'C'D'E'
    # just visualise how lines 67-77 work, it's obvious why person["trait"][True] == 1 when it is given so in the file, though unconditional is taken in joint_probability
    # less code but slower(redundant checking): for person in people:
    #                                               probabilities[person]["gene"][NumGenes(person, one_gene, two_genes)] += p

    for person in (set(probabilities) - one_gene - two_genes):  # no_genes not defined in this fn
        probabilities[person]["gene"][0] += p
    for person in one_gene:
        probabilities[person]["gene"][1] += p
    for person in two_genes:
        probabilities[person]["gene"][2] += p

    for person in have_trait:
        probabilities[person]["trait"][True] += p
    for person in (set(probabilities) - have_trait):  # ie for them p = probability to not_have_trait in a case of some other fixed conditions
        probabilities[person]["trait"][False] += p

    return


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        sum_tot = 0
        for i in range(3):
            sum_tot += probabilities[person]["gene"][i]
        for i in range(3):
            probabilities[person]["gene"][i] = probabilities[person]["gene"][i] / sum_tot

        sum_tot = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / sum_tot
        probabilities[person]["trait"][False] = 1 - probabilities[person]["trait"][True]
        # float addition easier than float division


if __name__ == "__main__":
    main()
