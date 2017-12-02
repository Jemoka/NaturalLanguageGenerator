from nltk import word_tokenize
from nltk import RegexpTokenizer
from nltk import RegexpParser
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
    return [result[0]]+[makeString(tokenizer.tokenize(i)[1:])[1:] for i in result[1:]]


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

def nounPhrase(taggedSentence):
    NP = "NP: {<DT>?<JJ>*<NN>}"
    parser = RegexpParser(NP)
    result = parser.parse(taggedSentence)
    return result

def dictIfy(tuple):
    ds = []
    for x, y in tuple:
        ds.append({y: x})
    return join(ds)

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t for t in tree]}

def reduceLevel(array):
    output = []
    for sublist in array:
        for item in sublist:
            output.append(item)
    return output

textData = "I like to eat red fishes which ones lives in ocean deep?"
tokens = word_tokenize(textData.lower())
text = Text(tokens)
print(pos_tag(text))
PoS = dictIfy(pos_tag(text))
print(PoS)
print(fuzzyFind(PoS, "VB"))
print(reduceLevel(fuzzyFind(PoS, "VB")))
print(multiSplit(textData, reduceLevel(fuzzyFind(PoS, "VB"))))
print(tree2dict(nounPhrase(pos_tag(text)))["S"])
json.dump(tree2dict(nounPhrase(pos_tag(text))), sys.stdout, indent=2)
