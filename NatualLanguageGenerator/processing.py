import base64
import zlib
import json


def key_to_json(data):
    if data is None or isinstance(data, (bool, int, str)):
        return data
    if isinstance(data, (tuple, frozenset)):
        return str(data)
    raise TypeError


def to_json(data):
    if data is None or isinstance(data, (bool, int, tuple, range, str, list)):
        return data
    if isinstance(data, (set, frozenset)):
        return sorted(data)
    if isinstance(data, dict):
        return {key_to_json(key): to_json(data[key]) for key in data}
    raise TypeError


class generatorobj:
    def __init__(self, coreObject, stringIdentifier):
        self.object = coreObject
        self.raw = coreObject.data
        self.vocabulary = coreObject.vocabulary
        self.gramSize = coreObject.n
        encodedID = stringIdentifier.encode()
        identifierHash = zlib.crc32(encodedID)
        signatureString = stringIdentifier + "/" + str(identifierHash)
        self.signature = base64.b64encode(signatureString.encode())

    def updateObject(self, updatedCoreObject):
        self.object = updatedCoreObject
        self.raw = updatedCoreObject.data
        self.vocabulary = updatedCoreObject.vocabulary
        self.gramSize = updatedCoreObject.n

    def exportJson(self):
        rawData = {str("rawData"): to_json(self.raw)}
        vocabulary = {str("parsedData"): to_json(self.vocabulary)}
        gramSize = {str("dataGramSize"): int(self.gramSize)}
        signature = {str("signature"): self.signature.decode()}
        data = {}
        dicts = [rawData, vocabulary, gramSize, signature]
        for d in dicts:
            data.update(d)
        return json.dumps(data)
