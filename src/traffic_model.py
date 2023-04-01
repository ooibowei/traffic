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
    
# We take a square-root transform to have positive forecast values
# TBATS (East)
df_east_train = np.sqrt(df_east[:'2021-11'])
df_east_test = np.sqrt(df_east['2021-12':])

tbats_e = tbats.TBATS(seasonal_periods=[24, 24*7])
mod_tbats_e = tbats_e.fit(df_east_train)
pickle.dump(mod_tbats_e, open('src/mod_tbats_e.pkl', 'wb'))
mod_tbats_e = pickle.load(open('src/mod_tbats_e.pkl', 'rb'))
yhat_tbats_e, yhat_tbats_e_conf = mod_tbats_e.forecast(steps=24*31, confidence_level=0.95)


# Prophet (East)
df_eastp = np.sqrt(df_east).rename(columns={'volume': 'y'})
df_eastp['ds'] = df_eastp.index
df_eastp_train = df_eastp[:'2021-11']
df_eastp_test = df_eastp['2021-12':]

prophet_e = Prophet()
mod_prophet_e = prophet_e.fit(df_eastp_train)
pickle.dump(mod_prophet_e, open('src/mod_prophet_e.pkl', 'wb'))
mod_prophet_e = pickle.load(open('src/mod_prophet_e.pkl', 'rb'))
yhat_prophet_e = mod_prophet_e.predict(df_eastp)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
yhat_prophet_etest = yhat_prophet_e.loc[yhat_prophet_e['ds'] >= '2021-12', 'yhat']


# TBATS (West)
df_west_train = np.sqrt(df_west[:'2021-11'])
df_west_test = np.sqrt(df_west['2021-12':])

tbats_w = tbats.TBATS(seasonal_periods=[24, 24*7])
mod_tbats_w = tbats_w.fit(df_west_train)
pickle.dump(mod_tbats_w, open('src/mod_tbats_w.pkl', 'wb'))
mod_tbats_w = pickle.load(open('src/mod_tbats_w.pkl', 'rb'))
yhat_tbats_w, yhat_tbats_w_conf = mod_tbats_w.forecast(steps=24*31, confidence_level=0.95)


# Prophet (West)
df_westp = np.sqrt(df_west).rename(columns={'volume': 'y'})
df_westp['ds'] = df_westp.index
df_westp_train = df_westp[:'2021-11']
df_westp_test = df_westp['2021-12':]

prophet_w = Prophet()
mod_prophet_w = prophet_w.fit(df_westp_train)
pickle.dump(mod_prophet_w, open('src/mod_prophet_w.pkl', 'wb'))
mod_prophet_w = pickle.load(open('src/mod_prophet_w.pkl', 'rb'))
yhat_prophet_w = mod_prophet_w.predict(df_westp)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
yhat_prophet_wtest = yhat_prophet_w.loc[yhat_prophet_w['ds'] >= '2021-12', 'yhat']


# Comparing TBATS and Prophet & final model hyperparameters
print('TBATS RMSE for East is', 
      mean_squared_error(np.square(df_east_test), np.square(yhat_tbats_e), squared=False))
print('Prophet RMSE for East is',
      mean_squared_error(np.square(df_eastp_test['y']), np.square(yhat_prophet_etest), squared=False))
print('TBATS RMSE for West is', 
      mean_squared_error(np.square(df_west_test), np.square(yhat_tbats_w), squared=False))
print('Prophet RMSE for West is', 
      mean_squared_error(np.square(df_westp_test['y']), np.square(yhat_prophet_wtest), squared=False))
print(mod_tbats_e.summary())
print(mod_tbats_w.summary())


# Generate plots with confidence intervals on test set
ax = df_east['2021-11-20':].plot()
pd.DataFrame(np.square(yhat_tbats_e), index=df_east_test.index).plot(ax=ax)
ax.fill_between(df_east_test.index, np.square(yhat_tbats_e_conf['lower_bound']), 
                np.square(yhat_tbats_e_conf['upper_bound']), color='b', alpha=.1)
plt.legend(['Actual', 'Forecast', '95% CI'], loc=2)
plt.title('Hourly volume forecast for East')
plt.savefig('images/east_forecast_test.png', dpi=1200, bbox_inches='tight')
plt.show()

ax = df_west['2021-11-20':].plot()
pd.DataFrame(np.square(yhat_tbats_w), index=df_west_test.index).plot(ax=ax)
ax.fill_between(df_west_test.index, np.square(yhat_tbats_w_conf['lower_bound']), 
                np.square(yhat_tbats_w_conf['upper_bound']), color='b', alpha=.1)
plt.legend(['Actual', 'Forecast', '95% CI'], loc=2)
plt.title('Hourly volume forecast for West')
plt.savefig('images/west_forecast_test.png', dpi=1200, bbox_inches='tight')
plt.show()


# Retrain with full data by modifiying the TBATS package to use the above hyperparameters
# East: Seasonal harmonics (11,6), ARMA (4,5)
# West: Seasonal harmonics (11,6), ARMA (2,5)
import tbats as tbatsmod
f_tbats_e = tbatsmod.TBATS(use_box_cox=None, use_trend=True, use_damped_trend=True,
                           seasonal_periods=[24, 24*7], 
                           use_arma_errors=True)
fmod_tbats_e = f_tbats_e.fit(np.sqrt(df_east))
pickle.dump(fmod_tbats_e, open('src/fmod_tbats_e.pkl', 'wb'))

f_tbats_w = tbatsmod.TBATS(use_box_cox=None, use_trend=True, use_damped_trend=True,
                           seasonal_periods=[24, 24*7], 
                           use_arma_errors=True)
fmod_tbats_w = f_tbats_w.fit(np.sqrt(df_west))
pickle.dump(fmod_tbats_w, open('src/fmod_tbats_w.pkl', 'wb'))


# Final model
print(fmod_tbats_e.summary())
print(fmod_tbats_w.summary())


# Generate out-of-sample forecasts for Jan 22 with confidence intervals 
import tbats
fmod_tbats_e = pickle.load(open('src/fmod_tbats_e.pkl', 'rb'))
fmod_tbats_w = pickle.load(open('src/fmod_tbats_w.pkl', 'rb'))
yhat_jan_e, yhat_jan_e_conf = fmod_tbats_e.forecast(steps=24*31, confidence_level=0.95)
yhat_jan_w, yhat_jan_w_conf = fmod_tbats_w.forecast(steps=24*31, confidence_level=0.95)

jan_dates = pd.date_range('2022-01-01 00:00:00', '2022-01-31 23:00:00', freq='H')

ax = df_east['2021-12-20':].plot()
pd.DataFrame(np.square(yhat_jan_e), index=jan_dates).plot(ax=ax)
ax.fill_between(jan_dates, np.square(yhat_jan_e_conf['lower_bound']), 
                np.square(yhat_jan_e_conf['upper_bound']), color='b', alpha=.1)
plt.legend(['Actual', 'Forecast', '95% CI'], loc=2)
plt.title('Jan 2022 hourly volume forecast for East')
plt.savefig('images/east_forecast.png', dpi=1200, bbox_inches='tight')
plt.show()

ax = df_west['2021-12-20':].plot()
pd.DataFrame(np.square(yhat_jan_w), index=jan_dates).plot(ax=ax)
ax.fill_between(jan_dates, np.square(yhat_jan_w_conf['lower_bound']), 
                np.square(yhat_jan_w_conf['upper_bound']), color='b', alpha=.1)
plt.legend(['Actual', 'Forecast', '95% CI'], loc=2)
plt.title('Jan 2022 hourly volume forecast for West')
plt.savefig('images/west_forecast.png', dpi=1200, bbox_inches='tight')
plt.show()
