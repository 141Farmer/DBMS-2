from pandas import read_csv
from collections import Counter
from math import log2

def trainTestSplit(X,y,testSize=0.3):
      trainSize=int((1-testSize)*len(X))
      X_train=X[:trainSize]
      y_train=y[:trainSize]
      X_test=X[trainSize:]
      y_test=y[trainSize:]
      return X_train,X_test,y_train,y_test

def get_most_common(y):
      return Counter(y).most_common(1)[0][0]

def calculate_entropy(y):
      if len(y)==0:
            return 0
      counts=Counter(y)
      probabilities=[count/len(y) for count in counts.values()]
      return -sum(p*log2(p) for p in probabilities)

def calculate_information_gain(X_feature, y):
      parent_entropy=calculate_entropy(y)
    
      values=set(X_feature)
      weighted_entropy=0

      for value in values:
            mask=X_feature==value
            subset_y=y[mask]
            if len(subset_y)>0:
                  weight=len(subset_y)/len(y)
                  weighted_entropy+=weight*calculate_entropy(subset_y)

      return parent_entropy-weighted_entropy

def find_best_split(X, y):
      best_gain=-float('inf')
      best_feature=0
 
      for feature in range(X.shape[1]):
            gain=calculate_information_gain(X[:,feature],y)
            if gain>best_gain:
                  best_gain=gain
                  best_feature=feature

      return best_feature

def predict(feature_value,feature_values,y):
      mask=feature_values==feature_value
      if not any(mask): 
            return get_most_common(y)
      return get_most_common(y[mask])

def make_predictions(X_train, y_train, X_test):
      predictions=[]
    
      for x_test in X_test:
            best_feature=find_best_split(X_train,y_train)
            pred=predict(x_test[best_feature],X_train[:,best_feature],y_train)
            predictions.append(pred)
    
      return predictions


def main():
      df=read_csv('iris/iris.data',header=None)
      df.columns=['sepal_length','sepal_width','petal_length','petal_width','class']
      df=df.sample(frac=1).reset_index(drop=True)
    
      X=df[['sepal_length','sepal_width','petal_length','petal_width']].values
      y=df['class'].values
    
      X_train,X_test,y_train,y_test=trainTestSplit(X,y,0.3)
    
      predictions=make_predictions(X_train,y_train,X_test)
    
      accuracy=sum([pred==test for pred,test in zip(predictions,y_test)])/len(y_test)
      print(f"\nAccuracy: {accuracy:.3f}")

if __name__ == '__main__':
    main()