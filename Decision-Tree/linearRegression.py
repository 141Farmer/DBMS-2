from pandas import read_csv


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


def fit_equation(X_train,y_train,class_name):
          binary_y=[(1 if label==class_name else 0) for label in y_train]
          X_class=[X_train[i] for i in range(len(X_train)) if binary_y[i]==1]
          y_class=[binary_y[i] for i in range(len(binary_y)) if binary_y[i]==1.0]

          mean_X=[sum(feature)/len(feature) for feature in zip(*X_class)]
          mean_y=1
          
          '''y=a+b*x'''
          coefficients=[]
          for i in range(len(mean_X)):
                    cov_xy,var_x=0,0
                    for j in range(len(X_train)):
                              cov_xy+=(X_train[j][i]-mean_X[i])*(binary_y[j]-mean_y)
                              var_x+=(X_train[j][i]-mean_X[i])**2
                    '''b=cov(X,y)/var(X)'''
                    coefficients.append(cov_xy/var_x if var_x!= 0 else 0)
          '''mean_y=a+b*mean_X'''
          '''a=mean_y-b*mean*X'''
          intercept=mean_y-sum(coefficients[i]*mean_X[i] for i in range(len(coefficients)))
        
          coefficients=[float(c) for c in coefficients]
          intercept=float(intercept)

          return coefficients,intercept


def predict_score(X,coefficients,intercept):
          dot_product=sum([x*c for x,c in zip(X,coefficients)])+intercept
          return dot_product


def predict_class(x_test,class_equations):
          scores={}
          for class_name,(coefficients,intercept) in class_equations.items():
                    scores[class_name]=predict_score(x_test,coefficients,intercept)

          return max(scores.items(),key=lambda x:x[1])[0]


def predictByLinearRegression(X_train,y_train,X_test,classes,columns):        
          class_equations={}
          for class_name in classes:
                    coefficients,intercept=fit_equation(X_train,y_train,class_name)
                    class_equations[class_name]=(coefficients,intercept)

          '''
          for class_name,(coefficients,intercept) in class_equations.items():
                    print('\nEquation for class: ',class_name)
                    for i in range(len(coefficients)):
                              print(f'({coefficients[i]:.3f}*{columns[i]}) + ',end='')
                    print(f'{intercept:.3f}')
          '''
          
          predictions=[]
          for x_test in X_test:
                    prediction=predict_class(x_test,class_equations)
                    predictions.append(prediction)
          
          return predictions


def main():
          df=read_csv('iris/iris.data',header=None)
          df.columns=['sepal_length','sepal_width','petal_length','petal_width','class']
          df=df.sample(frac=1).reset_index(drop=True)
    
          X=df[['sepal_length','sepal_width','petal_length','petal_width']].values
          y=df['class'].values
    
          X_train,X_test,y_train,y_test=trainTestSplit(X,y,0.3)
    
          classes=list(set(y))

          predictions=predictByLinearRegression(X_train,y_train,X_test,classes,df.columns)

          accuracyTest(predictions,y_test)

 
if __name__ == '__main__':
        main()