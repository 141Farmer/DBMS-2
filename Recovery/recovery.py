from pathlib import Path

def recover(log):
          ignore=[]
          redo=[]
          undo=[]
          ignore=[]
          ckpt=False
          transactions=[]
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


def main():
          with open(Path(__file__).parent/'input.pdf') as file:
                   log=file.read()               
          log=log.splitlines()
          ignore,undo,redo=recover(log)
          print('Ignore :',*ignore)
          print('Undo :',*undo)
          print('Redo :',*redo)

if __name__=='__main__':
          main()