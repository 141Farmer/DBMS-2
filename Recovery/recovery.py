from pathlib import Path

def recover(log):
          ignore=[]
          redo=[]
          undo=[]
          ignore=[]
          ckpt=False       
          for itr in reversed(log):
                    c=itr[1:-1].split(' ')
                    if 'CKPT(' in c[0]:
                              ckpt=True
                    elif c[0]=='COMMIT' and ckpt is True:
                              ignore.append(c[1])
                    elif c[0]=='COMMIT':
                              redo.append(c[1])
                    elif c[0]=='START' and c[1] not in redo and c[1] not in ignore:
                              undo.append(c[1])
          return ignore,undo,redo

def value(log,ignore,undo,redo):
          transactionValues=[[],[]]
          for itr in log:
                    c=itr[1:-1].split(' ')
                    if len(c)==4 and c[1] in transactionValues[0]:
                              continue
                    if 'T' in c[0] and c[0] in redo:
                              transactionValues[0].append(c[1])
                              transactionValues[1].append(c[3])
                    elif 'T' in c[0] and c[0] in undo:
                              transactionValues[0].append(c[1])
                              transactionValues[1].append(c[2])
                    elif 'T' in c[0] and c[0] in ignore:
                              transactionValues[0].append(c[1])
                              transactionValues[1].append(c[3])
          return transactionValues

def main():
          with open(Path(__file__).parent/'input.pdf') as file:
                   log=file.read()               
          log=log.splitlines()
          ignore,undo,redo=recover(log)
          transactionValues=value(log,ignore,undo,redo)
          print('Ignore :',*ignore)
          print('Undo :',*undo)
          print('Redo :',*redo)
          for i in range(len(transactionValues[0])):
                    print(transactionValues[0][i],transactionValues[1][i])

if __name__=='__main__':
          main()