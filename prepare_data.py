import pandas as pd
import numpy as np
import json
import os.path as path
import matplotlib.pyplot as plt


path_to_log = path.abspath(path.curdir) + '\\logs\\trimmed.json'
with open(path_to_log, encoding="utf-8") as infile:
        data_json = json.load(infile)
df = pd.DataFrame(data_json)
df = df.transpose()

df = df.astype(float)

df.plot()

plt.show()

