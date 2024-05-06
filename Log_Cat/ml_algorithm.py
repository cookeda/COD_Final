import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import normalize
import numpy as np


data = pd.read_csv('results.csv')

'''TODO: 
1. One Hot Encoder (DONE)
2. x = features, y = target
3. Split data into training and testing sets
4. Init and train logitic regression
5. Evaluate the model
'''

# Selecting categorical columns
categorical_columns = ['t1', 't2']

encoder = OneHotEncoder(sparse_output=False)
one_hot_encoded = encoder.fit_transform(data[categorical_columns])
one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_columns))

df_encoded = pd.concat([data.drop(categorical_columns, axis=1), one_hot_df], axis=1)
df_encoded['score_diff'] = abs(df_encoded['tm_1_score'] - df_encoded['tm_2_score'])
columns_to_drop = ['tm_1_score', 'tm_2_score', 'tm_1_win', 'date']  # add any other columns that should not be used as features

# Feature matrix X
X = df_encoded.drop(columns=columns_to_drop)
y = df_encoded['tm_1_win']
print('x, y', X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.19775, random_state=42)
model = LogisticRegression(max_iter=1000, C=0.0375, penalty = 'l2')  # Lower C means higher regularization
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy on Test Set:", accuracy)
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", report)
