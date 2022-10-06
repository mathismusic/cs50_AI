import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = corpus[page]
    numlinks = len(linked_pages)
    distribution = {}
    size = len(corpus)

    if numlinks != 0:
        for page in corpus.keys():
            distribution.update({page: (1 - damping_factor) / size})

        for linked_page in linked_pages:
            distribution[linked_page] += damping_factor / numlinks

        # it's a Prob Dist, so Normalise, not req is numlinks == 0, already normalised in that case
        tot_sum = 0
        for page in corpus:
            tot_sum += distribution[page]
        for page in corpus:
            distribution[page] = distribution[page] / tot_sum
    else:
        for page in corpus.keys():
            distribution.update({page: 1 / size})  # id to add damping_factor / size to distribution[page] = 1-d / size

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    list_of_pages = []
    page = random.choice(list(corpus.keys()))
    list_of_pages.append(page)
    samples = 1

    for i in range(n - 1):  # n - 1 more samples required
        distribution = transition_model(corpus, page, damping_factor)
        page = random.choices(list(distribution.keys()), list(distribution.values()), k=1)
        page = "".join(page)  # s.join(list) gives the string list[0]slist[1]s...slist[n - 1], s is a string, here s=""
        list_of_pages.append(page)

    PageRank = {}
    for page in corpus:
        PageRank.update({page: list_of_pages.count(page) / n})

    return PageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    size = len(corpus)
    d = damping_factor
    const_to_add = (1 - d) / size

    # this is the dictionary comprehension Method.
    PageRank = {
        page: 1 / size
        for page in corpus
    }

    # keep repeating while |before - after| > 0.001
    Bool = False
    while Bool == False:
        Bool = True
        PageRank_before = PageRank.copy()

        for page in corpus:  # iterates over keys of dict

            before = PageRank_before[page]
            summation = 0
            for page2 in corpus:
                if page in corpus[page2]:
                    if len(corpus[page2]) != 0:
                        summation += PageRank_before[page2] / len(corpus[page2])
                    else:
                        summation += PageRank_before[page2] / size  # size = len(corpus)

            after = PageRank[page] = const_to_add + d * summation
            if abs(before - after) > 0.001:
                if Bool == True:
                    Bool = False

    # Normalise
    tot_sum = 0
    for page in corpus:
        tot_sum += PageRank[page]
    for page in corpus:
        PageRank[page] = PageRank[page] / tot_sum
    return PageRank


if __name__ == "__main__":
    main()
