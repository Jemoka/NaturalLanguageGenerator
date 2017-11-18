"""
NatualLanguageGenerator.py
Very, very, very simple handler to all of the functions inside
this package. Makes a basic Markov class, and makes a sentnece.
"""
from . import core


class NLG:
    def __init__(self, accuracy, data):
        self.object = core.Markov(size=accuracy)
        self.object.fit(data)

    def makeSentence(self):
        return self.object.formSentence()
