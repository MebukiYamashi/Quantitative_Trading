"""
Trend following
buying on the bull-trend and selling on the bear-trend.
Buy: When the stock price approaches the top band and the indicator is strong-trended.
Sell: When the stock price approaches the lower band and the indicator is weak-trended.
%b: Buy = when MFI is higher than 0.8
    Sell = when MFI is lower than 0.2

MFI: Money flow index = 100 - (100 / (1+positive money flow/negative money flow))

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
df['PMF'] = 0
df['NMF'] = 0

for i in range(len(df.close) - 1):
    if df.TP.values[i] < df.TP.values[i+1]:
        df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.NMF.values[i+1] = 0
    else:
        df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.PMF.values[i+1] = 0

df['MFR'] = (df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum())
df['MFI10'] = 100 - 100 / (1 + df['MFR'])
df = df[19:]

plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.title('%s Trend following with based bollinger band(20days, 2std)' %name)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')  # x좌표 index의 종가를 y좌표로 설정해 실선 표시
plt.plot(df.index, df['upper'], 'r--', label='Upper band')  # 상단 볼린저밴드를 y좌표로 설정해 검은 실선표시
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')


for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')

plt.subplot(2, 1, 2)
plt.plot(df.index, df['PB'] * 100, 'b', label = "%B * 100")
plt.plot(df.index, df['MFI10'], 'g--', label = 'MFI(10 days)')
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])

for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')

plt.grid(True)
plt.legend(loc='best')
plt.show()