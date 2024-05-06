import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report

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

# Creating the encoder
encoder = OneHotEncoder(sparse_output=False)

# Fitting and transforming the encoder on categorical columns
one_hot_encoded = encoder.fit_transform(data[categorical_columns])
one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_columns))

# Concatenating the encoded df with the original df and dropping the original categorical columns
df_encoded = pd.concat([data.drop(categorical_columns, axis=1), one_hot_df], axis=1)

# Defining the target variable and features
y = df_encoded['tm_1_win']
X = df_encoded.drop('tm_1_win', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)


# Split the data
print(df_encoded.head())
print(y)
print(y.value_counts())
print(X)

print("Accuracy:", accuracy)
print("Confusion Matrix:\n", conf_matrix)
print(classification_report(y_test, y_pred))