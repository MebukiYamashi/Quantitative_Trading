"""Efficient Frontier Simulation
it used to function in Marketdata classes,
simulated by monte-carlo simulation.
The stock ratio outputs a scatter plot using the Numpy built-in random function
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import datetime
import Analyzer.Marketdata
sample = sys.stdin.readline

mkt = Analyzer.Marketdata.Marketdata()
sample = list(map(str, input().split()))
df = pd.DataFrame()
now = datetime.datetime.now()
s_day = datetime.datetime(now.year, now.month, now.day)

for s in sample:
    df[s] = mkt.read_naver(s, '2015-01-01', '2022-02-02')['close']

daily_ret = df.pct_change()
annal_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annal_cov = daily_cov * 252

pf_ret = []
pf_risk = []
pf_vol = []

for _ in range(20000):
    weight = np.random.random(len(sample))
    weight /= np.sum(weight)

    returns = np.dot(weight, annal_ret)
    risks = np.sqrt(np.dot(weight.T, np.dot(annal_cov, weight)))

    pf_ret.append(returns)
    pf_risk.append(risks)
    pf_vol.append(weight)

portfolio = {'returns': pf_ret, 'risks': pf_risk}
for i, s in enumerate(sample):
    portfolio[s] = [weight[i] for weight in pf_vol]
df = pd.DataFrame(portfolio)
df = df[['returns', 'risks'] + [s for s in sample]]

df.plot.scatter(x = 'risks', y = 'returns', figsize = (8, 6), grid=True)
plt.title('Efficient line')
plt.xlabel('Risk')
plt.ylabel('Expected returns')
plt.show()
