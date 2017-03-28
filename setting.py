#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

ROOT_DIR=os.path.dirname(os.path.abspath(sys.argv[0]))
RESULT_DIR=os.path.join(ROOT_DIR, "result")
WORDSIM353_DIR=os.path.join(ROOT_DIR, "wordsim353")

RESULT_PREFIXS=[
    "wordnet/path_", "wordnet/wup_", "wordnet/lch_",
    "wordnet/res_", "wordnet/jcn_", "wordnet/jcn_",
    "word2vec/word2vec_",
    "pagecount/webjaccard_", "pagecount/weboverlap_",
    "pagecount/webdice_", "pagecount/webpmi_"
    ]

RESULT_POSTFIXS=["set1.csv", "set2.csv"]


