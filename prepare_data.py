import pandas as pd
import numpy as np
import json
import os
import os.path as path
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

path_to_log = path.abspath(path.curdir) + '\\logs\\'
logs = []

for file in os.listdir(path_to_log):
    if file.endswith(".json"):
        logs.append(file)

for i in range(0, len(logs)):
    print(str(i+1) + ": " + logs[i])



# with open(path_to_log, encoding="utf-8") as infile:
#         data_json = json.load(infile)
# df = pd.DataFrame(data_json['history'])
# df = df.transpose()
#
# df = df.astype(float)
#
# df.plot()
#
# plt.show()

