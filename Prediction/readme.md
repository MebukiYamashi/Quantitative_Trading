# Prediction

## RNN prediction

This is an example of stock price forecasting using LSTM (Long/Short Term Memory) using Keras built into tensorflow.


Based on the 21days OHLCV data of stock prices,  
it consists of the top of the relative high point and the bottom of the relative low point.

using 21 days of OHLCV data, Dataset is used for training and testing at a 7:3 ratio.

The activation function was set to relu, the number of units was set to 21, the number of learning was set to 100, the dropout was set to 10%, the optimization was adam, and the loss function used an Mean squared error (MSE).

- example of prediction: KRX:000150, Forecast data for March 30

![img.png](img.png)
![img_1.png](img_1.png)
