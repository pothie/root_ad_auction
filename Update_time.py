# This file adds two additional columns: 'local_hour' and 'state' to 'raw_df.pickle' (test file)
# and saves the new file as 'Time_Update.pickle'
# 'local_hour' stores int which represents the hour in the local area
# 'state' stores string which is the abbreviation of states (eg. OH)
# For reference, it takes 20 mins for 150,000 rows of data 

import pandas as pd
import numpy as np

# Read zipcode file and delete 3 or 4 digit zipcodes
ZIP = pd.read_csv('zipcode/zipcode.csv')
zipdf = ZIP[['zip','state','timezone','dst']]
zipdf = zipdf[zipdf.zip > 9999]

# Read test file
test = pd.read_pickle('raw_df.pickle')  

# Record the distinct zipcodes in test_file
# When zip = -1 do not alter local_time and keep state as blank
unique_zip = list(test.geo_zip.unique())
if -1 in unique_zip:
    unique_zip.remove(-1)

# Initialize column 'local_hour' as int with the same value as 'hour'
hours = test['hour']
hours_list = hours.tolist()
hour_num = list(int(x[0:2]) for x in hours_list)
test['local_hour']= hour_num

# Initialize column 'state' as empty string
test['state'] = ''

# Update 'local_hour' with given zipcodes
for user_zip in unique_zip:
    for area_zip in zipdf.zip:
        
        # Find corresponding zipcode
        # if no coresponding zipcode found, use the following zipcode 
        if (user_zip <= area_zip):
            
            # Keep track of rows with user_zip
            temp = test.index[test.geo_zip == user_zip]
            
            # Get timezone and daylight saving time infor from zipdf
            tz = int(zipdf.loc[zipdf.zip == area_zip]['timezone'])
            ds = int(zipdf.loc[zipdf.zip == area_zip]['dst'])
            st = zipdf.loc[zipdf.zip == area_zip]['state']
            
            # Calculate local time
            # If the updated time is negative, which means it goes back to the previous day
            # Update column 'day'
            for ind in temp:
                t = test.loc[ind,'local_hour']+tz+ds
                if t < 0:
                    t = t + 24
                    test.loc[ind,'day'] = str(int(test.loc[ind,'day'])-1)
                test.loc[ind,'local_hour'] = t
            
            # Update column 'state'
            test.loc[temp,'state'] = list(st)
            
            # Zipcode found, move on to the next zipcode in unique_zip
            break  

# Calculate local time given zipcode = -1 or not given (subtract 5 from UTC)
ind_Unknown_zip = test.index[test.state == '']
test.loc[ind_Unknown_zip,'local_hour'] = test.loc[ind_Unknown_zip,'local_hour']-5
# Trace back to the previous day if local_hour < 0
for i in ind_Unknown_zip:
    if test.loc[i,'local_hour'] < 0:
        test.loc[i,'local_hour'] = test.loc[i,'local_hour'] + 24
        test.loc[i,'day'] = str(int(test.loc[i,'day'])-1)
         

# Save the updated file as pickle
test.to_pickle('Time_Update.pickle')
