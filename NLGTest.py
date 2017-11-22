from NatualLanguageGenerator.NatualLanguageGenerator import NLG
from NatualLanguageGenerator.NLGEngines.popularWord import PopularWord
nlg = NLG(["The quick brown fox jumped over the lazy dog".lower()], engine=PopularWord())
print(nlg.makeSentence())
print(nlg.object.countRank)
