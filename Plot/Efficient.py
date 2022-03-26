"""

Efficient Frontier Simulation
it used to function in Marketdata classes,
simulated by monte-carlo simulation.
The stock ratio outputs a scatter plot using the Numpy built-in random function

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import Analyzer.Marketdata


mkt = Analyzer.Marketdata.Marketdata()
print("Please enter to company for compare")
stocks = list(input().split())
df = pd.DataFrame()
today = datetime.datetime.today().strftime('%Y-%m-%d')
print("simulated from 2010-01-01 to", "".join(today))
for s in stocks:
    df[s] = mkt.get_daily_price(s, '2010-01-01', ''.join(today))['close']


daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov * 252


port_ret = []
port_risk = []
port_weights = []


for _ in range(20000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)


portfolio = {'Returns': port_ret, 'Risk': port_risk}
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk'] + [s for s in stocks]]


df.plot.scatter(x='Risk', y='Returns', figsize=(8, 6), grid=True)
plt.title('Efficient Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()