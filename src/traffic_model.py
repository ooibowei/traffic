import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import tbats
from prophet import Prophet

with open('data/df_403east.pickle', 'rb') as f:
    df_east = pickle.load(f)
    
with open('data/df_403west.pickle', 'rb') as f:
    df_west = pickle.load(f)
    

# TBATS (East)
df_east_train = df_east[:'2021-11']
df_east_test = df_east['2021-12':]

tbats_e = tbats.TBATS(seasonal_periods=[24, 24*7], n_jobs=8)
mod_tbats_e = tbats_e.fit(df_east_train)
pickle.dump(mod_tbats_e, open('src/mod_tbats_e.pkl', 'wb'))
mod_tbats_e = pickle.load(open('src/mod_tbats_e.pkl', 'rb'))
yhat_tbats_e, yhat_tbats_e_conf = mod_tbats_e.forecast(steps=24*31, confidence_level=0.95)


# Prophet (East)
df_eastp = df_east.rename(columns={'volume': 'y'})
df_eastp['ds'] = df_eastp.index
df_eastp_train = df_eastp[:'2021-11']
df_eastp_test = df_eastp['2021-12':]

prophet_e = Prophet()
mod_prophet_e = prophet_e.fit(df_eastp_train)
pickle.dump(mod_prophet_e, open('src/mod_prophet_e.pkl', 'wb'))
mod_tbats_e = pickle.load(open('src/mod_prophet_e.pkl', 'rb'))
yhat_prophet_e = mod_prophet_e.predict(df_eastp)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
yhat_prophet_etest = yhat_prophet_e.loc[yhat_prophet_e['ds'] >= '2021-12', 'yhat']


# TBATS (West)
df_west_train = df_west[:'2021-11']
df_west_test = df_west['2021-12':]

tbats_w = tbats.TBATS(seasonal_periods=[24, 24*7], n_jobs=16)
mod_tbats_w = tbats_w.fit(df_west_train)
pickle.dump(mod_tbats_w, open('src/mod_tbats_w.pkl', 'wb'))
mod_tbats_w = pickle.load(open('src/mod_tbats_w.pkl', 'rb'))
yhat_tbats_w, yhat_tbats_w_conf = mod_tbats_w.forecast(steps=24*31, confidence_level=0.95)


# Prophet (West)
df_westp = df_west.rename(columns={'volume': 'y'})
df_westp['ds'] = df_westp.index
df_westp_train = df_westp[:'2021-11']
df_westp_test = df_westp['2021-12':]

prophet_w = Prophet()
mod_prophet_w = prophet_w.fit(df_westp_train)
pickle.dump(mod_prophet_w, open('src/mod_prophet_w.pkl', 'wb'))
mod_tbats_w = pickle.load(open('src/mod_prophet_w.pkl', 'rb'))
yhat_prophet_w = mod_prophet_w.predict(df_westp)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
yhat_prophet_wtest = yhat_prophet_w.loc[yhat_prophet_w['ds'] >= '2021-12', 'yhat']


# Comparing TBATS and Prophet
print('TBATS RMSE for East is', 
      mean_squared_error(df_east_test, yhat_tbats_e, squared=False))
print('Prophet RMSE for East is',
      mean_squared_error(df_eastp_test['y'], yhat_prophet_etest, squared=False))
print('TBATS RMSE for West is', 
      mean_squared_error(df_west_test, yhat_tbats_w, squared=False))
print('Prophet RMSE for West is', 
      mean_squared_error(df_westp_test['y'], yhat_prophet_wtest, squared=False))


# Generate plots with confidence intervals
ax = df_east['2021-11-20':].plot()
pd.DataFrame(yhat_tbats_e, index=df_east_test.index).plot(ax=ax)
ax.fill_between(df_east_test.index, yhat_tbats_e_conf['lower_bound'], 
                yhat_tbats_e_conf['upper_bound'], color='b', alpha=.1)
plt.legend(['Actual', 'Forecast', '95% CI'], loc=3)
plt.title('Hourly volume forecast for East')
plt.savefig('images/east_forecast.png', dpi=1200, bbox_inches='tight')
plt.show()

ax = df_west['2021-11-20':].plot()
pd.DataFrame(yhat_tbats_w, index=df_west_test.index).plot(ax=ax)
ax.fill_between(df_west_test.index, yhat_tbats_w_conf['lower_bound'], 
                yhat_tbats_w_conf['upper_bound'], color='b', alpha=.1)
plt.legend(['Actual', 'Forecast', '95% CI'], loc=3)
plt.title('Hourly volume forecast for West')
plt.savefig('images/west_forecast.png', dpi=1200, bbox_inches='tight')
plt.show()


# Final model parameters
print(mod_tbats_e.summary())
print(mod_tbats_w.summary())
