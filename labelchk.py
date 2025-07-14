import pandas as pd

df = pd.read_csv("emails.csv")
print(df["Email Type"].value_counts())
