# =============================================================================
# SARIMA is not suitable because of multiple seasonalities in the hourly data 
# (daily and weekly)
#
# We build 2 models, one using TBATS and one using Prophet, and compare their 
# performance in forecasting. We train on data from Jan - Nov and test on data 
# in Dec
# =============================================================================

import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import sktime
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import MSTL
from statsmodels.tsa.seasonal import DecomposeResult

with open('data/df_403east.pickle', 'rb') as f:
    df_east = pickle.load(f)
    
with open('data/df_403west.pickle', 'rb') as f:
    df_west = pickle.load(f)

df_east_train = df_east[:"2021-11"]
df_east_test = df_east["2021-12":]


# Prophet
from prophet import Prophet
m = Prophet()
model = m.fit(df_east_train)


# TBATS
from sktime.forecasting.tbats import TBATS 
from sktime.forecasting.base import ForecastingHorizon
from sktime.performance_metrics.forecasting import *
tbats = TBATS(sp=[24, 24*7], n_jobs=12)
mod_tbats = tbats.fit(df_east_train)
fh = ForecastingHorizon(df_east_test.index, is_relative=False, freq='H')
y_pred = mod_tbats.predict(fh)

fig, ax = plt.subplots(figsize = (10,5))  
df_east["2021-11-15":].plot(title = 'TBATS Forecaster', xlabel = '', ax = ax)
y_pred.plot(ax = ax)
ax.legend(['Actual Values', 'Forecast'])
plt.show()

rmse = MeanSquaredError(square_root=True)
rmse(df_east_test, y_pred)