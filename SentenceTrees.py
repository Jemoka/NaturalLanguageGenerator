import time
start = time.time()
t0 = time.time()
print("Welcome to SentenceTrees version 0.0.4.1~Beta")
print("Initializing...")

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
import progressbar
import json
import re
import sys
import random
import pickle
import ast
import os

t1 = time.time()
print("System initialized. Time spent:", t1-t0)

class SentenceTrees(object):
    def __init__(self, treeGrammar=None, taggerDir=['StanfordTagger/models/english-bidirectional-distsim.tagger', 'StanfordTagger/stanford-postagger.jar']):
        self.tagger = StanfordPOSTagger(taggerDir[0], taggerDir[1])
        if treeGrammar is None or type(treeGrammar) != str:
            with open ("grammar.regexp", "r") as grammar:
                self.grammar = grammar.read()
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
        try:
            n = {"SBJ": nouns[0], "OBJ": nouns[1]}
        except IndexError:
            return None
        try:
            verb = wn.synsets(VB[0])[0].lemmas()[0].name()
            if verb == "be":
                verb = str(VB[0])
        except (TypeError, IndexError):
            if VB == 0:
                verb = "??"
            else:
                verb = str(VB[0])
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
        print("Initializing training cycle for target...")
        loss = 0
        bar = progressbar.ProgressBar()
        print("Training in progress...")
        for sentence in bar(data):
            tokens = word_tokenize(sentence.lower())
            sentenceTree = self.__treeIfy(self.tagger.tag(tokens))
            self.trees.append(sentenceTree)
            if self.__parse(sentenceTree) is None:
                loss += 1
                pass
            else:
                nouns, verb, mods = self.__parse(sentenceTree)
                self.__update(self.bSentCpnts, "SBJ", nouns["SBJ"])
                self.__update(self.bSentCpnts, "OBJ", nouns["OBJ"])
                self.__update(self.bSents, verb, nouns)
                for key, value in mods.items():
                    self.__update(self.mods, key, value)
                    self.vbList = self.vbList + [verb]
        print("Training target finished, dataCount =",len(data),"dataloss =", loss)

    def __formatter(self, string):
        if string[0] == " ":
            string = string[1:]
        string = "%s%s" % (string[0].upper(), string[1:])
        return string

    def formSentence(self):
            verb = random.sample(self.vbList, 1)[0]
            useSbj = random.sample(self.bSentCpnts["SBJ"], 1)[0]
            useObj = random.sample(self.bSentCpnts["OBJ"], 1)[0]
            NP = self.bSents[verb]
            sbj = ''
            for i in useSbj:
                posAdj = self.mods.get(i)
                sbj = ""
                if posAdj:
                    posAdj = random.sample(posAdj, 1)[0]
                    index = useSbj.index(i)
                    if index == 0:
                        sbj = posAdj
                    else:
                        sbj = sbj+" "+posAdj
                sbj = sbj+" "+i
            obj = ''
            for e in useObj:
                posAdj = self.mods.get(e)
                obj = ""
                if posAdj:
                    posAdj = random.sample(posAdj, 1)[0]
                    index = useObj.index(e)
                    if index == 0:
                        obj = posAdj
                    else:
                        obj = obj+" "+posAdj
                obj = obj+" "+e
            vmod = self.mods.get(verb)
            if vmod is not None:
                vmod = random.sample(vmod, 1)[0]
                sentence = sbj+" "+vmod+" "+verb+obj+"."+" "
                return self.__formatter(sentence)
            else:
                sentence = sbj+" "+verb+obj+"."+" "
                return self.__formatter(sentence)


if sys.argv[1] == "-r":
    t0 = time.time()
    print("Loading file...")
    with open(sys.argv[2], "rb") as DF:
        obj = pickle.loads(DF.read())
    t1 = time.time()
    print("Time spent:",t1-t0)
    print("Forming 100 sentences...")
    t0 = time.time()
    bar = progressbar.ProgressBar()
    for i in bar(range(0,100)):
        if i < 100:
            print(obj.formSentence(), end="")
        else:
            print(obj.formSentence())
    t1 = time.time()
    print(obj.formSentence())
    t1 = time.time()
    print("Time spent:",t1-t0)
    finish = time.time()
    print("Job finished, total time spent", finish-start)
    sys.exit()

if sys.argv[1] == "-t":
    print("Loading dataset...")
    datasetDir = sys.argv[2]
    savedFileDir = sys.argv[3]
    with open(datasetDir, 'r') as corpusFile:
        data = corpusFile.read()
    corpus = [i.encode('ascii', 'ignore').decode('ascii') for i in sent_tokenize(data)]
    print("Training...")
    s = SentenceTrees()
    t0 = time.time()
    s.train(corpus)
    t1 = time.time()
    print("Time spent:",t1-t0)
    print("Pickling...")
    t0 = time.time()
    with open(savedFileDir, 'wb') as output:
        pickle.dump(s, output, pickle.HIGHEST_PROTOCOL)
    t1 = time.time()
    print("Time spent:",t1-t0)
    print("Forming 100 sentences...")
    t0 = time.time()
    for i in range(0,100):
        if i < 100:
            print(s.formSentence(), end="")
        else:
            print(s.formSentence())
    t1 = time.time()
    print("Time spent:",t1-t0)
    finish = time.time()
    print("Job finished, total time spent", finish-start)
