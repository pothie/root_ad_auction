# This file adds two additional columns: 'local_hour' and 'state' to 'raw_df.pickle' (test file)
# and saves the new file as 'Time_Update.pickle'
# 'local_hour' stores int which represents the hour in the local area
# 'state' stores string which is the abbreviation of states (eg. OH)
# For reference, it takes 20 mins for 150,000 rows of data 

import pandas as pd
import numpy as np

from dateutil import parser # didnt have this in the previous version

# Read zipcode file and delete 3 or 4 digit zipcodes
ZIP = pd.read_csv('zipcode/zipcode.csv')
zipdf = ZIP[['zip','state','timezone','dst']]
zipdf = zipdf[zipdf.zip > 9999]

# Read test file
df = pd.read_pickle('raw_df.pickle')  

# Combine zipcode file and data file base on zipcode 
test = pd.merge(
       df,
       zipdf,
       left_on='geo_zip',
       right_on='zip',
       how='left'
       )

# Assume default timezone is UTC-6 and affected by daylight saving time 
# Based on the distribution of states
test.loc[test.loc[:,'timezone'].isnull(),'timezone'] = -6
test.loc[test.loc[:,'dst'].isnull(),'dst'] = 1

# Calculate local time and save as int
hours = test['hour']
hours_list = hours.tolist()
hour_num = list(int(x[0:2]) for x in hours_list)
test['local_hour'] = hour_num + test.timezone + test.dst

# Update day and day_of_week 
day = int(test.loc[1,'day'])-1
test.loc[test.loc[:,'local_hour']<0,'day'] = day
dow = parser.parse('April'+ str(day) +',2019').utcnow().strftime("%A")
test.loc[test.loc[:,'local_hour']<0,'day_of_week'] = dow
test.loc[test.loc[:,'local_hour']<0,'local_hour'] +=24 

# Save the updated file as pickle
test.to_pickle('Time_Update.pickle')
