from nltk.corpus import treebank
from nltk import chunk
from nltk.chunk.util import tagstr2tree
from nltk import word_tokenize
from nltk import RegexpTokenizer
from nltk import RegexpParser
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from nltk import pos_tag
from nltk import Text
from nltk import Tree
import json
import re
import sys


def makeString(words):
    string = ""
    for i in words:
        string = string + " " + i
    return string


def multiSplit(string, arraySplitters):
    tokenizer = RegexpTokenizer(r'\w+')
    splitterString = arraySplitters[0]
    for i in arraySplitters[1:]:
        splitterString = splitterString + "|" + i
    regexp = r'\s(?=(?:' + splitterString + r')\b)'
    result = re.split(regexp, string)
    return result


def fuzzyFind(dictionary, keyword):
    results = []
    for key, value in dictionary.items():
        if keyword in key:
            results.append(value)
    return results


def join(dicts):
    super_dict = {}
    for d in dicts:
        for k, v in d.items():
            super_dict.setdefault(k, []).append(v)
    return super_dict


def treeIfy(taggedSentence):
    # NP: {<JJ>*<NN>+}
    # {<JJ>*<NN><CC>*<NN>+}
    # {<JJ>*<NN|NNS>+}      PP: {<IN><DT>?<NP>}
    grammar = """
    LIST: {(<JJ>*<NN|NNS><,>?)+(<CC><JJ>*<NN|NNS>)}
    NP: {<DT>?<JJ>*<NN|NNS>+}
    {<DT>?<JJ>*<NN><CC>*<NN>+}
    {<DT>?<JJ>* <NN.*>+ <IN>?}
    {<DT>?<JJ>* <NN.*>+ <IN>?}
    {<DT>?<JJ>* <LIST>+}
    PP: {<IN><NP>}
    VP: {<VB|VBG|VBD|VBN|VBP|VBZ><.*>*}
    }<.>{
    """
    NPChunker = RegexpParser(grammar)
    return NPChunker.parse(taggedSentence)


def dictIfy(tuple):
    ds = []
    for x, y in tuple:
        ds.append({y: x})
    return join(ds)


def tree2dict(t):
    return {t.label(): [tree2dict(i) if isinstance(i, Tree) else i for i in t]}


def correctParticles(p):
    verbList = reduceLevel(fuzzyFind(dictIfy(p), "VB"))
    if len(verbList) <= 1:
        return p
    verbFound = False
    correctedList = []
    for word, PoS in p:
        if word in verbList:
            if PoS == "VBG" and verbFound:
                correctedList.append((word, "PARTICLE"))
            if not verbFound:
                correctedList.append((word, PoS))
                verbFound = True
        else:
            correctedList.append((word, PoS))
    return correctedList


def reduceLevel(array):
    output = []
    for sublist in array:
        for item in sublist:
            output.append(item)
    return output


# textData = "My sentence is quite long, so you might have to hurry up"
# tokens = word_tokenize(textData.lower())
# text = Text(tokens)
# print(correctParticles(pos_tag(text)))
# PoS = dictIfy(correctParticles(pos_tag(text)))
# print(PoS)
# print(fuzzyFind(PoS, "VB"))
# print(reduceLevel(fuzzyFind(PoS, "VB")))
# print(multiSplit(textData, reduceLevel(fuzzyFind(PoS, "VB"))))
# print(tree2dict(treeIfy(correctParticles(pos_tag(text))))["S"])
# json.dump(tree2dict(treeIfy(correctParticles(pos_tag(text)))), sys.stdout, indent=2)

etiquette_excerpt = "I like jack, but I am a good guy."
tokens = word_tokenize(etiquette_excerpt.lower())
treeData = tree2dict(treeIfy(pos_tag(tokens)))
json.dump(treeData, sys.stdout, indent=2)
