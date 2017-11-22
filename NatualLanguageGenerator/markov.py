import random
from .core import baseNLG
from .core import utilityFunctions


class Markov(baseNLG):
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
            grams = utilityFunctions.NGrams(self.n, i)
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
