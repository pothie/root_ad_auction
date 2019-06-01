import numpy as np
import matplotlib.pyplot as plt

states = df.columns[list('state_' in x for x in df.columns)]
states_clicks = df.columns[list(('state_' in x)|(x=='clicks') for x in df.columns)]
click_rate = []
for col in states:
    click_rate.append(df.loc[df.loc[:,col]==1,'clicks'].mean())
st = list(x[6:8] for x in states)
st[len(st)-1] = 'others'
num_ad =df[states].mean()
sc = pd.DataFrame(
    {'states': st,
     'click_rate': click_rate,
     'num_ad':num_ad
    })
sc = sc.sort_values(by=['click_rate'])

fig, ax1= plt.subplots(nrows=1, ncols=1,figsize=(10,5))

color = 'tab:blue'
ax1.set_ylabel('sent ad rate', color=color)  # we already handled the x-label with ax1
plt.bar(sc['states'],sc['num_ad'],color=color,alpha = 0.7)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_xlabel('states', color=color)
ax2.set_ylabel('click rate', color=color)
plt.scatter(sc['states'], sc['click_rate'],color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.show()

states_clicks = df[['local_hour','clicks']]
click_rate1 = []
for h in range(0,24):
    click_rate1.append(df.loc[df.loc[:,'local_hour']==h,'clicks'].mean())
    
fig, ax1= plt.subplots(nrows=1, ncols=1,figsize=(10,5))

color = 'tab:blue'
ax1.set_xlabel('hour of a day', color=color)
ax1.set_ylabel('sent ad rate', color=color)  # we already handled the x-label with ax1
plt.bar(range(0,24),df.groupby('local_hour').count().iloc[:,0]/len(df.index),color=color,alpha = 0.7)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis


color = 'tab:red'
ax2.set_ylabel('click rate', color=color)
plt.scatter(range(0,24), click_rate1,color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.tight_layout()
plt.show()
