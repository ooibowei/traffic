# =============================================================================
# We want to forecast traffic flow in order to facilitate traffic management. 
# For instance, intelligent transport systems can use traffic flow predictions 
# to mitigate congestion at a given junction/road 
# 
# Link: https://www.fhwa.dot.gov/policyinformation/tables/tmasdata/#y21
# Our dataset is obtained from the Department of Transportation.
# The dataset records daily traffic volume, binned by hour for year 2021
# Traffic volume data is collected using a mix of temporary and continuous traffic counting programs
# For this project, we restrict our analysis to:
#     State: Massachusetts
#     Station ID: 403
#     Direction: 3 (East) and 7 (West)
# 
# Possible extensions:
#     Other stations/directions. But missing data
# 
# Challenges: missing data in between, missing weather information
# Weather information: Temperature, rainfall, snowfall, percentage of cloud cover, main description of weather (categorical)
# Holiday: US national holiday/regional holiday
# =============================================================================

import pandas as pd
import numpy as np
import pickle

def year_hr_format(df):
    df['year'] = 2000 + df['year']
    df['hour'] = df['hour'].replace(to_replace='hour_', value='', regex=True).astype(int)
    return(df)


def df_to_ts(df):
    # Rename, combine lanes, convert to long, drop unnecessary columns
    df_agg = (
        df
        .rename(columns=rename_datetime)
        .drop(columns=['record_type', 'state_code', 'f_system', 'day_of_week', 'restrictions'])
        .groupby(['travel_dir','year','month','day', 'station_id'], as_index=False).sum() # Combine travel lanes
        .drop(columns=['travel_lane'])
        .melt(id_vars=['travel_dir', 'year', 'month', 'day', 'station_id'], var_name='hour', value_name='volume')
    )
    # Convert to time series
    df = (
          year_hr_format(df_agg)
          .set_index(pd.to_datetime(df_agg[['year','month','day','hour']]))
          .drop(columns=['year','month','day','hour'])
          .sort_index()
    )
    return df


def fullcount(df):
    df_count = df.groupby(['travel_dir', 'station_id'], as_index=False).agg(vol_count=('volume', 'count'))
    df_fullcount = df_count.loc[df_count['vol_count'] == (365+(pd.Period('2021').is_leap_year))*24].drop(columns=['vol_count'])
    return df_fullcount.values.tolist()


rename_datetime = {'year_record': 'year',
                   'month_record': 'month',
                   'day_record': 'day'}
months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
df_full = pd.concat([pd.read_csv('data/MA_'+m+'_2021 (TMAS).VOL', sep='|') for m in months])
df_full.info
df_ts = df_to_ts(df_full)
print(fullcount(df_ts))

# Station ID: 403, Direction: 3 (East) and 7 (West)
df_east = df_ts[(df_ts['station_id'] == 403) & (df_ts['travel_dir'] == 3)].drop(columns=['travel_dir', 'station_id'])
df_west = df_ts[(df_ts['station_id'] == 403) & (df_ts['travel_dir'] == 7)].drop(columns=['travel_dir', 'station_id'])

with open('data/df_5118east.pickle', 'wb') as f:
    pickle.dump(df_east, f)
    
with open('data/df_5118west.pickle', 'wb') as f:
    pickle.dump(df_west, f)

