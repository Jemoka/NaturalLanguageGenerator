# with open("parsed.json", "r") as file:
#     corpus = ast.literal_eval(file.read())import ast

# UnitTest: Tests all of the functions in the library
# This could also be used as documentation

# Goup 0: Importing Tests
from NatualLanguageGenerator import io
from NatualLanguageGenerator import markov


# Group 1: Core Tests
# Initializing a markov.Markov object
coreObject = markov.Markov()

# Fitting with data
# with open("parsed.json", "r") as file:
#     corpus = ast.literal_eval(file.read())
# coreObject.fit(list(corpus.keys()) + list(corpus.values()))
coreObject.fit(["One fish two fish blue fish red fish"])

# Returning a sentence
print(coreObject.formSentence())


# Group 2: IO and exporting Tests
# Creating generatorobj from core class
mObj = coreObject.generateObj("test")
print(mObj.vocabulary)

# Exporting JSON from generatorobj
print(mObj.exportJson())

# Initializing a io.fileWriter object with the generatorobj
fwObj = io.fileWriter(mObj)

# Writing the object to a file
fwObj.save("/Users/liujack/Desktop/", "test")

# Updating the object in core, processing, and fileWriter
coreObject.fit(["I do not like green eggs and ham"])
mObj.updateObject(coreObject)
fwObj.update(mObj)
fwObj.save()

# Retriving saved object
mObjRetrived = fwObj.load(filePath="/Users/liujack/Desktop/test.generatorobj")

# Loading saved object back into a core class
coreObject1 = markov.Markov()
coreObject1.unpackObj(mObjRetrived)
