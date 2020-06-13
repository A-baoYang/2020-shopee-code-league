import pandas as pd
from datetime import datetime
from tqdm import tqdm

def gen_dayHrMin(df, time_col):
    df['day'] = df[time_col].apply(lambda x: int(x.split(' ')[0].split('-')[2]))
    df['hour'] = df[time_col].apply(lambda x: int(x.split(' ')[1].split(':')[0]))
    df['minute'] = df[time_col].apply(lambda x: int(x.split(' ')[1].split(':')[1]))
    df['second'] = df[time_col].apply(lambda x: int(x.split(' ')[1].split(':')[2]))
    df['timeblock'] = (df['day'] - 27) * 24 + df['hour']
    df['min_block'] = (df['day'] - 27) * 24 * 60 + df['hour'] * 60 + df['minute']
    df['sec_block'] = (df['day'] - 27) * 24 * 3600 + df['hour'] * 3600 + df['minute'] * 60 + df['second']
    df = df.sort_values('sec_block')
#     user_clicks.drop(time_col, axis=1, inplace=True)
    return df


df = pd.read_csv('order_brush_order.csv')
print(df.isnull().sum())
print(len(df))
df['orderid'] = df['orderid'].astype(str)
df['shopid'] = df['shopid'].astype(str)
df['userid'] = df['userid'].astype(str)
df = gen_dayHrMin(df, 'event_time')
df = gen_timeblock(df)
df.head()


deemed_records = list()
for shop in tqdm(df.shopid.unique()):
    tmp = df[df['shopid']==shop].sort_values('sec_block')
    for sec in tmp.sec_block.unique():
        concentrate_rate = len(tmp[(tmp['sec_block']>=sec)&(tmp['sec_block']<=sec+3600)].orderid.values) / len(tmp[(tmp['sec_block']>=sec)&(tmp['sec_block']<=sec+3600)].userid.unique())
        if concentrate_rate >= 3:
            print(shop, sec, sec+3600, concentrate_rate)
            tmp[(tmp['sec_block']>=sec)&(tmp['sec_block']<=sec+3600)]
            protion_df = tmp[(tmp['sec_block']>=sec)&(tmp['sec_block']<=sec+3600)].groupby(['userid'])['orderid'].count().reset_index()
            protion_df['portion'] = protion_df['orderid'] / protion_df['orderid'].sum()
            protion_df
            max(protion_df['portion'].values)
            deemed_buyers = protion_df[protion_df['portion']==max(protion_df['portion'].values)].userid.unique()
            deemed_buyers
            for deemed_buyer in deemed_buyers:
                deemed_records.append([shop, deemed_buyer])

                
df_result = pd.DataFrame(deemed_records)
df_result.columns = ['shopid','userid']
df_result.drop_duplicates(inplace=True)
df_result = df_result.groupby('shopid').agg({'userid': '&'.join}).reset_index()

submit = df_result.copy()
for s in tqdm(df.shopid.unique()):
    if s not in df_result.shopid.unique():
        submit = submit.append(pd.DataFrame([[s,0]],columns=['shopid','userid']), ignore_index=True)
        
submit.to_csv('200613_6th_submission.csv', index=0)
