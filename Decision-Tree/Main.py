from pandas import read_csv,Series
from linearRegression import predictByLinearRegression
from decisionTreeGain import predictByInformationGain

def kFoldCrossValidation(X,y,n_splits):
          X_fold=[]
          y_fold=[]
          l=len(y)
          for i in range(0,l,l//n_splits):
                    X_fold.append(X[i:i+l//n_splits])
                    y_fold.append(y[i:i+l//n_splits])
          return X_fold,y_fold

def accuracyTest(predictions,y_test):
          accuracy=sum([pred==test for pred,test in zip(predictions,y_test)])/len(y_test)
          return accuracy

def fScores(predictions, y_test):
          truePositive=sum([pred==test for pred, test in zip(predictions,y_test)])
          falsePositive=sum([pred!=test for pred, test in zip(predictions,y_test)])
          falseNegative=falsePositive 
          trueNegative=len(y_test)-truePositive

          precision=truePositive/(truePositive+falsePositive) 
          distance=1-precision
          recall=truePositive/(truePositive+falseNegative) if (truePositive+falseNegative)>0 else 0
    
          f1=2*(precision*recall)/(precision+recall) if (precision+recall)>0 else 0
          f2=5*(precision*recall)/(4*precision+recall) if (4*precision+recall) > 0 else 0

          print('\n                         Predicted')
          print('                   yes          no')
          print(f'         yes     {truePositive:4d}        {falseNegative:4d}')
          print('Actual')
          print(f'         no      {falsePositive:4d}        {trueNegative:4d}')
          print(f'\nPrecision: {precision:.3f}')
          print(f"Distance to Heaven: {distance:.3f}")
          print(f'Recall: {recall:.3f}')
          print(f'F1 Score: {f1:.3f}')
          print(f'F2 Score: {f2:.3f}')
    
          return precision,distance,f1,f2



def main():
          df=read_csv('iris/iris.data',header=None)
          df.columns=['sepal_length','sepal_width','petal_length','petal_width','class']
          df=df.sample(frac=1).reset_index(drop=True)
    
          X=df[['sepal_length','sepal_width','petal_length','petal_width']].values
          y=df['class'].values
          classes=list(set(y))

          n_splits=5
          X_fold,y_fold=kFoldCrossValidation(X,y,n_splits)

          totalAccuracy=0
........  totalPrecision=0
          totalF1=0
          totalF2=0
          totalDistance=0
          for i in range(n_splits):
                    X_train,y_train=[],[]

                    X_first=X_fold[0:i]          
                    X_second=X_fold[i+1:n_splits-1]
                    for array in X_first:
                              X_train.extend(array.tolist())
                    for array in X_second:
                              X_train.extend(array.tolist())

                    y_first=y_fold[0:i]
                    y_second=y_fold[i+1:n_splits-1]
                    for array in y_first:
                              y_train.extend(array.tolist())
                    for array in y_second:
                              y_train.extend(array.tolist())
                    
                    X_test,y_test=X_fold[i],y_fold[i]
                    #predictions=predictByInformationGain(X_train,y_train,X_test)
                    predictions=predictByLinearRegression(X_train,y_train,X_test,classes,df.columns)
                    print(f'\n{i+1}th split')
                    precision,distance,f1,f2=fScores(predictions,y_test)
                    totalPrecision+=precision
                    totalDistance+=distance
                    totalF1+=f1
                    totalF2+=f2
          print(f"\nMean Precesion: {totalPrecision/n_splits:.3f}")
          print(f"\nMean distance to heaven score: {totalDistance/n_splits:.3f}")
          print(f"\nMean F1 score: {totalF1/n_splits:.3f}")
          print(f"\nMean F2 score: {totalF2/n_splits:.3f}")


if __name__=='__main__':
          main()