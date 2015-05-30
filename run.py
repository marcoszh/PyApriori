# -*- coding: utf-8 -*-
__author__ = 'Marcos'

import apriori as ap
import sys
import csv
import time
import resource

def load_data():
    return [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'], ['I2', 'I3'], ['I1', 'I3'], ['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]


def load_large_data():
    array = []


    file_iter = open('INTEGRATED-DATASET.csv', 'rU')
    for line in file_iter:
        line = line.strip().rstrip(',')                         # Remove trailing comma
        items = line.split(',')
        items = sorted(items)
        #print items
        array.append(items)
    return array


def main(argv):
    #读取数据
    dataset = load_large_data()
    print dataset

    #寻找频繁项集
    timestart = time.clock()
    L, support = ap.apriori(dataset, 0.2)
    time_elapsed = (time.clock() - timestart)
    print '频繁项集有'
    print L

    #生成关联规则
    print '关联规则有'
    ap.printRules(L, support, 0.6)

    print '耗时：', time_elapsed, 's'

    print '内存：', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'byte'



if __name__ == '__main__':
    main(sys.argv)