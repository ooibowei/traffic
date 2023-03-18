import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import statsmodels.api as sm

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


with open('data/df_5118east.pickle', 'rb') as f:
    df_east = pickle.load(f)
    
with open('data/df_5118west.pickle', 'rb') as f:
    df_west = pickle.load(f)

print(sm.tsa.stattools.adfuller(df_east))

plot_acf(df_east)
plot_acf(df_east.diff().dropna()) # d=1
plot_acf(df_east.diff().diff().dropna()) # d=2

plot_acf(df_east.diff(24).dropna()) # D=1
plot_pacf(df_east.diff(24).dropna()) # D=1

plot_acf(df_east.diff(24).diff().dropna()) # d=1, D=1
plot_pacf(df_east.diff(24).diff().dropna()) # d=1, D=1

mod = sm.tsa.statespace.SARIMAX(df_east, order=(0,0,0), seasonal_order=(0,1,1,24), freq='H')
model = mod.fit()
residuals = pd.DataFrame(model.resid)
plot_acf(residuals, auto_ylims=True, zero=False)
plot_pacf(residuals, zero=False, auto_ylims=True)



plot_acf(df_east.diff(24).dropna(), auto_ylims=True, zero=False)
plot_pacf(df_east.diff(24).dropna(), auto_ylims=True, zero=False)

mod = sm.tsa.statespace.SARIMAX(df_east, order=(2,0,0), seasonal_order=(0,1,0,24), freq='H')
model = mod.fit()
residuals = pd.DataFrame(model.resid)
plot_acf(residuals, auto_ylims=True, zero=False, lags=100)
plot_pacf(residuals, auto_ylims=True, zero=False, lags=100)
sm.stats.acorr_ljungbox(residuals,lags=24)


from pmdarima.arima import auto_arima


model = auto_arima(df_east, 
                      test='adf',
                      max_p=5, max_q=5, max_P=5, max_Q=5,
                      m=24,             
                      D=1,          
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)