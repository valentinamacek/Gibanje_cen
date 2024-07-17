import pandas as pd
import numpy as np

df = pd.read_excel('ecoicop_klasifikacija.xlsx')

print(df.head())

data = df.to_numpy()
print(data[1])

