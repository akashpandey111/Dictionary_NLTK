#! /usr/bin/python

import sys
from nltk.corpus import wordnet
from sklearn.externals.joblib import load, dump

"""
__author__ = "Akash Pandey"
__email__ = "akashpandey111@gmail.com"
"""


WORDS = load('genuine.pkl')


def p(word, n=sum(WORDS.values())):
    return WORDS[word] / n


def correction(word): 
    """Most probable spelling correction for word."""
    return max(candidates(word), key=p)


def candidates(word): 
    """Generate possible spelling corrections for word."""
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


def known(words): 
    """The subset of `words` that appear in the dictionary of WORDS."""
    return set(w for w in words if w in WORDS)


def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word): 
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

if __name__ == '__main__':

    while True:
        search_word = raw_input("Word >>> ")

        if search_word == "exit":
            break

        if search_word != correction(search_word):
            print "Did you mean %s? If yes, please try again with the correct spelling!" % correction(search_word)

        try:
            sins = wordnet.synsets(search_word)

            print "\n\n%s:" %(sins[0].lemmas()[0].name())
            print "\nDefinition :", str(sins[0].definition())
            print "\nExamples :\n\n", sins[0].examples()

            synonyms = []
            antonyms = []

            for syn in sins:
                for l in syn.lemmas():
                    synonyms.append(l.name())
                    if l.antonyms():
                        antonyms.append(l.antonyms()[0].name())

            if synonyms:
                print "\nSynonyms : ", ", ".join([str(i) for i in list(set(synonyms))])
            if antonyms:
                print "Antonyms : ", ", ".join([str(i) for i in list(set(antonyms))])

            del synonyms, antonyms, search_word, sins

            print

        except LookupError:
            print "Unable to find search results for %s. Please check the word again." % search_word

    sys.exit(True)
