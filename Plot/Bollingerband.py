"""
Based on the 20-day moving average of stock prices,
consists of the top of the relative high point and the bottom of the relative low point.
Formula:
        upper = middle + (2 * standard deviation)
        middle = MA20
        lower = middle - (2 * standard deviation)

%B -Indicators of where the stock price is in the band
Formula:
        (close_price - lower) / (upper - middle)

Bandwidth - The width between the upper and lower bowling bands
Formula:
        (upper - lower) / (middle)
"""

import matplotlib.pyplot as plt
import Analyzer.Marketdata

mkt = Analyzer.Marketdata.Marketdata()
print("Please enter company_name, year-month-date to check band")
name, date = map(str, input().split())
df = mkt.get_daily_price(''.join(name), '%s'%date)

df['MA20'] = df['close'].rolling(window=20).mean()  # 20개 종가 표본으로 평균 구하기
df['stddev'] = df['close'].rolling(window=20).std()  # stddev 칼럼으로 데이터프레임에 추가
df['upper'] = df['MA20'] + (df['stddev'] * 2)  # 중간 볼린저밴드 + (2 * 표준편차)를 계산(상단)
df['lower'] = df['MA20'] - (df['stddev'] * 2)  # 중간 볼린저밴드 + (2 * 표준편차)를 계산(하단)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower']) # (종가 - 하단밴드) / (상단밴드 - 하단밴드를 구해 %b 생성)
df = df[19:]  # 19번째행까지 NaN 이므로 20번째 행부터 사용

plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')  # x좌표 index의 종가를 y좌표로 설정해 실선 표시
plt.plot(df.index, df['upper'], 'r--', label='Upper band')  # 상단 볼린저밴드를 y좌표로 설정해 검은 실선표시
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')

plt.subplot(2, 1, 2)  # 2열 그리드에 배치
plt.plot(df.index, df['PB'], color='b', label='%B')

plt.grid(True)
plt.legend(loc='best')
plt.title('Bollinger Band (20 day, 2 std)')
plt.show()