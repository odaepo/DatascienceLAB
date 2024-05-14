import pandas as pd
import numpy as np
import joblib

df = [
    [0, 2.0, 570.0, 2.0, 0, 2, 0, 0, 0, 0,	0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
]

# Load the clean dataset
#df = pd.read_csv('Dataset/sale_test.csv', low_memory=False)

# Load the model
model = joblib.load("model.joblib")

# Make predictions
pred = model.predict(df)

# Print the predictions
print(pred)