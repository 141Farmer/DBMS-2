from itertools import combinations
from pathlib import Path
from csv import reader

def countSingleItems(transactions,minSupport):
          itemCounts={}
          for transaction in transactions:
                    for item in transaction:
                              itemCounts[item]=itemCounts.get(item,0)+1
          
          return {frozenset([item]) for item,count in itemCounts.items() if count>=minSupport}


def generateCandidates(currentItemsets,length):
          candidates=set()
          for itemset1 in currentItemsets:
                    for itemset2 in currentItemsets:
                              unionItemset=itemset1|itemset2
                              if len(unionItemset)==length:
                                        candidates.add(unionItemset)
          return candidates


def countCandidates(transactions,candidateItemsets,minSupport):
          itemsetCounts={itemset: 0 for itemset in candidateItemsets}
          for transaction in transactions:
                    for itemset in candidateItemsets:
                              if itemset.issubset(transaction):
                                        itemsetCounts[itemset]+=1
          return {itemset for itemset,count in itemsetCounts.items() if count>=minSupport}


def apriori(transactions,minSupport):
          frequentItemsets=[]
          currentItemsets=countSingleItems(transactions,minSupport)
          frequentItemsets.extend(currentItemsets)

          length=2
          while currentItemsets:
                    candidateItemsets=generateCandidates(currentItemsets,length)
                    currentItemsets=countCandidates(transactions,candidateItemsets,minSupport)
                    frequentItemsets.extend(currentItemsets)
                    length+=1

          return frequentItemsets


def main():
          transactions=[]
          with open(Path(__file__).parent/'input.csv','r') as file:
                    data=reader(file)
                    for d in data:
                              transactions.append(set(d[1:]))
          
          minSupport=2
          frequentItemsets=apriori(transactions,minSupport)
          for itemset in frequentItemsets:
                    print(*itemset)

if __name__=='__main__':
          main()
