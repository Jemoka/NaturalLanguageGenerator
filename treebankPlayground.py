from nltk.corpus import treebank_chunk
from nltk import Tree
from nltk import chunk
import nltk.corpus, nltk.tag

def conll_tag_chunks(chunk_sents):
    tag_sents = [nltk.chunk.tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in chunk_tags] for chunk_tags in tag_sents]

def ubt_conll_chunk_accuracy(train_sents, test_sents):
    train_chunks = conll_tag_chunks(train_sents)
    test_chunks = conll_tag_chunks(test_sents)

    u_chunker = nltk.tag.UnigramTagger(train_chunks)
    print('u:', nltk.tag.accuracy(u_chunker, test_chunks))

    ub_chunker = nltk.tag.BigramTagger(train_chunks, backoff=u_chunker)
    print('ub:', nltk.tag.accuracy(ub_chunker, test_chunks))

    ubt_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=ub_chunker)
    print('ubt:', nltk.tag.accuracy(ubt_chunker, test_chunks))

    ut_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=u_chunker)
    print('ut:', nltk.tag.accuracy(ut_chunker, test_chunks))

    utb_chunker = nltk.tag.BigramTagger(train_chunks, backoff=ut_chunker)
    print('utb:', nltk.tag.accuracy(utb_chunker, test_chunks))

# treebank chunking accuracy test
treebank_sents = nltk.corpus.treebank_chunk.chunked_sents()
print(treebank_sents)
