import pandas as pd
import numpy as np
from collections import Counter

def trainTestSplit(X,y,testSize=0.3):
          trainSize=int(1-testSize*len(X))
          X_train=X[:trainSize]
          y_train=y[:trainSize]
          X_test=X[trainSize:]
          y_test=X[trainSize:]
          return X_train,X_test,y_train,y_test


def get_most_common(y):
    """Return most common class in a list"""
          return Counter(y).most_common(1)[0][0]

def calculate_purity(y):
    """Calculate how pure a node is (1 = pure, 0 = impure)"""
          counter = Counter(y)
          return max(counter.values()) / len(y)

def find_best_split(X, y):
    """Find the best feature to split on"""
          best_purity = 0
          best_feature = 0
    
          for feature in range(X.shape[1]):
        # Get unique values for this feature
                    values = set(X[:, feature])
        
        # Calculate average purity for this feature
          avg_purity = 0
          for value in values:
                    mask = X[:, feature] == value
                    if sum(mask) > 0:  # Avoid empty splits
                              avg_purity += calculate_purity(y[mask]) * sum(mask) / len(y)
        
        # Update best if this feature is better
          if avg_purity > best_purity:
                    best_purity = avg_purity
                    best_feature = feature
            
          return best_feature

def build_tree(X, y, max_depth=3, depth=0):
    """Build a decision tree"""
    # Return most common class if:
    # 1. We've reached max depth
    # 2. All samples are of same class
    # 3. No more features to split on
          if depth >= max_depth or len(set(y)) == 1 or X.shape[1] == 0:
                    return get_most_common(y)
    
    # Find best feature to split on
          best_feature = find_best_split(X, y)
          tree = {best_feature: {}}
    
    # Split on each value of the best feature
          for value in set(X[:, best_feature]):
        # Get data matching this feature value
                    mask = X[:, best_feature] == value
                    subset_X = X[mask]
                    subset_y = y[mask]
        
          if len(subset_y) == 0:
                    tree[best_feature][value] = get_most_common(y)
          else:
            # Recursively build tree for this subset
                    tree[best_feature][value] = build_tree(subset_X, subset_y, max_depth, depth + 1)
    
          return tree

def predict(tree, x):
    """Predict class for a single sample"""
    # If tree is just a value, return it
          if not isinstance(tree,dict):
                    return tree
    
    # Get the feature and value from the sample
          feature = next(iter(tree))
          value = float(x[feature])  # Convert numpy values to float
    
    # If we haven't seen this value before, return most common value
          if value not in tree[feature]:
                    prediction=max(tree[feature].values(),key=lambda x: list(tree[feature].values()).count(x))
                    return prediction
                  
    
    # Recurse on matching branch
          return predict(tree[feature][value],x)

# Example usage
def main():
   
          df = pd.read_csv('iris/iris.data', header=None)
          df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
          df=df.sample(frac=1).reset_index(drop=True)
    
          X=df[['sepal_length','sepal_width','petal_length','petal_width']].values
          y=df['class'].values
    
          X_train,X_test,y_train,y_test=trainTestSplit(X,y,0.3)
    
    
          tree=build_tree(X_train,y_train,max_depth=3)
    
 
          predictions=[predict(tree,x) for x in X_test]
    

    accuracy = sum(p == t for p, t in zip(predictions, y_test)) / len(y_test)
    print(f"Accuracy: {accuracy:.2f}")

if __name__ == '__main__':
    main()