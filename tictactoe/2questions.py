v2:

import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for file in os.scandir(directory):
        with open(os.path.join(directory, file.name)) as f:
            files[file.name] = f.read()  # filename = file.name
    return files

    # Imp Note: open(file) takes in relative path of file as input which is filename only when file is directly in cwd


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    word_list = nltk.word_tokenize(document.lower())
    word_list = [word.translate(str.maketrans('', '', string.punctuation))
                 for word in word_list if not word in set(nltk.corpus.stopwords.words("english"))]

    # if tokenize returned a word "?", then above line turns it to "", and we remove these now
    word_list = [word for word in word_list if word != ""]

    return word_list

    # comprehension just like nested loops
    # string.punctuation = "!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    # str.replace(oldchr, newchr, count) replaces the first count occurences of oldchr with newchr, so word.replace(letter, "") if letter in string.punctuation works.
    # But str.replace takes 14x the time taken by str.translate


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    counts = {}
    for document in documents:
        for word in set(documents[document]):  # set(.) to not waste time when a word repeats in the text
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

    const = math.log(len(documents))
    return {word: (const - math.log(counts[word])) for word in counts}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}
    for file in files:  # files[file] is list of words in the file called file
        tfidf = 0
        for word in query:
            if word not in files[file]:
                continue
            tfidf += files[file].count(word) * idfs[word]
        tf_idfs[file] = tfidf

    # top n files as tuples (file, tfidf). Sort by second thing(the value here) in each item(a kv tuple) in the iterable
    top_files_tuple = sorted(tf_idfs.items(), key=lambda item: item[1], reverse=True)[:n]
    return [top_file[0] for top_file in top_files_tuple]

    # list[start:stop:step] returns list slice, starts at index = start till index < stop increasing start by step each time
    # basically like range(start, stop, step)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_idfs = {}
    for sentence in sentences:
        matching_word_measure = 0
        for word in query:
            if word in sentences[sentence]:
                matching_word_measure += idfs[word]
        sentence_idfs[sentence] = matching_word_measure

    sorted_sentences = sorted(sentence_idfs.items(), key=lambda item: (
        item[1], query_density(query, sentences[item[0]])), reverse=True)
    return [s[0] for s in sorted_sentences][:n]


def query_density(query, sentence):
    '''
    sentence = list of words
    query = set of words in query
    '''
    count = 0
    for word in sentence:
        if word in query:  # elem in set(.) is O(1)(indep of n)
            count += 1
    return count / len(sentence)


if __name__ == "__main__":
    main()

///////////////////////////////////////

v1:

import nltk
import sys
import os
import string
import math

FILE_MATCHES = 2
SENTENCE_MATCHES = 5


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for file in os.scandir(directory):
        with open(os.path.join(directory, file.name)) as f:
            files[file.name] = f.read()  # filename = file.name

    return files

    # Imp Note: open(file) takes in relative path of file as input which is filename only when file is directly in cwd


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    word_list = nltk.word_tokenize(document.lower())

    for word in word_list:
        if word in nltk.corpus.stopwords.words("english"):
            word_list.remove(word)
            continue
        for letter in word:
            if letter in string.punctuation:
                word.replace(letter, "")

    return word_list

# str.replace(oldchr, newchr, count) replaces the first count occurences of oldchr with newchr


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    counts = {}
    for document in documents:
        for word in set(documents[document]):  # set(.) to not waste time when a word repeats in the text
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

    log_num_docs = math.log(len(documents))
    return {word: (log_num_docs - math.log(counts[word])) for word in counts}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}
    for file in files:  # files[file] is list of words in file called file
        tfidf = 0
        for word in query:
            if word not in files[file]:
                continue

            tfidf += files[file].count(word) * idfs[word]
        tf_idfs[file] = tfidf

    # top n files as tuples (file, tfidf). Sort by second thing(the value here) in each item(a kv tuple) in the iterable
    top_files_tuple = sorted(tf_idfs.items(), key=lambda item: item[1], reverse=True)[:n]
    return [top_file[0] for top_file in top_files_tuple]

    # sorted(iterable) returns the sorted iterable, does not just update it
    # sorted(dict) sorts list of keys by default and returns list of keys in some kind(alphabetical/numericfor word in query: of ascending order
    # sorted(dict.values()) returns the same as above with key->value
    # sorted(dict.items()) returns list of kv pairs sorted by KEY in ascending order(by default if key=None it sorts full item ie lambda item: item)
    # tuples(sim.lists) have <, >, == based element-wise. Ex. (1, 1000) < (2, -1) and (1, 4) > (1, -1000) and (1, 2, 3) < (2, 3, 4, 5, 6, 7, 8, 9)
    # also, (1, 4) < (1, 4, 5) the shorter seq is considered smaller

    # list[start:stop:step] returns list slice, starts at index = start till index < stop increasing start by step each time
    # basically like range(start, stop, step)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    sentence_idfs = {}
    for sentence in sentences:
        matching_word_measure = 0
        for word in query:
            if word in sentences[sentence]:
                matching_word_measure += idfs[word]
        sentence_idfs[sentence] = matching_word_measure

    sorted_sentences = sorted(sentence_idfs.items(), key=lambda item: (item[1], 1-query_density(query, sentences[item[0]])), reverse=True)
    print(sorted_sentences[:5])

    '''### Not required here but very instructive ###
    for s1 in sorted_sentences:
        for s2 in sorted_sentences:

            if s1[0] == s2[0] or s1[1] != s2[1]:
                continue

            if query_density(query, sentences[s1[0]]) >= query_density(query, sentences[s2[0]]):
                continue


            # swap to keep sentences with identical idfs in descending query_density order. Here s2 has higher query_density
            # the tuple s1, part of the list sorted_sentences was assigned (sentence1, matching_word_measure1), now assign it to ((sentence2, matching_word_measure2)
            # s1, s2 = s2, s1 won't d anything as s1, s2 are not references to the elements of the list, rather they are just copies of the values of the elements of the list
            # but list[list.index(s1)] is indeed a reference to the element assigned as s1. list[i] is reference to ith element
            # sorted_sentences[sorted_sentences.index(s1)], sorted_sentences[sorted_sentences.index(s2)] = sorted_sentences[sorted_sentences.index(s2)], sorted_sentences[sorted_sentences.index(s1)]
            or: tmp = s1
            s1 = s2
            s2 = tmp
            i1 = sorted_sentences.index(s1)
            i2 = sorted_sentences.index(s2)
            sorted_sentences[i1], sorted_sentences[i2] = sorted_sentences[i2], sorted_sentences[i1]
    '''

    return [s[0] for s in sorted_sentences][:n]


def query_density(query, sentence):

    # sentence = list of words
    # query = set of words in query
    count = 0
    for word in sentence:
        if word in query:
            count += 1
    return count / len(sentence)

    '''Identical to above:
    count = 0
    for word in query:
        if word in set(sentence):  # set(.) is O(1), list is O(n)
            count += sentence.count(word)
    return count / len(sentence)
    '''

if __name__ == "__main__":
    main()
