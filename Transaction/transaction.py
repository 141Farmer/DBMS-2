from pathlib import Path
from csv import reader

def graphMake(input):
          pair=[]
          transactions=[]
          operations=[]
          values=[]
          graph=[]
          numStep=len(input[0])
          numTranasaction=len(input)

          for j in range(1,numStep):                    
                    for i in range(numTranasaction):
                              if input[i][j]!='-' and input[i][j]!='COM':
                                        transaction=input[i][0]
                                        operation=input[i][j][0]
                                        value=input[i][j][2]
                                        if value in values:    
                                                  for idx in range(len(transactions)):
                                                            if values[idx]==value and transaction!=transactions[idx]:
                                                                      if operation!=operations[idx] or operation=='W':
                                                                                graph.append([transactions[idx],transaction])
                                        transactions.append(transaction)
                                        operations.append(operation)
                                        values.append(value)

          '''                          
          for i in range(len(transactions)):
                    print(transactions[i],operations[i],values[i])
          '''

          return graph

def cycleCheck(graph):
          adjList={}
          for edge in graph:
                    u,v=edge
                    if u not in adjList:
                              adjList[u]=[]
                    adjList[u].append(v)
          visited=set()
          recStack=set()

          def dfs(node):
                    if node in recStack:
                              return True
                    if node in visited:
                              return False
                    recStack.add(node)
                    visited.add(node)
                    for neighbor in adjList.get(node,[]):
                              if dfs(neighbor):
                                        return True
                    recStack.remove(node)
                    return False

          for node in adjList:
                    if node not in visited:
                              if dfs(node):
                                        return True

          return False



def main():
          input=[]
          with open(Path(__file__).parent/'input.csv','r') as file:
                    data=reader(file)
                    for d in data:
                              input.append(d)
          graph=graphMake(input)
          for i in range(len(graph)):
                    print(graph[i][0],'->',graph[i][1])

          if cycleCheck(graph) is True:
                    print('Conflict unserializable')
          else:
                    print('Conflict serializable')
          
if __name__=='__main__':
          main()