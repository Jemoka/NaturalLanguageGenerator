"""
NatualLanguageGenerator.py
Very, very, very simple handler to all of the functions inside
this package. Makes a basic Markov class, and makes a sentnece.
"""
import core


class NLG:
    def __init__(self, accuracy, data):
        self.m = core.Markov(size=accuracy)
        self.m.fit(data)

    def makeSentence(self):
        return self.m.formSentence()
