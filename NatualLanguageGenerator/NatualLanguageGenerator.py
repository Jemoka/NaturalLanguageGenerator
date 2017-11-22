"""
NatualLanguageGenerator.py
Very, very, very simple handler to all of the functions inside
this package. Makes a basic NLG class, and makes a sentence.
"""
from .NLGEngines.markov import Markov
from .NLGEngines.popularWord import PopularWord


class NLG:
    def __init__(self, data, accuracy=3, engine=None, algorithum="Markov"):
        if engine is not None:
            self.object = engine
            self.object.fit(data)
            return
        if algorithum == "Markov":
            self.object = Markov(size=accuracy)
        elif algorithum == "PopularWord":
            self.object = PopularWord(size=accuracy)
        else:
            raise TypeError("Nonexsistant algorithum supplied")
        self.object.fit(data)

    def makeSentence(self):
        return self.object.formSentence()
