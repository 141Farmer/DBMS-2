'''
from sklearn.neighbors import KDTree
from numpy import random

rng=random.RandomState(30)
X=rng.randint(low=0,high=100,size=(10,2))  
with open('input.txt','w') as file:
    for x in X:
        file.writelines(str(x[0])+' '+str(x[1])+'\n')
'''
def build_kdtree(points,dimension=0):
    if not points:
        return None
  
    k=len(points[0])  
    axis=dimension%k

    points.sort(key=lambda x:x[axis])
    median=len(points)//2

    return {
        "point": points[median],
        "left": build_kdtree(points[:median],dimension+1),  
        "right": build_kdtree(points[median+1:],dimension+1)  
    }


def kdtree_query(tree,query_point,k=1,dimension=0):
    if tree is None:
        return []

    axis=dimension%len(query_point)

    next_branch=None
    opposite_branch=None
    if query_point[axis]<tree["point"][axis]:
        next_branch=tree["left"]
        opposite_branch=tree["right"]
    else:
        next_branch=tree["right"]
        opposite_branch=tree["left"]

    neighbors=kdtree_query(next_branch,query_point,k,dimension+1)

    current_point=tree["point"]
    distance=sum((query_point[i]-current_point[i])**2 for i in range(len(query_point)))**0.5

    neighbors.append((distance,current_point))
    neighbors.sort(key=lambda x: x[0])  
    neighbors=neighbors[:k]  

    if len(neighbors)<k or abs(query_point[axis]-current_point[axis])<neighbors[-1][0]:
        neighbors+=kdtree_query(opposite_branch,query_point,k,dimension+1)
        neighbors.sort(key=lambda x:x[0])
        neighbors=neighbors[:k] 

    return neighbors


if __name__=="__main__":
    points=[]
    with open('input.txt', 'r') as file:
        for line in file:
            values=list(map(int,line.strip().split()))
            points.append(values)

    tree=build_kdtree(points)
    query_point=[7,0]
    k=3
    neighbors=kdtree_query(tree,query_point,k)
    #print("KDTree:",tree)
    print(f"{k} nearest neighbors to {query_point}:")
    for neighbor in neighbors:
        print(neighbor)