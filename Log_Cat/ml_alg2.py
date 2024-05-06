import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder

# Load the dataset
data = pd.read_csv('results.csv')

# Isolate the columns for one-hot encoding
teams = data[['team1', 'team2']]

# One-hot encode the team columns
encoder = OneHotEncoder(sparse_output=False)
teams_encoded = encoder.fit_transform(teams)
feature_names = encoder.get_feature_names_out(['team1', 'team2'])

# Create a DataFrame from the encoded data
X = pd.DataFrame(teams_encoded, columns=feature_names)

# Add any other numerical features you need in the model
X['team1_kills'] = data['team1_kills']
X['team2_kills'] = data['team2_kills']
X['flip'] = data['flip']  # Assuming flip is a numeric column

# Set the target variable
y = data['team1_win']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the logistic regression model without intercept
model = LogisticRegression(fit_intercept=False)
model.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("Confusion Matrix:\n", conf_matrix)
