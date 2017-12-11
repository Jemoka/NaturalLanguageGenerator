import time
start = time.time()
t0 = time.time()
print("Welcome to SentenceTrees version 0.1.0~Alpha")
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
import language_check
import json
import re
import sys
import random
import pickle
import ast
import os

t1 = time.time()
print("System initialized. Time spent:", t1-t0)

class SentenceTrees:
    def __init__(self, treeGrammar=None, taggerDir=['StanfordTagger/models/english-bidirectional-distsim.tagger', 'StanfordTagger/stanford-postagger.jar']):
        self.tagger = StanfordPOSTagger(taggerDir[0], taggerDir[1])
        self.lt = language_check.LanguageTool('en-US')
        if treeGrammar is None or type(treeGrammar) != str:
            with open ("grammar.exp.regexp", "r") as grammar:
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
            verb = str(VB[0])
        except (TypeError, IndexError):
            if VB == 0:
                verb = "do"
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
            tokens = word_tokenize(sentence)
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

    def __format(self, string):
        if string[0] == " ":
            string = string[1:]
        string = "%s%s" % (string[0].upper(), string[1:])
        errors = self.lt.check(string)
        return language_check.correct(string, errors) + ". "

    def __beConform(self, sbj):
        fNoun = None
        fNounType = None
        for i in reversed(self.tagger.tag(sbj)):
            if i[1] in ["NN", "NNS", "NNP", "NNPS", "PRP"]:
                fNoun = i[0]
                fNounType = i[1]
                break
        if fNoun is None:
            return "[fNoun]"
        if fNounType == "NN" or fNounType == "NNP":
            return "is"
        elif fNounType == "NNS" or fNounType == "NNPS":
            return "are"
        elif fNounType == "PRP":
            if fNoun.lower() == "you":
                return "are"
            elif fNoun.lower() == "i":
                return "am"
            elif fNoun.lower() == "he":
                return "is"
        return "[end]"

    def __sentIfy(self, array):
        uniquewords = []
        for word in array:
            if word not in uniquewords:
                uniquewords.append(word)

        positions = [uniquewords.index(word) for word in array]
        recreated = " ".join([uniquewords[i] for i in positions])

        return recreated

    def formSentence(self):
            verb = random.sample(self.vbList, 1)[0]
            useSbj = random.sample(self.bSentCpnts["SBJ"], 1)[0]
            useObj = random.sample(self.bSentCpnts["OBJ"], 1)[0]
            if verb in ["is", "are", "am"]:
                verb == self.__beConform(useSbj)
            NP = self.bSents[verb]
            sbj = []
            for i in useSbj:
                sbj.append(i)
                posAdj = self.mods.get(i)
                if posAdj:
                    posAdj = random.sample(posAdj, 1)[0]
                    index = sbj.index(i)
                    if index <= 0:
                        sbj = [posAdj]
                    else:
                        sbj.insert(index-1, posAdj)
            obt = []
            for e in useObj:
                obt.append(e)
                posAdj = self.mods.get(e)
                obj = ""
                if posAdj:
                    posAdj = random.sample(posAdj, 1)[0]
                    index = obt.index(e)
                    if index == 0:
                        obt = [posAdj]
                    else:
                        obt.insert(index-1, posAdj)

            vmod = self.mods.get(verb)
            if vmod is not None:
                vmod = random.sample(vmod, 1)[0]
                sentence = self.__sentIfy(sbj+[vmod]+[verb]+obt)
                return self.__format(sentence)
            else:
                sentence = self.__sentIfy(sbj+[verb]+obt)
                return self.__format(sentence)

def userInterface():
    print("Welcome to SentenceTrees Menu Interface")
    mode = ""
    while mode != "0":
        print("""
        ~SentenceTrees Menu~

        1 - Train Module
        2 - Load .pkl

        0 - Exit

        """)
        mode = input("CHOICE: ")
        if mode == "1":
            datasetDir = input("Training Corpus Directory: ").strip()
            savedFileDir = input("Packaged .plk Directory (will be created): ").strip()
            t0 = time.time()
            print("Loading dataset...")
            with open(datasetDir, 'r') as corpusFile:
                data = corpusFile.read()
            corpus = [i.encode('ascii', 'ignore').decode('ascii') for i in sent_tokenize(data)]
            t1 = time.time()
            print("Time spent:",t1-t0)
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
                if i < 99:
                    print(s.formSentence(), end="")
                else:
                    print(s.formSentence())
            t1 = time.time()
            print("Time spent:",t1-t0)

        elif mode == "2":
            savedFileDir = input("Packaged .pkl Directory: ").strip()
            t0 = time.time()
            print("Loading file...")
            with open(savedFileDir, "rb") as DF:
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

        elif mode == "0":
            print("Quitting...")

        print("\n")

    finish = time.time()
    print("Session finished, total time spent", finish-start)
    sys.exit()




try:
    mode = sys.argv[1]
except IndexError:
    print("Please supply a handle.")
    sys.exit()

if sys.argv[1] == "--r":
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
    print("Session finished, total time spent", finish-start)

elif sys.argv[1] == "--ui":
    userInterface()

elif sys.argv[1] == "--t":
    t0 = time.time()
    print("Loading dataset...")
    datasetDir = sys.argv[2]
    savedFileDir = sys.argv[3]
    with open(datasetDir, 'r') as corpusFile:
        data = corpusFile.read()
    corpus = [i.encode('ascii', 'ignore').decode('ascii').lower() for i in sent_tokenize(data)]
    t1 = time.time()
    print("Time spent:",t1-t0)
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
        if i < 99:
            print(s.formSentence(), end="")
        else:
            print(s.formSentence())
    t1 = time.time()
    print("Time spent:",t1-t0)
    finish = time.time()
    print("Session finished, total time spent", finish-start)

elif sys.argv[1] == "--eval":
    print("Welcome to SentenceTrees EVAL Tools version 0.2.0~Alpha")
    mode = ""
    while mode != "0":
        print("""
        ~EVAL Tools~

        1 - Form Sentence Tree
        2 - Edit Grammar
        3 - Pkl Obj Variable Return
        4 - Temp-train obj on sentence
        5 - Visualize Chunkstring
        6 - Open Frontend UI

        0 - Exit EVAL Tools

        """)

        mode = input("CHOICE: ")
        if mode == "1":
            sentence = input("Supply a sentence: ")
            print("You supplied:", sentence)
            print("Initializing object and tagger...")
            t0 = time.time()
            s = SentenceTrees()
            tagger = StanfordPOSTagger('StanfordTagger/models/english-bidirectional-distsim.tagger', 'StanfordTagger/stanford-postagger.jar')
            t1 = time.time()
            print("Time spent:",t1-t0)
            print("Forming sentence tree...")
            t0 = time.time()
            treeData = s._SentenceTrees__treeIfy(tagger.tag(word_tokenize(sentence)))
            print("Sentence tree:", treeData)
            t1 = time.time()
            print("Time spent:",t1-t0)
            t0 = time.time()
            print("Starting graph mainloop...")
            treeData.draw()
            print("Mainloop finished.")
            t1 = time.time()
            print("Time spent:",t1-t0)

        elif mode == "2":
            t0 = time.time()
            os.system("open "+"grammar.exp.regexp")
            t1 = time.time()
            print("Time spent:",t1-t0)

        elif mode == "3":
            path = input("Object .pkl Directory: ")
            t0 = time.time()
            print("Loading file...")
            with open(path.strip(), "rb") as DF:
                obj = pickle.loads(DF.read())
            t1 = time.time()
            print("Time spent:",t1-t0)
            t0 = time.time()
            print("Loading variables...")
            time.sleep(1)
            print("\n")
            print("obj.trees:", obj.trees)
            time.sleep(1)
            print("\n")
            print("obj.vblist:", obj.vbList)
            time.sleep(1)
            print("\n")
            print("obj.bSentCpnts:", obj.bSentCpnts)
            time.sleep(1)
            print("\n")
            print("obj.bSents:", obj.bSents)
            time.sleep(1)
            print("\n")
            print("obj.mods:", obj.mods)
            time.sleep(1)
            print("\n")
            t1 = time.time()
            print("Time spent:",t1-t0)

        elif mode == "4":
            sentence = input("Supply a sentence: ")
            print("You supplied:", sentence)
            t0 = time.time()
            print("Initializing object...")
            obj = SentenceTrees()
            t1 = time.time()
            print("Time spent:",t1-t0)
            print("Training...")
            t0 = time.time()
            obj.train([sentence.encode('ascii', 'ignore').decode('ascii')])
            t1 = time.time()
            print("Time spent:",t1-t0)
            t0 = time.time()
            print("Loading variables...")
            time.sleep(1)
            print("\n")
            print("obj.trees:", obj.trees)
            time.sleep(1)
            print("\n")
            print("obj.vblist:", obj.vbList)
            time.sleep(1)
            print("\n")
            print("obj.bSentCpnts:", obj.bSentCpnts)
            time.sleep(1)
            print("\n")
            print("obj.bSents:", obj.bSents)
            time.sleep(1)
            print("\n")
            print("obj.mods:", obj.mods)
            time.sleep(1)
            print("\n")
            t1 = time.time()
            print("Time spent:",t1-t0)

        elif mode == "5":
            sentence = input("Supply a chunkstring: ")
            print("Forming sentence tree...")
            treeData = eval(sentence)
            print("Sentence tree:", treeData)
            print("Time spent:",t1-t0)
            t0 = time.time()
            print("Starting graph mainloop...")
            treeData.draw()
            print("Mainloop finished.")
            t1 = time.time()
            print("Time spent:",t1-t0)

        elif mode == "6":
            print("\n")
            userInterface()

        elif mode == "0":
            print("Quitting...")

        else:
            print("Invalid mode supplied.")

    finish = time.time()
    print("Session finished, total time spent", finish-start)
    sys.exit()

else:
    print("Invalid handle supplied.")
