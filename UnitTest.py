# with open("parsed.json", "r") as file:
#     corpus = ast.literal_eval(file.read())import ast

# UnitTest: Tests all of the functions in the library
# This could also be used as documentation

# Goup 0: Importing Tests
from NatualLanguageGenerator import io
from NatualLanguageGenerator import popularWord
import ast


# Group 1: Core Tests
# Initializing a markov.Markov object
coreObject = popularWord.PopularWord()

# Fitting with data
with open("parsed.json", "r") as file:
    corpus = ast.literal_eval(file.read())

keys = []
values = []
for i in list(corpus.keys()):
    keys = keys + [i.encode('unicode_escape').decode()]

for i in list(corpus.values()):
    values = values + [i.encode('unicode_escape').decode()]

coreObject.fit(keys + values)
# coreObject.fit(["One fish two fish blue fish red fish"])

# Returning a sentence
print(coreObject.formSentence())


# Group 2: IO and exporting Tests
# Creating generatorobj from core class
gObj = coreObject.generateObj("test")

# Exporting JSON from generatorobj
print(gObj.exportJson())

# Initializing a io.fileWriter object with the generatorobj
fwObj = io.fileWriter(gObj)

# Writing the object to a file
fwObj.save("/Users/liujack/Desktop/", "test")

# Updating the object in core, processing, and fileWriter
coreObject.fit(["I do not like green eggs and ham"])
gObj.updateObject(coreObject)
fwObj.update(gObj)
fwObj.save()

# Retriving saved object
mObjRetrived = fwObj.load(filePath="/Users/liujack/Desktop/test.generatorobj")

# Loading saved object back into a core class
coreObject1 = popularWord.PopularWord()
coreObject1.unpackObj(mObjRetrived)
