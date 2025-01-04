import pandas as pd 
import numpy as np 
from collections import Counter 

def trainTestSplit(X,y,testSize=0.3): 
      trainSize=int(1-testSize*len(X)) 
      X_train=X[:trainSize] 
      y_train=y[:trainSize] 
      X_test=X[trainSize:] 
      y_test=y[trainSize:] 
      return X_train,X_test,y_train,y_test 

def accuracyTest(predictions,y_test):
      accuracy=sum([pred==test for pred,test in zip(predictions,y_test)])/len(y_test)
      print(f"\nAccuracy: {accuracy:.3f}")

def get_most_common(y): 
      return Counter(y).most_common(1)[0][0] 

def calculate_purity(y): 
      counter=Counter(y) 
      return max(counter.values())/len(y) 

def find_best_split(X,y):
      best_purity=0
      best_feature= 0

      for feature in range(len(X[0])):
            values=set(row[feature] for row in X)
            avg_purity=0

            for value in values:
                  mask=[row[feature]==value for row in X]
                  subset_y=[y[i] for i in range(len(y)) if mask[i]]

            if len(subset_y)>0:
                avg_purity+=calculate_purity(subset_y)*len(subset_y)/len(y)

            if avg_purity>best_purity:
                  best_purity=avg_purity
                  best_feature=feature

      return best_feature


def build_tree(X,y,max_depth=3,depth=0):
      if depth>=max_depth or len(set(y))==1 or len(X[0])==0:
            return get_most_common(y)

      best_feature=find_best_split(X,y)
      tree={best_feature:{}}

      values=set(row[best_feature] for row in X)

      for value in values:
            mask=[row[best_feature]==value for row in X]
            subset_X=[row for i,row in enumerate(X) if mask[i]]
            subset_y=[y[i] for i in range(len(y)) if mask[i]]

            if len(subset_y)==0:
                  tree[best_feature][value]=get_most_common(y)
            else:
                  tree[best_feature][value]=build_tree(subset_X,subset_y,max_depth,depth+1)

      return tree


def predict(tree,x): 
      if not isinstance(tree,dict): 
            return tree 

      feature=next(iter(tree)) 
      value=float(x[feature])  

      if value not in tree[feature]: 
            prediction=max(tree[feature].values(),key=lambda x: list(tree[feature].values()).count(x)) 
            return prediction 

      return predict(tree[feature][value],x) 


def predictByInformationGain(X_train,y_train,X_test):
      tree=build_tree(X_train,y_train,max_depth=9) 
      print(tree)
      predictions=[predict(tree,x) for x in X_test] 
      return predictions


def main(): 
      df=pd.read_csv('iris/iris.data',header=None) 
      df.columns=['sepal_length','sepal_width','petal_length','petal_width', 'class'] 
      df=df.sample(frac=1).reset_index(drop=True) 

      X=df[['sepal_length','sepal_width','petal_length','petal_width']].values 
      y=df['class'].values 

      X_train,X_test,y_train,y_test=trainTestSplit(X,y,0.3) 
 
      predictions=predictByInformationGain(X_train,y_train,X_test) 
      accuracy=accuracyTest(predictions,y_test)


if __name__=='__main__': 
    main()