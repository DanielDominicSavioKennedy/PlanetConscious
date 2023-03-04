import pandas as pd


hey = pd.read_csv("data.csv", error_bad_lines=False)
print(hey.to_dict())
print(hey)