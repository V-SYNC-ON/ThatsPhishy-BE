import pandas as pd

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier

import pickle

data=pd.read_csv("phishing.csv")
data = data.drop(['Index'],axis = 1)

#split data
X = data.drop(["class"],axis =1)
y = data["class"]
X_train, X_test, y_train, y_test = tts(X, y, test_size = 0.2, random_state = 42)
forest = RandomForestClassifier(n_estimators=10)
forest.fit(X_train,y_train)
y_train_forest = forest.predict(X_train)
y_test_forest = forest.predict(X_test)
print(classification_report(y_test, y_test_forest))

pickle.dump(forest, open('random_forest.pkl', 'wb'))