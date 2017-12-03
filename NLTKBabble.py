from nltk.corpus import treebank
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


class NLGBabble(object):
    def __init__(self, data):
        self.data = []
        self.parsed = []
        self.trees = []
        for i in data:
            self.data.append(i)
            tokens = word_tokenize(i.lower())
            self.tokens.append(tokens)
            tree = self.__treeIfy(pos_tag(tokens))
            self.trees.append(tree)
            self.tDicts.append(self.__dictIfy(tree))

    def __dictIfy(self, t):
            return {t.label(): [self.__dictIfy(i) if isinstance(i, Tree) else i for i in t]}

    def __treeIfy(taggedSentence):
        grammar = """
        LIST:
        {(<JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS><,>?)+(<CC><JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS>)}
        }{
        INF:
        {<TO><VB|VBG|VBD|VBN|VBP|VBZ>}
        NP:
        {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS>+}
        {<DT>?<RB>*<JJ>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS><CC>*<PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS>+}
        {<DT>?<RB>*<JJ>* <PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS.*>+ <IN>?}
        {<DT>?<RB>*<JJ>* <PRP|PRP$|WP|WP$|NN|NNS|NNP|NNPS.*>+ <IN>?}
        {<DT>?<RB>*<JJ>* <LIST>+}
        VP:
        {<RB>*<VB|VBG|VBD|VBN|VBP|VBZ><.*>*}
        }<.>{
        PP:
        {<IN><NP>}
        """
        NPChunker = RegexpParser(grammar)
        return NPChunker.parse(taggedSentence)
