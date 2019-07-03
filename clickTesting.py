import getopt
import sys
import pandas as pd
import numpy as np
import time

from collections import defaultdict

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)


df = df[df["col1"].isin(["control"])]
print(df)
print(df.size)
