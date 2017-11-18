import pickle
import os
import base64
import zlib


class markovobj:
    def __init__(self, coreObject, stringIdentifier):
        self.object = coreObject
        self.raw = coreObject.data
        self.vocabulary = coreObject.vocabulary
        self.gramSize = coreObject.n
        encodedID = stringIdentifier.encode()
        identifierHash = zlib.crc32(encodedID)
        signatureString = stringIdentifier + "/" + str(identifierHash)
        self.signature = base64.b64encode(signatureString.encode())


class fileWriter:
    def __init__(self, object):
        self.object = object
        self.path = ""

    def save(self, directory="", filename=""):
        path = os.path.join(directory, filename + "." + "markovobj")
        with open(path, 'wb') as dataFile:
            pickle.dump(self.object, dataFile, pickle.HIGHEST_PROTOCOL)
        self.path = path

    def retrive(self, filePath=None):
        if not filePath:
            filePath = self.path
        with open(filePath, 'rb') as input:
            mobject = pickle.load(input)
        return mobject
