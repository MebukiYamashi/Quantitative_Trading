# Plot

## Efficient.py


Efficient Frontier Simulation
it used to function in Marketdata classes, simulated by monte-carlo simulation.  
The stock ratio outputs a scatter plot using the Numpy built-in random function.

## Bollingerband.py

Based on the 20-day moving average of stock prices,  
consists of the top of the relative high point and the bottom of the relative low point.
+ Formula of the Bollingerband


      upper = middle + (2 * standard deviation)  
      middle = MA20
      lower = middle - (2 * standard deviation)  


      %b: Indicators of where the stock price is in the band  
          (close_price - lower) / (upper - middle)

      Bandwidth: The width between the upper and lower bowling bands  
                 (upper - lower) / (middle)

## Trendfollowing.py

Based on the %b indicator and MFI(Money Flow Index)

        MFI = Typical Price * Volume
              100 - ( 100 / ( 1 + Positive MFI / Negative MFI)
        Positive | Negative MFI: sums of bull | bear times of Money flow
        Typical Price: H, L, V for a specific period are combined and divided by 3

## Reversal.py

Buy: When the stock price tags the lower band and the indicator is strong-trended.
+ (%b indicator < 0.05, Intraday Intensity > 0 )

Sell: When the stock price tags the higher band and the indicator is weak-trended.
+ (%b indicator > 0.95, Intraday Intensity < 0 )

It using 'Intraday Intensity' 

        Intraday Intensity: (2 * C - H - L) / (H - L) * V
        convert to percentage: sum of intensity(21 days) / sum of volumes over(21 days) * 100
