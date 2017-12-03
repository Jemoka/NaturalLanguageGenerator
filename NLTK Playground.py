from nltk.corpus import treebank
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
    LIST:
    {(<JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS><,>?)+(<CC><JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS>)}
    INF:
    {<TO><VB|VBG|VBD|VBN|VBP|VBZ>}
    NP:
    {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS|LS>+<.*>*}
    {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS><CC>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS>+}
    {<DT>?<RB>*<JJ>* <PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS|LS.*>+ <IN>?}
    {<DT>?<RB>*<JJ>* <PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS|LS.*>+ <IN>?}
    {<DT>?<RB>*<JJ>* <LIST>+}
    }<,>{
    }<RB>*<VB|VBG|VBD|VBN|VBP|VBZ>{
    VP:
    {<RB>*<VB|VBG|VBD|VBN|VBP|VBZ><.*>*}
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
    for key, value in data:
        if any(value==s for s in ["JJ", "RB", "DT"]):
            data = [x for x in data if x != (key, value)]
    return data


def strip(tree):
    NP = findNode(tree, "NP")
    VB = findVerb(reduceLevel(findNode(tree, "VP")))
    print(NP, VB)
    sNP = []
    for i in NP:
        sNP.append(simplify(i))
    print(sNP, VB)


tagger = StanfordPOSTagger('StanfordTagger/models/english-bidirectional-distsim.tagger', 'StanfordTagger/stanford-postagger.jar')
etiquette_excerpt = "On Wendsdays, Susan comes to teach me English."
tokens = word_tokenize(etiquette_excerpt.lower())
treeData = treeIfy(tagger.tag(tokens))
print(treeData)
json.dump(tree2dict(treeData), sys.stdout, indent=2)
TreeView(treeData)._cframe.print_to_file('/Users/liujack/Desktop/output.ps')
treeDict = tree2dict(treeData)
print(strip(treeData))
