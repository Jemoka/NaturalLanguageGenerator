from nltk.corpus import treebank
from nltk.corpus import wordnet as wn
from nltk.tag.stanford import StanfordPOSTagger
from nltk import chunk
from nltk.chunk.util import tagstr2tree
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
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
import time

class SentenceTrees(object):
    def __init__(self, treeGrammar=None, taggerDir=['StanfordTagger/models/english-bidirectional-distsim.tagger', 'StanfordTagger/stanford-postagger.jar']):
        self.tagger = StanfordPOSTagger(taggerDir[0], taggerDir[1])
        if treeGrammar is None or type(treeGrammar) != str:
            self.grammar = """
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
        else:
            self.grammar = treeGrammar
        self.trees = []
        self.vbList = []
        self.bSentCpnts = {}
        self.bSents = {}
        self.mods = {}

    @staticmethod
    def __reduceLevel(array):
        output = []
        for sublist in array:
            for item in sublist:
                output.append(item)
        return output

    @staticmethod
    def __findNode(tree, nodeName):
        leaves = []
        for subtree in tree.subtrees():
            if subtree.label() == nodeName:
                leaves.append(subtree.leaves())
        return leaves

    @staticmethod
    def __findVerb(array):
        for i in array:
            if type(i) != tuple:
                pass
            if any(i[1] in s for s in ["VB", "VBG", "VBP", "VBD", "VBD", "VBN", "VBZ"]):
                return (i[0], i[1])
        return 0

    @staticmethod
    def __simplify(array):
        data = array
        modifiers = {}
        for key, value in data:
            try:
                index = data.index((key, value))
            except ValueError:
                pass
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


    def __parse(self, tree):
        NP = self.__findNode(tree, "NP")
        VB = self.__findVerb(self.__reduceLevel(self.__findNode(tree, "VP")))
        sNP = []
        mod = {}
        for i in NP:
            sNP.append(self.__simplify(i)[0])
            mod.update(self.__simplify(i)[1])
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

    def __treeIfy(self, taggedSentence):
        NPChunker = RegexpParser(self.grammar)
        return NPChunker.parse(taggedSentence)

    @staticmethod
    def __update(dictionary, key, value):
        if dictionary.get(key) is None:
            dictionary[key] = [value]
        else:
            dictionary[key] = dictionary.get(key) + [value]

    def train(self, data):
        for sentence in data:
            tokens = word_tokenize(sentence.lower())
            sentenceTree = self.__treeIfy(self.tagger.tag(tokens))
            self.trees.append(sentenceTree)
            nouns, verb, mods = self.__parse(sentenceTree)
            self.__update(self.bSentCpnts, "SBJ", nouns["SBJ"])
            self.__update(self.bSentCpnts, "OBJ", nouns["OBJ"])
            self.__update(self.bSents, verb, nouns)
            for key, value in mods.items():
                self.__update(self.mods, key, value)
            self.vbList = self.vbList + [verb]

    def formSentence(self):
            verb = random.sample(self.vbList, 1)[0]
            useSbj = random.sample(self.bSentCpnts["SBJ"], 1)[0]
            useObj = random.sample(self.bSentCpnts["OBJ"], 1)[0]
            NP = self.bSents[verb]
            sbj = ''
            for i in useSbj:
                sbj = sbj+" "+i
            obj = ''
            for e in useObj:
                obj = obj+" "+e
            return sbj+" "+verb+obj+"."


s = SentenceTrees()
t0 = time.time()
philosophy = """
Historically, "philosophy" encompassed any body of knowledge. From the time of Ancient Greek philosopher Aristotle to the 19th century, "natural philosophy" encompassed astronomy, medicine, and physics. For example, Newton's 1687 Mathematical Principles of Natural Philosophy later became classified as a book of physics. In the 19th century, the growth of modern research universities led academic philosophy and other disciplines to professionalize and specialize. In the modern era, some investigations that were traditionally part of philosophy became separate academic disciplines, including psychology, sociology, linguistics, and economics.
"""
s.train(sent_tokenize(philosophy))
t1 = time.time()
print(t1-t0)
t0 = time.time()
print(s.formSentence())
t1 = time.time()
print(t1-t0)
