import pandas as pd
import numpy as np


def processs_keys(item):
    return {'TimeStamp':item.name,'keytype':item['data']['keytype'],'keyname':item['data']['keyname']}

def process_postion(item):
    
    try:
        lat = float(item['data']['values']['latitude'])
        lon = float(item['data']['values']['longitude'])
    except:
        lon = np.nan
        lat = np.nan
    return {'TimeStamp':item.name,'Latitude':lat,'Longitude':lon}

def process_data(file):
    data = pd.read_json(file,lines=True)
    data.set_index('timestamp',inplace=True)
    data.index.name = 'TimeStamp'
    gps = pd.DataFrame.from_records(data[data.message.str.endswith("gps.eng")].apply(process_postion,axis=1)).set_index('TimeStamp')
    keys = pd.DataFrame(list(data[data.message.str.endswith('keystroke.eng')].apply(processs_keys,axis=1)))
    keys.set_index('TimeStamp',inplace=True)
    keys =pd.pivot_table(keys, values='keyname', index=['TimeStamp'],columns=['keytype'],aggfunc='first')
    if not 'benthic' in keys.columns:
        keys['benthic'] =''
    if not 'substrate' in keys.columns:
        keys['substrate'] =''
    benthos =pd.concat([keys['benthic'].resample('1S').first().ffill(),keys['substrate'].resample('1S').first().ffill()], axis=1)
    benthos =benthos.join(keys.loc[~keys.animal.isna(),'animal'],how='outer').sort_index()
    
    benthos.index.name = 'TimeStamp'
    benthos = benthos.join(gps.resample('1S').first().dropna(),how='outer').sort_index()
    benthos['Station'] =int(file.split('_')[2])
    benthos.rename(columns ={'benthic':'Benthic','animal':'Animal','substrate':'Substrate','Latitude':'ShipLatitude',
                             'Longitude':'ShipLongitude'},inplace=True)
    benthos[['Benthic', 'Substrate']] = benthos[['Benthic', 'Substrate']].ffill()
    benthos[['ShipLatitude', 'ShipLongitude']] = benthos[['ShipLatitude', 'ShipLongitude']].interpolate()
    return benthos
