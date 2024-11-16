from pathlib import Path
from random import randint
from time import time
from multiprocessing import Process,cpu_count
from math import ceil

dataNumber=10**2
input1=Path(__file__).parent/'input1.txt'
input2=Path(__file__).parent/'input2.txt'
output1=Path(__file__).parent/'output1.txt'
output2=Path(__file__).parent/'output2.txt'

def makeData():
          with open(input1,'w') as file:
                    for i in range(dataNumber):
                              file.write(str(i))
                              file.write(',')
          with open(input2,'w') as file:
                    for i in range(dataNumber):
                              file.write(str(randint(0,dataNumber*10)))
                              file.write(',')
def input():
          with open(input1,'r') as file:
                    list1=file.read()
                    list1=list1.split(',')  
          with open(input2,'r') as file:
                    list2=file.read()
                    list2=list2.split(',') 
          return list1,list2
                              
def compare(originallist,comparelist,output):
          with open(output,'a') as file:
                    for x in comparelist:
                              if x in originallist:
                                        file.write(str(x))
                                        file.write(',')

def linearCompare(originallist,comparelist):
          t1=time()
          open(output1,'w')
          compare(originallist,comparelist,output1)
          t2=time()
          print("Singlecore match time: ",t2-t1)

def multiCoreCompareProcess(originallist,comparelist):
          t1=time()
          open(output2,'w')
          numCpu=cpu_count()
          data=[]
          l=len(comparelist)
          for i in range(0,len(comparelist),ceil(l/numCpu)):
                    data.append(comparelist[i:i+ceil(l/numCpu)])
          for d in data:
                    Process(target=compare,args=(originallist,d,output2,)).start()
          t2=time()
          print("Multicore match time: ",t2-t1)


def main():
          makeData()
          originallist,comparelist=input()
          linearCompare(originallist,comparelist)
          multiCoreCompareProcess(originallist,comparelist)

if __name__=='__main__':
          main()