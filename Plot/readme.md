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


     %B: Indicators of where the stock price is in the band  


            (close_price - lower) / (upper - middle)

     Bandwidth: The width between the upper and lower bowling bands  

            (upper - lower) / (middle)
