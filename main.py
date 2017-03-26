#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, csv, copy

from setting import *
from sim_wordnet import sim_wordnet
from sim_word2vec import sim_word2vec
from sim_pagecount import sim_pagecount

def main():
    set1file=file(os.path.join(WORDSIM353_DIR,"set1.csv"), 'rb')
    set1reader=csv.reader(set1file)

    set2file=file(os.path.join(WORDSIM353_DIR, "set2.csv"), 'rb')
    set2reader=csv.reader(set2file)

    combinedfile=file(os.path.join(WORDSIM353_DIR, "combined.csv"), 'rb')
    combinedreader=csv.reader(combinedfile)

    filenames=["set1.csv", "set2.csv", "combined.csv"]
    files=[set1file, set2file, combinedfile]
    readers=[set1reader, set2reader, combinedreader]

    for i in xrange(len(filenames)):
        reader=readers[i]
        FIRST_LINE_FLAG=True
        wordpairs=[]

        for line in reader:
            if FIRST_LINE_FLAG:
                FIRST_LINE_FLAG=False
                continue
            wordpairs.append((copy.deepcopy(line[0]), copy.deepcopy(line[1]), copy.deepcopy(line[2])))

        sim_wordnet(wordpairs, filenames[i])
        sim_word2vec(wordpairs, filenames[i])
        sim_pagecount(wordpairs, filenames[i])

    for csvfile in files:
        csvfile.close()

if __name__ == '__main__':
    main()
