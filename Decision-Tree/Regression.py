import pandas as pd
import numpy as np

def trainTestSplit(X,y,testSize=0.3):
          trainSize=int(1-testSize*len(X))
          X_train=X[:trainSize]
          y_train=y[:trainSize]
          X_test=X[trainSize:]
          y_test=X[trainSize:]
          return X_train,X_test,y_train,y_test

          
def fit_equation(X,y,class_name):
    
        binary_y=(y==class_name).astype(float)

        X_with_intercept=np.column_stack([X,np.ones(len(X))])

        coefficients = np.linalg.pinv(X_with_intercept) @ binary_y
    
        return coefficients[:-1], coefficients[-1]  # Return coefficients and intercept separately

def predict_score(X, coefficients, intercept):
    
        return np.dot(X, coefficients) + intercept

def predict_class(X, class_equations):
    
        scores = {}
        for class_name, (coefficients, intercept) in class_equations.items():
            scores[class_name] = predict_score(X, coefficients, intercept)
    
    # Return class with highest score
        return max(scores.items(), key=lambda x: x[1])[0]

def main():
        df = pd.read_csv('iris/iris.data', header=None)
        df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
        df=df.sample(frac=1).reset_index(drop=True)
    
        X=df[['sepal_length','sepal_width','petal_length','petal_width']].values
        y=df['class'].values
    
        X_train,X_test,y_train,y_test=trainTestSplit(X,y,0.3)
    
    
        classes=np.unique(y)

        class_equations={}
        print("\nLinear Equations for each class:")
        for class_name in classes:
                coefficients,intercept=fit_equation(X_train,y_train,class_name)
                class_equations[class_name]=(coefficients,intercept)
        
        # Print equation
                print(f"\n{class_name}:")
                print(f"{coefficients[0]:.3f}*sepal_length + "
                  f"{coefficients[1]:.3f}*sepal_width + "
                  f"{coefficients[2]:.3f}*petal_length + "
                  f"{coefficients[3]:.3f}*petal_width + "
                  f"{intercept:.3f}")
    
    # Make predictions
        predictions = []
        for x in X_test:
                pred_class = predict_class(x, class_equations)
                predictions.append(pred_class)
    
    # Calculate and print accuracy
        accuracy = sum(p == t for p, t in zip(predictions, y_test)) / len(y_test)
        print(accuracy)
    
    
if __name__ == '__main__':
        main()