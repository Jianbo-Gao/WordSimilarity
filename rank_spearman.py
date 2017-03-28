#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, csv, copy

from scipy import stats

from setting import *

def rank_spearman(wordpairs, filename):
    human_result=[]
    for wordpair in wordpairs:
        human_result.append(copy.deepcopy(wordpair[2]))

    results=[]
    for prefix in RESULT_PREFIXS:
        method_result=[]
        method_path=os.path.join(RESULT_DIR,prefix+filename)
        method_file=file(method_path,'rb')
        reader=csv.reader(method_file)
        for line in reader:
            method_result.append(copy.deepcopy(float(line[2])))
        method_file.close()

        method_type=prefix.split('/')[0]
        method_name=prefix.split('/')[1][:-1]
        method_data=filename.split('.')[0]
        method_spearman=stats.spearmanr(human_result, method_result)[0]
        results.append(copy.deepcopy([method_type,method_name,method_data,method_spearman]))

    return results
