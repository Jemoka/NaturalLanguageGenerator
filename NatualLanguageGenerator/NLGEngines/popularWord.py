import random
import operator
import ast
from NatualLanguageGenerator.core import baseNLG
from NatualLanguageGenerator.core import utilityFunctions
from NatualLanguageGenerator.processing import generatorobj

with open("parsed.json", "r") as file:
    corpus = ast.literal_eval(file.read())

keys = []
values = []
for i in list(corpus.keys()):
    keys = keys + [i.encode('unicode_escape').decode()]

for i in list(corpus.values()):
    values = values + [i.encode('unicode_escape').decode()]


class PopularWord(baseNLG):
    def __init__(self):
        self.raw = []
        self.refrences = {}
        self.vocabulary = []
        self.data = []

    def __GetNext(self, current=None):
        potential = self.refrences.get(current)
        if not potential:
            return random.sample(list(self.refrences.keys()), 1)[0]
        countRanks = {}
        for i in potential:
            countRanks[i] = self.countRank.get(i)[0]
        return max(countRanks.items(), key=operator.itemgetter(1))[0]

    def fit(self, data):
        for i in data:
            tokens = ["$start/"] + i.split(" ") + ["$end"]
            self.vocabulary = self.vocabulary + tokens
            grams = []
            for i in range(0, len(tokens) - 1):
                grams = grams + [[tokens[i], tokens[i + 1]]]
            self.data = self.data + grams
            for pair in grams:
                if not self.refrences.get(pair[0]):
                    self.refrences[pair[0]] = [pair[1]]
                else:
                    oldPair = self.refrences[pair[0]]
                    self.refrences[pair[0]] = oldPair + [pair[1]]
        self.__tallyCounts()

    def __tallyCounts(self):
        keys = list(self.refrences.keys())
        values = list(self.refrences.values())
        keyTallies = {}
        for i in keys:
            tally = 0
            for e in values:
                for s in e:
                    if i == s:
                        tally += 1
            keyTallies[i] = tally
        tallies = {}
        for key, value in self.refrences.items():
            for i in value:
                oldTally = tallies.get(i)
                if not oldTally:
                    if keyTallies[key] == 0:
                        tallies[i] = [1, [key]]
                    else:
                        tallies[i] = [keyTallies[key], [key]]
                else:
                    if oldTally == 0:
                        tallies[i] = [1, key]
                    else:
                        tallies[i] = [oldTally[0] + keyTallies[key], oldTally[1] + [key]]
        self.countRank = tallies

    def formSentence(self, sentence='', current=None):
        next = self.__GetNext(current)
        if next == "$end":
            return sentence
        elif next == "$start/":
            return self.formSentence(sentence=sentence, current=next)
        sentence = sentence + " " + next
        return self.formSentence(sentence=sentence, current=next)

    # generatorobj handlers
    # unpackObj: Unpacks and loads a object of class generatorobj into class
    def unpackObj(self, obj, verify=True):
        if verify:
            if utilityFunctions.verifyObject(obj) != 0:
                raise RuntimeError("Object recived not verified")
        mObject = utilityFunctions.decodeObject(obj.pObject)
        try:
            self.raw = mObject.raw
            self.vocabulary = mObject.vocabulary
            self.data = mObject.data
            self.countRank = mObject.countRank
            self.refrences = mObject.refrences
            self.objSignature = obj.signature
        except AttributeError:
            message = "Object given is not object of class PopularWord"
            raise AttributeError(message)

    # generateObj: Generates a generatorobj from the current class with an id
    def generateObj(self, identifier):
        return generatorobj(self, identifier)
