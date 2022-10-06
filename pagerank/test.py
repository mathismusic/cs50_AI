'''from collections import Counter

corpus = {1: {1, 2, 3}, 2: {1, 2, 3}, 3: {1, 2, 3}}

d = 0.85
numlinks = {}
PageRank = {}
size = len(corpus.keys())
const_to_add = (1 - d) / size
for page in corpus:
    numlinks.update({page: len(corpus[page])})
    PageRank.update({page: 1 / size})  # add in the one kv pair dict to PageRank
    summation = 0
for page in corpus:
    for linked_page in corpus[page]:
        summation += PageRank[linked_page] / numlinks[linked_page]
    PageRank[page] = const_to_add + d * summation
print(PageRank)

x = [1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 7, 8]
print(dict(Counter(x)))
print(list(corpus.keys()))'''

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
    print(transition_model(corpus, "1.html", DAMPING))
    '''ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    '''

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
    numlinks_page = len(linked_pages)
    distribution = {}
    size = len(corpus)
    for page in corpus.keys():
        distribution.update({page: (1 - damping_factor) / size})
    if numlinks_page != 0:
        for linked_page in linked_pages:
            distribution[linked_page] += damping_factor / numlinks_page
    else:
        distribution[linked_page] = 1 / size  # add damping_factor / size

    tot_sum = 0
    for page in corpus:
        tot_sum += distribution[page]
    for page in corpus:
        distribution[page] = distribution[page] / tot_sum

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = 1
    list_of_pages = []
    pages = list(corpus.keys())
    print(pages)
    list_of_pages.append(random.choice(pages))
    return pages
