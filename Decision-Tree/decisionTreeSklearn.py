from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from pandas import DataFrame

data=load_iris()
df=DataFrame(data.data,columns=['sepal_length','sepal_width','petal_length','petal_width'])
df['class']=data.target

X=df[['sepal_length','sepal_width','petal_length','petal_width']].values
y=df['class'].values

X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=50,test_size=0.3)

tree=DecisionTreeClassifier(criterion='entropy',random_state=50).fit(X_train,y_train)

scores=tree.score(X_test,y_test)
print(scores)
