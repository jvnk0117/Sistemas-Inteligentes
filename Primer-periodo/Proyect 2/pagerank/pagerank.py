#Lizbeth Paulina Ayala Parra A01747237
#Alejandro Perez Gonzalez A01746643
import os
import re
import sys
import random
from typing import Dict, List

DAMPING = 0.85
SAMPLES = 10000
INCLUDE_ITERATE_PAGERANK = True


def main():
    # check that they have given a corpus as a command-line argument
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    if INCLUDE_ITERATE_PAGERANK:
        ranks = iterate_pagerank(corpus, DAMPING)
        print(f"PageRank Results from Iteration")
        for page in sorted(ranks):
            print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory: str) -> Dict[str, List[str]]:
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


def transition_model(corpus: Dict[str, List[str]], page: str, damping_factor: float):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    num_pages = len(corpus)
    transition_probabilities = dict()
    if corpus[page]:
        link_prob = damping_factor / len(corpus[page])
        for link in corpus[page]:
            transition_probabilities[page] = link_prob
    else:
        link_prob = damping_factor / num_pages
        for page in corpus:
            transition_probabilities[page] = link_prob

    random_prob = (1 - damping_factor) / num_pages
    for page in corpus:
        if page not in transition_probabilities:
            transition_probabilities[page] = random_prob

    return transition_probabilities


def sample_pagerank(corpus: Dict[str, List[str]], damping_factor: float, n: int) -> Dict[str, float]:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = dict()
    current_page = random.choice(list(corpus.keys()))

    """Initialize page rank with zero for all pages"""
    for page in corpus:
        page_rank[page] = 0

    """Perform random walk and accumulate page ranks"""
    for i in range(n):
        page_rank[current_page]+= 1
        transition_probabilities = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(list(transition_probabilities.keys()),list(transition_probabilities.values()))[0]
        current_page = next_page

    """Normalize page ranks to get estimated PageRank values"""
    total_visits = sum(page_rank.values())
    for page in page_rank:
        page_rank[page] /= total_visits

    return page_rank



def iterate_pagerank(corpus: Dict[str, List[str]], damping_factor: float, epsilon: float = 0.001) -> Dict[str, float]:
    """
    This function is EXTRA CREDIT -- not required for the project. If you complete
    it, you will have 20 extra points to be applied if you miss points on other projects.

    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    num_pages = len(corpus)

    """Initialize PageRank values with equal probability"""
    page_rank: Dict = {page: 1 / len(corpus) for page in corpus}

    """Initialize page rank with equal values for all pages"""
    initial_page_rank = 1 / num_pages
    for page in corpus:
        page_rank[page] = initial_page_rank

    converged = False
    while not converged:
        new_page_rank = dict()
        for page in corpus:
            new_pr = (1 - damping_factor) / num_pages
            for link_page, links in corpus.items():
                if page in links:
                    new_pr += damping_factor * page_rank[link_page] / len(links)
            new_page_rank[page] = new_pr

        """Check for convergence"""
        max_change = max(abs(new_page_rank[page] - page_rank[page]) for page in corpus)
        if max_change < epsilon:
            converged = True

        page_rank = new_page_rank

    sum_pagerank = sum(page_rank.values())
    assert abs(sum_pagerank - 1) < 1e-6, "Sum of PageRank values is not close to 1: {}".format(sum_pagerank())

    return page_rank


if __name__ == "__main__":
    main()
