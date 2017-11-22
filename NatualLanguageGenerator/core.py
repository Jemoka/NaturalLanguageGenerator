import base64
import zlib
import pickle
from .processing import generatorobj


class utilityFunctions(object):
    # Utility (private) methods that this class will sourced
    # verifyObject: Verifies the signature of an object
    @staticmethod
    def verifyObject(obj):
        signatureString = base64.b64decode(obj.signature)
        signatureData = signatureString.split("/".encode())
        if str(zlib.crc32(signatureData[0])).encode() != signatureData[1]:
            # raise RuntimeWarning("Object unverified")
            return 1
        else:
            return 0

    # decodeObject: Turns a base64 string of an object to orignal form
    @staticmethod
    def decodeObject(stringObj):
        byteString = base64.b64decode(stringObj)
        return pickle.loads(byteString)

    # __NGrams: Parses a string into dictionary of NGrams, private
    @staticmethod
    def NGrams(gramSize, string):
        size = gramSize - 1
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
                    for e in range(1, gramSize + 1):
                        nextGram = (tokens[startPos + size + e],)
                        nextGrams = nextGrams + nextGram
                    grams[gram] = [nextGrams]
                else:
                    nextGrams = tuple()
                    for e in range(1, gramSize + 1):
                        nextGram = (tokens[startPos + size + e],)
                        nextGrams = nextGrams + nextGram
                    grams[gram] = grams.get(gram) + [nextGrams]
            except IndexError:
                grams[gram] = ""
        return grams


class baseNLG(object):
    # Init method that initializes the class variables
    def __init__(self, gramSize=3):
        self.n = gramSize
        self.vocabulary = {}
        self.data = list()
        pass

    # __GetNext: Predicts the next set of grams from the current set
    def __GetNext(self, current=None):
        '''
        Gets the next set of words based on the current set
        Or gets the next set of words randomly to start a sentence
        '''
        message = "baseNLG.__GetNext not implimented"
        raise NotImplementedError(message)

    # Nonprivate Functions
    # Generation functions
    # fit: Adds data to class and parses it into NGrams, public
    def fit(self, data):
        '''
        Fits the class of data for future generation needs
        '''
        message = "baseNLG.fit not implimented"
        raise NotImplementedError(message)

    # formSentence: Forms a sentence via calling GetNext multiple times
    def formSentence(self, sentence='', current=None):
        '''
        Forms a sentence from nothing or a current words
        Should be recursive
        '''
        message = "baseNLG.formSentence not implimented"
        raise NotImplementedError(message)

    # generatorobj handlers
    # unpackObj: Unpacks and loads a object of class generatorobj into class
    def unpackObj(self, obj, verify=True):
        '''
        Unpacks generatorObj that was depickled, optionally verifying it
        '''
        message = "baseNLG.unpackObj not implimented"
        raise NotImplementedError(message)

    # generateObj: Generates a generatorobj from the current class with an id
    def generateObj(self, identifier):
        return generatorobj(self, identifier)
