from NatualLanguageGenerator import NatualLanguageGenerator as nlg
generator = nlg.NLG(4, ["I do not like you"])
print(generator.makeSentence())

from NatualLanguageGenerator import io
ioObject = io.IO(object=generator.m)
ioObject.save("/Users/liujack/Desktop", "test")
m = ioObject.retrive("/Users/liujack/Desktop/test.MARKOVOBJ")
print(m.vocabulary)
