df = pd.read_pickle('clean_df.pickle')

others = list(['CA','AL','ID','NV','NY','VA','FL'])#,'UNKNOWN'])

expand_segment = df['state']

expand_segment = pd.concat([df.auction_id, expand_segment], axis=1)

expand_segment = pd.melt(expand_segment, id_vars = ['auction_id']) 

expand_segment = expand_segment.pivot_table(
        index='auction_id',
        columns='value',
        aggfunc='size'
        )
expand_segment.loc[:,'state_others'] = 0
expand_segment = expand_segment.fillna(0)

for col in expand_segment.columns:
    if col in others:
        expand_segment.loc[:,'state_others'] = expand_segment.loc[:,'state_others'] + expand_segment.loc[:,col]
    elif col =='state_others':
        break
    else:
        expand_segment.rename(columns = {col: 'state_' + col}, inplace=True) 
expand_segment = expand_segment.drop(others,axis=1)

df = pd.merge(
        df, 
        expand_segment, 
        left_on='auction_id', 
        right_index=True
        )
        
df.to_pickle('state_split.pickle')
