"""

Reversals
Buy: When the stock price tags the lower band and the indicator is strong-trended.
Sell: When the stock price tags the higher band and the indicator is weak-trended.
It using 'Intraday Intensity',
this indicator is close to 1 when the closing price is formed at the top of the band within the transaction range is 0,
when formed in the middle, and -1 is when formed at the bottom.
Intraday Intensity: (2 * C - H - L) / (H - L) * V
convert to percentage: sum of intensity over 21 days / sum of volumes over 21 days * 100

"""

import matplotlib.pyplot as plt
import Analyzer.Marketdata
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

mkt = Analyzer.Marketdata.Marketdata()
print("Please enter company_name, year-month-date to check band")
name, date = map(str, input().split())
df = mkt.get_daily_price(''.join(name), '%s'%date)

df['MA20'] = df['close'].rolling(window=20).mean()  # 20개 종가 표본으로 평균 구하기
df['stddev'] = df['close'].rolling(window=20).std()  # stddev 칼럼으로 데이터프레임에 추가
df['upper'] = df['MA20'] + (df['stddev'] * 2)  # 중간 볼린저밴드 + (2 * 표준편차)를 계산(상단)
df['lower'] = df['MA20'] - (df['stddev'] * 2)  # 중간 볼린저밴드 + (2 * 표준편차)를 계산(하단)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower']) # (종가 - 하단밴드) / (상단밴드 - 하단밴드를 구해 %b 생성)
df['TP'] = (df['high'] + df['low'] + df['close']) / 3
df['II'] = (2*df['close']-df['high']-df['low'])/(df['high']-df['low'])*df['volume']
df['IIP21'] = df['II'].rolling(window=21).sum()/df['volume'].rolling(window=21).sum()*100
df = df.dropna()

plt.figure(figsize=(9, 9))
plt.subplot(3, 1, 1)

plt.title('%s Bollinger Band(20 day, 2 std) - Reversals' %name)
plt.plot(df.index, df['close'], 'm', label='Close')
plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')

for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')

plt.subplot(3, 1, 2)
plt.plot(df.index, df['PB'], 'b', label='%b')
plt.grid(True)
plt.legend(loc='best')

plt.subplot(3, 1, 3)
plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')
for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        plt.plot(df.index.values[i], 0, 'bv')

plt.grid(True)
plt.legend(loc='best')
plt.show()
