import pickle
import os


class fileWriter:
    def __init__(self, object):
        self.object = object
        self.path = None

    def save(self, directory=None, filename=None):
        if not filename:
            if self.path:
                path = self.path
            else:
                raise ValueError("Please supply a directory and file name")
        else:
            path = os.path.join(directory, filename + "." + "generatorobj")
        with open(path, 'wb') as dataFile:
            pickle.dump(self.object, dataFile, pickle.HIGHEST_PROTOCOL)
        self.path = path

    def update(self, updatedObject):
        self.object = updatedObject

    def load(self, filePath=None, saveIntoClass=True):
        if not filePath:
            filePath = self.path
        with open(filePath, 'rb') as input:
            mobject = pickle.load(input)
        if saveIntoClass:
            self.object = mobject
        return mobject
