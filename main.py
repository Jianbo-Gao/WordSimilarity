#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, csv, copy

from setting import *
from sim_wordnet import sim_wordnet
from sim_word2vec import sim_word2vec
from sim_pagecount import sim_pagecount
from rank_spearman import rank_spearman

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

    rank_file=file(os.path.join(RESULT_DIR,"rank.csv"),'wb')
    rank_writer=csv.writer(rank_file)

    for i in xrange(len(filenames)):
        reader=readers[i]
        FIRST_LINE_FLAG=True
        wordpairs=[]

        for line in reader:
            if FIRST_LINE_FLAG:
                FIRST_LINE_FLAG=False
                continue
            wordpairs.append((copy.deepcopy(line[0]), copy.deepcopy(line[1]), copy.deepcopy(float(line[2]))))

        sim_wordnet(wordpairs, filenames[i])
        sim_word2vec(wordpairs, filenames[i])
        sim_pagecount(wordpairs, filenames[i])
        rank_results=rank_spearman(wordpairs, filenames[i])
        rank_writer.writerows(rank_results)

    for csvfile in files:
        csvfile.close()
    rank_file.close()

if __name__ == '__main__':
    main()
