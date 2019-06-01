# Import libraries
import pandas as pd
from os import listdir
from dateutil import parser

# Test reading data back in
df = pd.read_pickle('raw_df.pickle')  

# Read zipcode file
ZIP = pd.read_csv('zipcode/zipcode.csv')
zipdf = ZIP[['zip','state','timezone','dst']]
zipdf = zipdf[zipdf.zip>9999]

# Add columns 'state','timezone', 'dst'(daylight saving time)
df = pd.merge(
       df,
       zipdf,
       left_on='geo_zip',
       right_on='zip',
       how='left'
       )
       
# If no corresponding zip is found, set it to be in central time
df.loc[df.loc[:,'timezone'].isnull(),'timezone'] = -6
df.loc[df.loc[:,'dst'].isnull(),'dst'] = 1

# Add column 'local_hour'
hours = df['hour']
hours_list = hours.tolist()
hour_num = list(int(x[0:2]) for x in hours_list)
df['local_hour'] = hour_num + df.timezone + df.dst

# Keep day and day_of_week consisent with hour
day = int(df.loc[1,'day'])-1
df.loc[df.loc[:,'local_hour']<0,'day'] = day
dow = parser.parse('April'+ str(day) +',2019').utcnow().strftime("%A")
df.loc[df.loc[:,'local_hour']<0,'day_of_week'] = dow
df.loc[df.loc[:,'local_hour']<0,'local_hour'] +=24 

df.columns[df.isna().any()]

# Replace NA/NaN with the string 'NA'
df = df.fillna(value = {'category': 'NA',
                        'platform_bandwidth': 'NA',
                        'platform_carrier': 'NA',
                        'platform_device_screen_size': 'NA',
                        'creative_type': 'NA'})
    
# Reformat the category column to be one category per column    
expand_category = df['category'].str.split(',', expand = True) 
expand_category = pd.concat([df.auction_id, expand_category], axis=1)

expand_category = pd.melt(expand_category, id_vars = ['auction_id']) 

expand_category = expand_category[expand_category['value'].notnull()]

expand_category = expand_category.pivot_table(
        index='auction_id',
        columns='value',
        aggfunc='size'
        )

expand_category.columns = ['category_' + str(col) for col in expand_category.columns]
expand_category = expand_category.fillna(0)

df = pd.merge(
        df, 
        expand_category, 
        left_on='auction_id', 
        right_index=True
        )

# Reformat the segment column to be one segment per column    
df['segments'] = df['segments'].str.replace(r"\[","")
df['segments'] = df['segments'].str.replace(r"\]","")
    
expand_segment = df['segments'].str.split(', ', expand = True)
expand_segment = pd.concat([df.auction_id, expand_segment], axis=1)

expand_segment = pd.melt(expand_segment, id_vars = ['auction_id']) 

expand_segment = expand_segment[expand_segment['value'].notnull()]

expand_segment = expand_segment.pivot_table(
        index='auction_id',
        columns='value',
        aggfunc='size'
        )

expand_segment.columns = ['segment_' + str(col) for col in expand_segment.columns]
expand_segment = expand_segment.fillna(0)

df = pd.merge(
        df, 
        expand_segment, 
        left_on='auction_id', 
        right_index=True
        )
df.to_pickle('clean_df.pickle')
