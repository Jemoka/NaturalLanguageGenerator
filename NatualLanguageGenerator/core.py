import random
import base64
import zlib
from .io import markovobj


class Markov:
    # Init method that initializes the class variables
    def __init__(self, size=3):
        self.n = size
        self.vocabulary = {}
        self.data = list()
        pass

    # Utility (private) methods that this class will sourced
    # __NGrams: Parses a string into dictionary of NGrams, private
    def __NGrams(self, size, string):
        size -= 1
        tokens = ["$start/"] + string.split(" ") + ["end$"]
        grams = {}
        for startPos in range(0, len(tokens) - 1):
            n = size
            gram = []
            while n >= 0:
                try:
                    gram = gram + [tokens[startPos + n]]
                except IndexError:
                    pass
                n -= 1
            gram = tuple(list(reversed(gram)))
            try:
                if grams.get(gram) is None:
                    nextGrams = tuple()
                    for e in range(1, self.n + 1):
                        nextGram = (tokens[startPos + size + e],)
                        nextGrams = nextGrams + nextGram
                    grams[gram] = [nextGrams]
                else:
                    nextGrams = tuple()
                    for e in range(1, self.n + 1):
                        nextGram = (tokens[startPos + size + e],)
                        nextGrams = nextGrams + nextGram
                    grams[gram] = grams.get(gram) + [nextGrams]
            except IndexError:
                grams[gram] = ""
        return grams

    # __GetNext: Predicts the next set of grams from the current set
    def __GetNext(self, current=None):
        current = self.vocabulary.get(current)
        if not current:
            current = self.vocabulary.keys()
        selection = random.sample(current, 1)[0]
        return selection

    # Nonprivate Functions
    # Generation functions
    # fit: Adds data to class and parses it into NGrams, public
    def fit(self, data):
        # Usage: object.fit(List_Corpus)
        for i in data:
            self.data = self.data + [i]
            grams = self.__NGrams(self.n, i)
            self.vocabulary.update(grams)

    # formSentence: Forms a sentence via calling GetNext multiple times
    def formSentence(self, sentence='', current=None):
        # Usage: object.formSentence()
        # DO NOT PASS ANY PARAMETERS unless you know what you're doing
        nextWords = self.__GetNext(current=current)
        listNext = list(nextWords)
        tempSentence = " "
        for i in listNext:
            if i == "end$":
                return sentence + " " + tempSentence
            elif i == "$start/":
                pass
            elif any(stopword in ["!", ".", "?"] for stopword in i):
                return sentence + " " + tempSentence + " " + i
            else:
                tempSentence = tempSentence + " " + i
        return self.formSentence(sentence=tempSentence, current=current)

    # markovobj handlers
    # unpackObj: Unpacks and loads a object of class markovobj that was pickled
    def unpackObj(self, obj, verify=True):
        if verify:
            signatureString = base64.b64decode(obj.signature)
            signatureData = signatureString.split("/".encode())
            if str(zlib.crc32(signatureData[0])).encode() != signatureData[1]:
                raise RuntimeWarning("Object unverified, returning")
                return
        self.n = obj.gramSize
        self.data = obj.raw
        self.vocabulary = obj.vocabulary
        self.objSignature = obj.signature

    # generateObj: Generates a markovobj from the current class with an id
    def generateObj(self, identifier):
        return markovobj(self, identifier)
