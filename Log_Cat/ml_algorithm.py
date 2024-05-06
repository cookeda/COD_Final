import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder

data = pd.read_csv('results.csv')

'''TODO: 
1. One Hot Encoder (DONE)
2. x = features, y = target
3. Split data into training and testing sets
4. Init and train logitic regression
5. Evaluate the model
'''

categorical_columns = data.select_dtypes(include=['object']).columns.tolist()

encoder = OneHotEncoder(sparse_output=False)

one_hot_encoded = encoder.fit_transform(data[categorical_columns])
one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(categorical_columns))

df_encoded = pd.concat([data, one_hot_df], axis=1)
df_encoded = df_encoded.drop(categorical_columns, axis=1)
df_encoded.to_csv('encoded_results.csv')


# Set the features and target
X = abs(df_encoded['tm_1_score'] - df_encoded['tm_2_score'])
y = df_encoded['tm_1_win']  # Target: 'team1_win'

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save the encoded data to a new CSV file
df_encoded.to_csv('encoded_results.csv')

# Display the resulting dataframe
print(f"Encoded data:\n{df_encoded.head()}")