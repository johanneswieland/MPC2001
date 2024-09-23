
# %%

import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import datetime
import pandas_datareader.data as web    
import mpc_utilities as utils



# %%

# ------------------------------------------------------------------------
# Downloads Data from BEA
# ------------------------------------------------------------------------
UserID = '3235FBB2-CE58-418E-8D35-2893BB16F5FB'
TableType = 'NIUnderlyingDetail'
TableName = 'U20305'
Frequency = 'M'
Year = '2000,2001,2002'

#proxies = {'http': 'http://proxy-t.frb.gov:8080', 'https': 'http://proxy-t.frb.gov:8080' }
#headers = {'User-Agent': 'jake.orchard@frb.gov'}



url =   (
        'https://apps.bea.gov/api/data/?'
        + '&UserID=' + UserID 
        + '&method=GetData&'
        + 'DataSetName=' + TableType 
        + '&TableName=' + TableName 
        + '&Frequency=' + Frequency 
        + '&Year=' + Year 
        + '&ResultFormat=json'
        )

beatable = requests.get(url)
# beatable = requests.get(url, proxies = proxies, headers = headers)


# ------------------------------------------------------------------------
# Convert table into dataframe
# ------------------------------------------------------------------------

# converts json to dict so we can accesss the data entries 
datadict = json.loads(beatable.text)['BEAAPI']['Results']['Data']

# this parses the remaining dictionary entries to create a long table
df = pd.DataFrame.from_records(datadict, index=range(len(datadict)))


# ------------------------------------------------------------------------
# Format data frame to time series
# ------------------------------------------------------------------------

# Convert time period to datetime
df['TimePeriod'] =  pd.to_datetime(df['TimePeriod'], format='%YM%m')

# Set panel variables
df.set_index(['LineDescription','TimePeriod'], inplace=True)

# make data numeric
df['DataValue'] = df['DataValue'].replace(',','', regex=True).astype(float)

# convert to monthly and billions of dollars
df['DataValue'] = df['DataValue'] / 12 / 1000

#%%

#--------------------------------------------
#Saves dataframe containing actual
#New and used vehicle expenditure
# Also includes apperal and healthcare
#--------------------------------------------


dfapparel = df.loc['Clothing and footwear'].reset_index()
dfhealth = df.loc['Health care']
dfapparel = dfapparel.rename(columns={"DataValue": "apparel_exp"})
dfhealth = dfhealth.rename(columns={"DataValue": "health_exp"})

dfagg = dfapparel.merge(dfhealth,how ='inner', left_on = 'TimePeriod',right_on = 'TimePeriod')
dfagg = dfagg[['TimePeriod','apparel_exp','health_exp']]



dfagg = dfagg.rename(columns={'TimePeriod':'DATE'})
dfagg = dfagg.set_index('DATE')
dfagg.to_parquet('../output/pce_apparel_health.parquet', index=True)
dfagg.to_csv('../output/pce_apparel_health.csv')
# %%


