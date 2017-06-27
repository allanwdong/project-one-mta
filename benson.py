import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

from IPython.display import Image
# enables inline plots, without it plots don't show up in the notebook

%matplotlib inline

df = pd.read_csv("http://web.mta.info/developers/data/nyct/turnstile/turnstile_170624.txt")


columns = ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'EXITS']
df.columns = columns
# rename columns because original EXITS column name had super long empty space at the end


df['DATETIME']=pd.to_datetime(df.DATE+df.TIME, format='%m/%d/%Y%H:%M:%S')
# create DATETIME column

col_groups =df.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])
df['TIMEDIFF_ENTRIES'] = col_groups['ENTRIES'].diff(periods = 6)
df['TIMEDIFF_EXITS'] = col_groups['EXITS'].diff(periods = 6)
df.fillna(value = 0)
# create TIMEDIFF_ENTRIES and TIMEDIFF_EXITS columns - true numbers of entries/exits per turnstile

df.insert(2, 'STATION', df.pop('STATION'))
# moves STATION column to position 2, when counting C/A as 0

df.drop(['LINENAME','DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'EXITS'], axis=1, inplace=True)
# drops LINENAME, DIVISION, DATE, TIME, DESC, ENTRIES, EXITS columns


df.loc[df.STATION=='CHAMBERS ST'].plot(kind='bar',x='DATETIME', y='TIMEDIFF_ENTRIES', subplots=True, figsize = (16,10))
# replace 'CHAMBERS ST' with any station name to produce bar plot
