import pandas as pd
import numpy as np
import sys

print("Hello world!!")
print("Locura la IA")
print("Sin external libreries funciona perfecto!")

num = np.array([1,2,3,4,5,6,7])
df = pd.read_csv('./csv/words.csv')
print(df.head(5))
print(num)


print(sys.argv[1])
print(sys.argv[2])
