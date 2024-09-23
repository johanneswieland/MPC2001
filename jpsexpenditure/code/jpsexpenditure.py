# %%

import pandas as pd
import numpy as np
from jpsbeamapping import mapping

# %%
# BEA Linenumbers in JPS aggregate:


# %%
df = pd.read_parquet('../input/pceexpenditure.parquet')

# make linenumber numeric and add to index
df['LineNumber'] = pd.to_numeric(df['LineNumber'])
df = df.reset_index().set_index(['LineNumber','LineDescription','TimePeriod']).sort_index()

# check mapping:
# iterate over items in mapping and check whether
for key, value in mapping.items():
    assert df.loc[pd.IndexSlice[value, key, '2001-01-01'], ['DataValue']].count()>0



# apply mapping: extract from df the lines in mapping values and aggregate them
dfsum = df.loc[pd.IndexSlice[list(mapping.values()), :, :]].reset_index()[['TimePeriod', 'DataValue']].groupby('TimePeriod').sum()

# calculatue share of JPS in PCE:
PCE = df.loc[pd.IndexSlice[1,'Personal consumption expenditures',:],'DataValue'].reset_index()[['TimePeriod','DataValue']].set_index('TimePeriod')
share = dfsum / PCE

assert dfsum.loc['1998-01-01','DataValue'] * 12 * 1000 == 3070002, 'JPS 1998-01-01 does not match'
# %%
# price defalator to convert to real 2012 dollars
dfprice = pd.read_parquet('../input/pceexpenditureprice.parquet')
dfnom = pd.read_parquet('../input/pceexpenditure.parquet')

# create chained deflator of nondurable goods and services
nondurserv = ['Nondurable goods', 'Services']
price = dfprice.loc[pd.IndexSlice[nondurserv, :], 'DataValue'].reset_index().set_index(['TimePeriod','LineDescription']).unstack()['DataValue']
nomexp = dfnom.loc[pd.IndexSlice[nondurserv, :], 'DataValue'].reset_index().set_index(['TimePeriod','LineDescription']).unstack()['DataValue']
realexp = nomexp / price * 100

chain_curr = nomexp.sum(axis = 1) / (realexp.shift(periods = 1) * price).sum(axis = 1)
chain_lag = (realexp * price.shift(periods = 1)).sum(axis = 1) / nomexp.shift(periods = 1).sum(axis = 1)

chain_pce = np.sqrt(chain_curr * chain_lag)

basedate = pd.to_datetime('2012-07-01')
realexpsum = nomexp.sum(axis = 1)
# in monthly increments add lagged dfreal value multiplied with current chain_pce
date = pd.to_datetime(basedate) + pd.DateOffset(months = 1)
while date <= pd.to_datetime('2022-12-01'):
    realexpsum.loc[date] = realexpsum.loc[date - pd.DateOffset(months = 1)] * chain_pce.loc[date]
    date = date + pd.DateOffset(months = 1)

date = pd.to_datetime(basedate) - pd.DateOffset(months = 1)
while date >= pd.to_datetime('1959-01-01'):
    realexpsum.loc[date] = realexpsum.loc[date + pd.DateOffset(months = 1)] / chain_pce.loc[date + pd.DateOffset(months = 1)]
    date = date - pd.DateOffset(months = 1)

# assert abs(realexpsum.loc['2022-12-01'] - 1004.779) < 0.01, 'realexpsum 2022-12-01 does not match'

deflator = nomexp.sum(axis = 1) / realexpsum 

# %%
# create and save real JPS series
dfreal = dfsum / deflator.to_frame('DataValue')

dfsum.to_parquet('../output/jpsexpenditure.parquet')
dfreal.to_parquet('../output/jpsexpenditurereal.parquet')

# %%
