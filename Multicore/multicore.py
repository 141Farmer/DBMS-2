from pathlib import Path
from random import randint
from time import time
from multiprocessing import Process,Pool,cpu_count
from concurrent.futures import ProcessPoolExecutor
from math import ceil

dataNumber=3*10**4
input1=Path(__file__).parent/'input1.txt'
input2=Path(__file__).parent/'input2.txt'
output1=Path(__file__).parent/'output1.txt'
output2=Path(__file__).parent/'output2.txt'
output3=Path(__file__).parent/'output3.txt'
output4=Path(__file__).parent/'output4.txt'
numCpu=cpu_count()


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
                              
def compare(args):
          originallist,comparelist,output=args
          with open(output,'a') as file:
                    for x in comparelist:
                              if x in originallist:
                                        file.write(str(x))
                                        file.write(',')

def linearCompare(originallist,comparelist):
          t1=time()
          open(output1,'w')
          args=originallist,comparelist,output1
          compare(args)
          t2=time()
          print("Singlecore match time: ",t2-t1)

def multiCoreCompareProcess(originallist,comparelist):
          t1=time()
          open(output2,'w')
          data=[]
          l=len(comparelist)
          for i in range(0,len(comparelist),ceil(l/numCpu)):
                    data.append(comparelist[i:i+ceil(l/numCpu)])
          processes=[]
          for d in data:
                    args=originallist,d,output2
                    p=Process(target=compare,args=(args,))
                    processes.append(p)
                    p.start()
          for p in processes:
                    p.join()
          
          t2=time()
          print("MulticoreProcess match time: ",t2-t1)

def multiCoreComparePool(originallist,comparelist):
          t1=time()
          open(output3,'w')
          data=[]
          l=len(comparelist)
          for i in range(0,len(comparelist),ceil(l/numCpu)):
                    data.append(comparelist[i:i+ceil(l/numCpu)])

          args=[(originallist,chunk,output3) for chunk in data]

          with Pool(processes=numCpu) as pool:
                    pool.map(compare,args)
          
          pool.close()
          t2=time()
          print("MulticorePool match time: ",t2-t1)




def multiCoreCompareProcessPoolExecutor(originallist,comparelist):
          t1=time()
          open(output4,'w')
          data=[]
          l=len(comparelist)
          for i in range(0,len(comparelist),ceil(l/numCpu)):
                    data.append(comparelist[i:i+ceil(l/numCpu)])

          args=[(originallist,chunk,output3) for chunk in data]

          with ProcessPoolExecutor(numCpu) as pool:
                    pool.map(compare,args)
          
          t2=time()
          print("MulticoreProcessPoolExecutor match time: ",t2-t1)

def main():
          makeData()
          originallist,comparelist=input()
          linearCompare(originallist,comparelist)
          multiCoreCompareProcess(originallist,comparelist)
          multiCoreComparePool(originallist,comparelist)
          multiCoreCompareProcessPoolExecutor(originallist,comparelist)
if __name__=='__main__':
          main()