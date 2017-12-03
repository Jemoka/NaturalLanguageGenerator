import io
import pickle

from nltk import pos_tag
from nltk.corpus import conll2000
from nltk.corpus import treebank

# tagged_corpus = [pos_tag(i) for i in treebank.sents()]
#
# with io.open('PoSDatabases/treebank.pos', 'wb') as fout:
#     pickle.dump(tagged_corpus, fout)
#
# tagged_corpus = [pos_tag(i) for i in conll2000.sents()]
#
# with io.open('PoSDatabases/conll2000.pos', 'wb') as fout:
#     pickle.dump(tagged_corpus, fout)
#
