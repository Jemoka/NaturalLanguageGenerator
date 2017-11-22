import random
import operator
import ast


class countRanker(object):

    def __init__(self, data):
        self.raw = data
        self.refrences = {}
        self.vocabulary = []
        self.data = []
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
        self.pointTally()

    def pointTally(self):
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

    def next(self, current=None):
        potential = self.refrences.get(current)
        if not potential:
            return random.sample(list(self.refrences.keys()), 1)[0]
        countRanks = {}
        for i in potential:
            countRanks[i] = self.countRank.get(i)[0]
        return max(countRanks.items(), key=operator.itemgetter(1))[0]

    def speak(self, sentence="", current=None):
        next = self.next(current)
        if next == "$end":
            return sentence
        elif next == "$start/":
            return self.speak(sentence=sentence, current=next)
        sentence = sentence + " " + next
        return self.speak(sentence=sentence, current=next)


with open("parsed.json", "r") as file:
    corpus = ast.literal_eval(file.read())

keys = []
values = []
for i in list(corpus.keys()):
    keys = keys + [i.encode('unicode_escape').decode()]

for i in list(corpus.values()):
    values = values + [i.encode('unicode_escape').decode()]

r = countRanker(keys + values)
print(r.refrences)
for i in range(0, 500):
    try:
        print(r.speak().lower(), end="")
    except (UnicodeEncodeError, RecursionError):
        i -= 1
