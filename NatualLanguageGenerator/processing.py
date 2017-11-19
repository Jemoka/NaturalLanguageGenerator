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
