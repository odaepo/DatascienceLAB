import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn import preprocessing, svm
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


# Load the clean dataset
df = pd.read_csv('Dataset/sale_clean.csv', low_memory=False)

#df.drop(['citta'], axis=1, inplace = True) 
#df.drop(['indirizzo'], axis=1, inplace = True) 
#df.drop(['provincia'], axis=1, inplace = True) 
#df.drop(['regione'], axis=1, inplace = True) 
#df.drop(['ripartizione_geografica'], axis=1, inplace = True) 
#df.drop(['classe_energetica'], axis=1, inplace = True) 

# Drop rows with missing values
df.dropna(inplace = True)

# Drop index column
#df.drop(columns=df.columns[0], axis=1, inplace = True)

# Prepare training and testing dataset
y = df['prezzo']
df.drop(['prezzo'], axis=1, inplace = True) 

# Categorical columns
categorical_columns = ['citta', 'indirizzo', 'provincia', 'regione', 'ripartizione_geografica', 'classe_energetica']

# Label encoder for categorical columns
#le = preprocessing.LabelEncoder()
#df[categorical_columns] = df[categorical_columns].apply(le.fit_transform)
#X = df

# One-hot encode the categorical columns
transformers = [
    ['one_hot', preprocessing.OneHotEncoder(), categorical_columns]
]

# Column transformer
ct = ColumnTransformer(transformers, remainder='passthrough')
X = ct.fit_transform(df)
#X = df

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train, y_train)

# Make predictions on the train and test daset
X_pred = model.predict(X_train)
y_pred = model.predict(X_test)
#print("Predictions:", y_pred)

# Evaluate the model
#print('Mean Absolute Error - Train:', metrics.mean_absolute_error(y_train, X_pred))
#print('Mean Absolute Error - Test:', metrics.mean_absolute_error(y_test, y_pred))

#print('Mean Squared Error - Train:', metrics.mean_squared_error(y_train, X_pred))
#print('Mean Squared Error - Test:', metrics.mean_squared_error(y_test, y_pred))

#print('Root Mean Squared Error - Train:', metrics.root_mean_squared_error(y_train, X_pred))
#print('Root Mean Squared Error - Test:', metrics.root_mean_squared_error(y_test, y_pred))

#print('Coefficients:', model.coef_)
#print('Intercept:', model.intercept_)

print('R^2 Score:', metrics.r2_score(y_train, X_pred))
print('R^2 Score:', metrics.r2_score(y_test, y_pred))

# Save the model
joblib.dump(model, 'model.joblib')