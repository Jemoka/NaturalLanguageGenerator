import ast
import pickle
from NatualLanguageGenerator import io
from NatualLanguageGenerator import core
# from NatualLanguageGenerator import NatualLanguageGenerator as nlg

# generator = nlg.NLG(4, ["I do not like you"])
# print(generator.makeSentence())
#
# obj = generator.object
# markovObj = io.markovobj(obj, "test1")
# ioObject = io.fileWriter(markovObj)
# ioObject.save("/Users/liujack/Desktop", "test")
# m = ioObject.retrive()
#
# m = core.Markov()
# mObject = io.markovobj(obj, "test2")
# m.unpackObj(mObject)
# print(m.formSentence())

with open("parsed.json", "r") as file:
    corpus = ast.literal_eval(file.read())

m = core.Markov(size=5)
# m.fit(list(corpus.keys()) + list(corpus.values()))
m.fit(list(corpus.keys())+list(corpus.values()))
print(m.formSentence())
fileWritier = io.fileWriter(m.generateObj("studentCorpus"))
fileWritier.save("/Users/liujack/Documents/MarkovData", "studentCorpus")


directory = "/Users/liujack/Documents/MarkovData/studentCorpus.markovobj"
with open(directory, "rb") as file:
    mobj = pickle.load(file)
mclass = core.Markov()
mclass.unpackObj(mobj)
print("\n")
for i in range(0, 500):
    try:
        print(mclass.formSentence(), end="")
    except UnicodeEncodeError:
        i -= 1
