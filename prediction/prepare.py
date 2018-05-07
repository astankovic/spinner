import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# create a differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return pd.Series(diff)
        
df = pd.read_csv('2018_04_26_Zaqatala_Shuvalan.csv')

df_increments = pd.DataFrame()

for column in df.columns:
    df_increments[column + '_increment'] = difference(df[column])

fig = plt.figure()

p1 = fig.add_subplot(211)
p12 = fig.add_subplot(212)
##p2 = fig.add_subplot(312)
##p3 = fig.add_subplot(313)

p1.plot(df['odd_1'])
p12.plot(df_increments['odd_1_increment'][df_increments['odd_1_increment']>0], c='r')
p12.plot(df_increments['odd_1_increment'][df_increments['odd_1_increment']<=0], c='b')

##p2.plot(df['odd_x'])
##p3.plot(df['odd_2'])

p1.legend()
p12.legend()
##p2.legend()
##p3.legend()

plt.show()
