import core
import pickle
import os


class IO:
    def __init__(self, object=core.Markov()):
        self.object = object
        self.path = ""

    def save(self, directory="", filename=""):
        path = os.path.join(directory, filename + "." + "MARKOVOBJ")
        with open(path, 'wb') as dataFile:
            pickle.dump(self.object, dataFile, pickle.HIGHEST_PROTOCOL)
        self.path = path

    def retrive(self, filePath=None):
        if not filePath:
            filePath = self.path
        with open(filePath, 'rb') as input:
            mobject = pickle.load(input)
        return mobject
