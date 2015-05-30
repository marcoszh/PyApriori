#-*- coding:utf-8 - *-
__author__ = 'Marcos'
 

def findAllItem(dataset):
    """找到所有出现过的项"""
    items = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in items:
                items.append([item])
    items.sort()
    #frozenset because it will be a ket of a dictionary.
    return map(frozenset, items)
 
 
def dropItem(dataset, candidates, min_support):
    """淘汰掉不够min_support的项"""
    counter = {}
    for dataitem in dataset:
        for can in candidates:
            if can.issubset(dataitem):
                counter.setdefault(can, 0)
                counter[can] += 1
 
    num_items = float(len(dataset))
    newcandidates = []
    support_data = {}
    for key in counter:
        support = counter[key] / num_items
        if support >= min_support:
            newcandidates.insert(0, key)
        support_data[key] = support
    return newcandidates, support_data
 
 
def aprioriGen(freq_sets, k):
    """进行第k步合并"""
    retList = []
    lenLk = len(freq_sets)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(freq_sets[i] | freq_sets[j])
    return retList
 
 
def apriori(dataset, minsupport=0.5):
    """算法主体"""
    C1 = findAllItem(dataset)
    D = map(set, dataset)
    L1, support_data = dropItem(D, C1, minsupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = dropItem(D, Ck, minsupport)
        support_data.update(supK)
        L.append(Lk)
        k += 1
 
    return L, support_data

def printRules(L, support_data, min_confidence=0.7):
    """生成关联规则
    L: 频繁项集
    support_data: L对应的支持度
    min_confidence: 最小置信度
    """
    rules = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            #print "freqSet", freqSet, 'H1', H1
            if (i > 1):
                rules_from_conseq(freqSet, H1, support_data, rules, min_confidence)
            else:
                calc_confidence(freqSet, H1, support_data, rules, min_confidence)
    return rules


def calc_confidence(freqSet, H, support_data, rules, min_confidence=0.7):
    """计算置信度"""
    pruned_H = []
    for conseq in H:
        conf = support_data[freqSet] / support_data[freqSet - conseq]
        if conf >= min_confidence:
            print freqSet - conseq, '--->', conseq, 'conf:', conf
            rules.append((freqSet - conseq, conseq, conf))
            pruned_H.append(conseq)
    return pruned_H


def rules_from_conseq(freqSet, H, support_data, rules, min_confidence=0.5):
    """得到推断"""
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(freqSet, Hmp1,  support_data, rules, min_confidence)
        if len(Hmp1) > 1:
            rules_from_conseq(freqSet, Hmp1, support_data, rules, min_confidence)
