#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models import word2vec

import os, csv

from setting import *

def sim_word2vec(wordpairs, filename):
    WORD2VEC_DIR=os.path.join(RESULT_DIR, "word2vec")

    resultfile=file(os.path.join(WORD2VEC_DIR,"word2vec_"+filename),'wb')
    resultwriter=csv.writer(resultfile)

    sentences = word2vec.Text8Corpus(os.path.join(ROOT_DIR,"text8","text8"))
    model = word2vec.Word2Vec(sentences)

    for wordpair in wordpairs:
        try:
            sim = model.similarity(wordpair[0], wordpair[1])
        except Exception, e:
            sim = -100
            print "word2vec: "+str(e)
        result=(wordpair[0], wordpair[1], sim)
        resultwriter.writerow(result)

    resultfile.close()
