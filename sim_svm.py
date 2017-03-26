#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, csv

from sklearn import preprocessing, svm, linear_mode
from numpy import *

from setting import *

def sim_svm(wordpair, filename):
    prefixs=[
    "wordnet/path_", "wordnet/wup_", "wordnet/lch_",
    "wordnet/res_", "wordnet/jcn_", "wordnet/jcn_",
    "word2vec/word2vec_",
    "pagecount/webjaccard_", "pagecount/weboverlap_",
    "pagecount/webdice_", "pagecount/webpmi_"
    ]
    postfixs=["set1.csv", "sec2.csv"]


