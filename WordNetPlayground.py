# Studying synonyms while learning about Wordnet & NLTK
# Adapted from https://pythonprogramming.net/wordnet-nltk-tutorial/
from nltk.corpus import wordnet as wn
import json

'''
Before we start...
A quick parts of speech lesson!

n = NOUN
A noun is a part of speech that serves as a subject or object.
More generally, we think of a noun as a person, place, thing,
quality, or action.

v = VERB
A verb is the part of speech that indicates what something does,
or what it is.

a = ADJECTIVE
An adjective is a word that modifies a noun (or pronoun) to make
it more specific. "Rotten eggs, smelly socks"

s = ADJECTIVE SATELLITE
A adj that always appear next to a word. "Atomic bomb"

r = ADVERB
An adverb is a word that modifies anything other than a noun,
usually a verb. "Done wisely"

Congratulations, you are now elementary-level educated in PoS
'''

# Wordnet is a web of words
# wn.synsets(someWord) returns all possible shades of meaning based on a word
# These sets of similar words is grouped in a object called 'synset'
SS = wn.synsets('establish')
print(SS)

# Isolating a synset from the list and printing out its metadata
# wordNetObject.name() returns metadata for synsets or word for lemmas
print(SS[0].name().split("."))  # [word, part of speech, definition #]

# Finding lemmas (essentially, expanded synsets) based on a synset
# A lemma countains a list of the possible synonyms from a synset
print(SS[0].lemmas())

# Isolating the word from a lemma
# This also uses wordNetObject.name()
print(SS[0].lemmas()[0].name())

# Working with synsets
# Returning definitions for a synsets
# synsetObj.definition() returns a string definition for a synsets
print(SS[0].definition())

# Returning examples of a use
# synsetObj.examples() returns an array of examples where the word is caused
print(SS[0].examples())

# Comparing two synsets
# synsetObj1.wup_similarity(synsetObj2) returns an float of simularties (0-1)
bathroom = wn.synset('bathroom.n.01')
toilet = wn.synset('toilet.n.01')
print(bathroom.wup_similarity(toilet))  # Bathroom is quite similar to toilet.

speak = wn.synset('speak.v.01')
toilet = wn.synset('toilet.n.01')
print(speak.wup_similarity(toilet))  # Speaking? Not so much.

# Working with lemmas
# Finding the antonyms of a lemmas
# lemmaObj.antonyms() returns an array of lemmas that are antonyms of a lemma
print(SS[0].lemmas()[0].antonyms())


# Putting it all together
# WordNet Browser Application
def browser(word):
    '''
    Goal: Establish a dictionary of words that are synonyms or antonyms of a
    user-inputted word and find the different shades of definitions
    '''
    data = {}
    # Step 1: get synsets
    SS = wn.synsets(word)

    # Step 2: Iterate over synsets to get synonyms and antonyms
    synonyms = {}
    antonyms = {}
    for synset in SS:
        # Step 2.1: Find and iterate over the lemma of a synset,
        # essentially finding the synonyms (and antonyms, in a sec)
        ssSynonyms = []
        ssAntonyms = []
        for syn in synset.lemmas():
            # Step 2.1.1: Add synonym (lemma.name()) to an synonyms array
            ssSynonyms = ssSynonyms + [syn.name()]
            for ant in syn.antonyms():
                ssAntonyms = ssAntonyms + [ant.name()]
        # Step 2.2: Add the synonym and antonyms into dictionaries
        # with keys equaling to the definition of the synset and PoS
        synsetID = synset.name().split(".")[1] + ". " + synset.definition()
        synonyms[synsetID] = ssSynonyms
        antonyms[synsetID] = ssAntonyms

    # Step 3: Add the two dictionaries up in "data", set some metadata
    data["query_word"] = word
    data["synonyms"] = synonyms
    data["antonyms"] = antonyms

    # Step 4: Return
    return json.dumps(data)


# Try it out!
print(browser("grand"))
