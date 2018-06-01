#Association Rule: Frequent Itemset (Pairs and Triples)

import operator
import itertools

s = 100; cnt = 0 
itemcounter = []  
mapInd = []

fn = "data/browsing.txt"

with open(fn, "r") as file:
    for f in file:
        cnt += 1
        for i in set(f.split()):
            if i not in mapInd:
                mapInd.append(i)
                itemcounter.append(1)
            else:
                indexItem = mapInd.index(i)
                count = itemcounter[indexItem]
                count += 1
                itemcounter[indexItem] = count

freqSet = [mapInd.index(ind) for ind in mapInd if itemcounter[mapInd.index(ind)] >= s]
freqSet.sort()

candItems = {}
for item in itertools.combinations(sorted(freqSet),2):
    candItems[item] = 0   

with open(fn, "r") as file:
    for f in file:
        dat  = sorted([mapInd.index(item) for item in set(f.split())])
        for it in itertools.combinations(dat,2):
            if it in candItems:
                count =candItems[it]
                count += 1
                candItems[it] = count

freqSet2 = [pair for pair,thres in candItems.items() if thres >= s]
freqSet2.sort()

candItemsIII = {}
tripleItems = []
for fs in freqSet2:
    for i in [y for y in freqSet2 if y[0] == fs[1]]:
        tripleItems.append( (fs[0],fs[1],i[1]) )
      
for tri in tripleItems:
    flg = True
    for itr in itertools.combinations(tri,2):
        if itr not in freqSet2:
            flg = False
            break
    if flg:
        candItemsIII[tri] = 0
     
with open(fn, "r") as file:
    for f in file:
        fpr = sorted([mapInd.index(l) for l in set(f.split())])
        for fpr_items in itertools.combinations(fpr,3):
            if fpr_items in candItemsIII:
                tripleCount = candItemsIII[fpr_items] 
                tripleCount = tripleCount +1
                candItemsIII[fpr_items] = tripleCount
 
freqSet3 = [pair3 for pair3,thres in candItemsIII.items() if thres >= s]
freqSet3.sort()     

def Compute_Conf(a,b):
    prob_ab = 0
    ab = set(a).union(set(b))
    if len(ab) == 2:
        prob_ab = candItems[tuple(sorted(ab))]
    elif len(ab) == 3:
        prob_ab = candItemsIII[tuple(sorted(ab))]
    prob_a = 0
    if len(a) == 1:
        prob_a = itemcounter[a[0]]
    elif len(a) == 2:
        prob_a = candItems[tuple(sorted(a))]
    if prob_ab > prob_a:
        print(a,b,ab)
        print(prob_ab, prob_a, prob_ab/prob_a)
    return(round(prob_ab/prob_a,4))


# Q2 (d)
def Pair_Items():
    ruleII = {}
    for itempairs in freqSet2:
        ruleII[itempairs]=Compute_Conf((itempairs[0],),(itempairs[1],))
        ruleII[(itempairs[1],itempairs[0])] = Compute_Conf((itempairs[1],),(itempairs[0],))
    candPairs = sorted(ruleII.items(), key = operator.itemgetter(1))
    candPairs.reverse()
    candPr = ["%s -> %s - %s" % (mapInd[rule[0][0]],mapInd[rule[0][1]],rule[1]) for rule in candPairs[0:5]]
    print ("\n".join(candPr))

# Q2 (e)
def Triple_Items():
    ruleIII = {}
    for itempairs in freqSet3:
        for fset in itertools.combinations(itempairs,2):
            foo = tuple(set(itempairs).difference(set(fset)))
            ruleIII[(fset,foo)] = Compute_Conf(fset,foo)

    candTriples = sorted(ruleIII.items(), key = operator.itemgetter(1))
    candTriples.reverse()
    candTr = ["{%s,%s} -> %s - %s" % (mapInd[rule[0][0][0]],mapInd[rule[0][0][1]],mapInd[rule[0][1][0]], rule[1]) for rule in candTriples[0:5]]
    print ("\n".join(candTr))

#Answers
Pair_Items()
Triple_Items()

    
