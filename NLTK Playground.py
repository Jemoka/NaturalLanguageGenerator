from nltk.corpus import treebank
from nltk.corpus import wordnet as wn
from nltk import BigramTagger
from nltk import UnigramTagger
from nltk import TrigramTagger
from nltk import DefaultTagger
from nltk.tag.stanford import StanfordPOSTagger
from nltk import chunk
from nltk.chunk.util import tagstr2tree
from nltk import word_tokenize
from nltk import RegexpTokenizer
from nltk import RegexpParser
from nltk.draw.util import CanvasFrame
from nltk.draw.tree import TreeView
from nltk import pos_tag
from nltk import Text
from nltk import Tree
from nltk import CFG
import json
import re
import sys
import random


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
    LIST:
    {(<JJ>*<PRP|PRP$|WP|WP$|NN.*|JJ|RB><,>?)+(<CC><JJ>*<PRP|PRP$|WP|WP$|NN.*|JJ|RB>)}
    NRC:
    {<,><WDT><.*>*<,>}
    INF:
    {<TO><VB|VBG|VBD|VBN|VBP|VBZ>}
    NP:
    {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN.*|LS>+<.*>*}
    {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN.*><CC>*<PRP|PRP$|WP|WP$|NN.*>+}
    {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN.*|LS.*>+ <IN>?}
    {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN.*|LS.*>+ <IN>?}
    {<DT>?<RB>*<JJ>*<LIST>+}
    }<,>{
    }<.>{
    }<RB>*<VB.*>{
    VP:
    {<RB>*<VB.*><.*>*}
    }<.>{
    PP:
    {<IN><NP>}
    }<,>{
    """
    NPChunker = RegexpParser(grammar)
    return NPChunker.parse(taggedSentence)


def dictIfy(tuples):
    ds = []
    for i in tuples:
        tupleList = list(i)
        ds.append({tupleList[1]: tupleList[0]})
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


def findVP(sentence, index=0):
    VP = sentence[index]
    currentIndex = index
    while type(VP) != dict:
        VP = findVP(sentence, index=currentIndex + 1)
    while VP.get("VP") is None:
        VP = findVP(sentence, index=currentIndex + 1)
    return VP


def findNode(tree, nodeName):
    leaves = []
    for subtree in tree.subtrees():
        if subtree.label() == nodeName:
            leaves.append(subtree.leaves())
    return leaves


def findVerb(array):
    for i in array:
        if type(i) != tuple:
            pass
        if any(i[1] in s for s in ["VB", "VBG", "VBP", "VBD", "VBD", "VBN", "VBZ"]):
            return (i[0], i[1])
    return 0

def simplify(array):
    data = array
    modifiers = {}
    for key, value in data:
        index = data.index((key, value))
        if any(value==s for s in ["JJ", "RB", "DT"]):
            try:
                searchArray = [["RB","RB"], ["JJ", "NN"], ["RB", "JJ"], ["JJ", "JJ"], ["RB", "RB"], ["JJ", "NNS"], ["JJ", "NNP"], ["JJ", "NNPS"]]
                if any([value, data[index+1][1]]==e for e in searchArray):
                    newd = {data[index+1]: (key, value)}
                    modifiers.update(newd)
            except IndexError:
                pass
            data = [x for x in data if x != (key, value)]
    return (data, modifiers)


def parse(tree):
    print(tree)
    NP = findNode(tree, "NP")
    VB = findVerb(reduceLevel(findNode(tree, "VP")))
    sNP = []
    mod = {}
    for i in NP:
        sNP.append(simplify(i)[0])
        mod.update(simplify(i)[1])
    nouns = []
    for i in sNP:
        nl = []
        for key, value in i:
            nl.append(key)
        nouns.append(nl)

    n = {"SBJ": nouns[0], "OBJ": nouns[1]}
    verb = wn.synsets(VB[0])[0].lemmas()[0].name()
    modifiers = {}
    for key, value in mod.items():
        modifiers.update({key[0]:value[0]})
    return n, verb, modifiers

def update(dictionary, key, value):
    if dictionary.get(key) is None:
        dictionary[key] = [value]
    else:
        dictionary[key] = [dictionary.get(key)] + [value]

tagger = StanfordPOSTagger('StanfordTagger/models/english-bidirectional-distsim.tagger', 'StanfordTagger/stanford-postagger.jar')
etiquette_excerpt = "The quick brown fox jumped over the lazy dog and funny cat."
tokens = word_tokenize(etiquette_excerpt.lower())
treeData = treeIfy(tagger.tag(tokens))
json.dump(tree2dict(treeData), sys.stdout, indent=2)
print("\n")
# TreeView(treeData)._cframe.print_to_file('/Users/liujack/Desktop/output.ps')
treeDict = tree2dict(treeData)
nouns, verb, mods = parse(treeData)

baseSentenceComponents = nouns
print({verb:nouns})
baseSentences = {verb:nouns}
modifiers = mods
verbs = [verb]

etiquette_excerpt = "Susan taught me English on Sunday."
tokens = word_tokenize(etiquette_excerpt.lower())
treeData = treeIfy(tagger.tag(tokens))
json.dump(tree2dict(treeData), sys.stdout, indent=2)
print("\n")
treeDict = tree2dict(treeData)
nouns, verb, mods = parse(treeData)

update(baseSentenceComponents, "SBJ", nouns["SBJ"])
update(baseSentenceComponents, "OBJ", nouns["OBJ"])
update(baseSentences, verb, nouns)
for key, value in mods.items():
    update(modifiers, key, value)
verbs = verbs + [verb]

print(baseSentenceComponents, baseSentences, modifiers, verbs)

useVerb = random.sample(verbs, 1)[0]
useSbj = random.sample(baseSentenceComponents["SBJ"], 1)[0]
useObj = random.sample(baseSentenceComponents["OBJ"], 1)[0]
NP = baseSentences[useVerb]
print(useSbj, useVerb, useObj)
