from pathlib import Path

def recover(log):
          total=[[],[]]
          ckpt=False       
          for itr in reversed(log):
                    c=itr[1:-1].split(' ')
                    if 'CKPT(' in c[0]:
                              ckpt=True
                    elif c[0]=='COMMIT' and ckpt is True:
                              total[0].append('Ignore')
                              total[1].append(c[1])
                    elif c[0]=='COMMIT':
                              total[0].append('Redo')
                              total[1].append(c[1])
                    elif c[0]=='START' and c[1] not in total[1]:
                              total[0].append('Undo')
                              total[1].append(c[1])
          return total

def value(log,total):
          transactionValues=[[],[]]
          for itr in log:
                    c=itr[1:-1].split(' ')
                    if len(c)!=4 or c[1] in transactionValues[0]:
                              continue
                    if c[0] in total[1]:
                              i=total[1].index(c[0])
                    else:
                              continue
                    if total[0][i]=='Redo':
                              transactionValues[0].append(c[1])
                              transactionValues[1].append(c[3])
                    elif total[0][i]=='Undo':
                              transactionValues[0].append(c[1])
                              transactionValues[1].append(c[2])
                    elif total[0][i]=='ignore':
                              transactionValues[0].append(c[1])
                              transactionValues[1].append(c[3])
          return transactionValues

def main():
          with open(Path(__file__).parent/'input.pdf') as file:
                   log=file.read()               
          log=log.splitlines()
          total=recover(log)
          for i in range(len(total[0])):
                    print(total[0][i],total[1][i])
          transactionValues=value(log,total)
          for i in range(len(transactionValues[0])):
                    print(transactionValues[0][i],transactionValues[1][i])
          
if __name__=='__main__':
          main()