"""
NatualLanguageGenerator.py
Very, very, very simple handler to all of the functions inside
this package. Makes a basic NLG class, and makes a sentence.
"""
from .markov import Markov
from .popularWord import PopularWord


class NLG:
    def __init__(self, accuracy, data, algorithum="PopularWord"):
        if algorithum == "Markov":
            self.object = Markov(size=accuracy)
        elif algorithum == "PopularWord":
            self.object = PopularWord(size=accuracy)
        else:
            raise TypeError("Nonexsistant algorithum supplied")
        self.object.fit(data)

    def makeSentence(self):
        return self.object.formSentence()
