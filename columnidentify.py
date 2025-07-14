import pandas as pd

df = pd.read_csv("emails.csv")
print("Columns in your CSV file:", df.columns.tolist())
