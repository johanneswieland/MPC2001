# This file loads the CEX 2001 rebate module and processes it for merging with 
# the consumption expenditure files
# The 2001 rebate .csv raw file has a different format than the 2008 rbt.csv
#%%
import pandas as pd
import numpy as np
import os, sys
import re
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(rootpath)
from utilities.mpc_utilities import aggregate_df, fill_missing_by_type


# ------------------------------------------------------------------------
# LOAD THE REBATE FILE
# ------------------------------------------------------------------------

df = pd.read_parquet('../input/TAX.parquet')

dftaxint = df.copy()[['NEWID', 'TAXAMT1']].set_index('NEWID')

#Reshape the data so that each row represents one rebate
# df = df[df.columns.drop(list(df.filter(regex='_')))]
df = df.drop(['TAXQ3', 'TAXQ3_'], axis=1).set_index(['NEWID', 'TAXQ1', 'TAXQ1_'])
df.columns = pd.MultiIndex.from_tuples([[name+flag,num] for name, num, flag in [re.split('(\d)',col, 1) for col in df.columns]])
df = df.stack(level=1).reset_index()
df = df.rename(columns={'level_3':'RBT01NUMBER','TAXAMT':'RBT01AMT','TAXMO':'RBT01MO'})



#Per JPS, drop rows where lead in question is missing or household states they 
# did not receive a rebate unless they report receipt in the second questio.
# This is not super clear from the paper but appears to be what JPS are doing
# based on the replication sample
df = df[(df['TAXQ1_']!='D') | (df['TAXQ1_']!='A')]
# df = df[(df['TAXQ1'])==1]

#Drop rows where rebateamt is missing or zero
df = df[np.isnan(df['RBT01AMT'])==0]
df = df[(df['RBT01AMT'])>0]

#Drop columns with rebate month  of nan
df = df[np.isnan(df['RBT01MO'])==0]

# get all households interview dates
intdate = pd.read_parquet('../input/fmliquarterly.parquet', columns = ['NEWID', 'CUID','INTDATE','INTNUM','RBTINTVIEW_2001'])

# get all households expenditure dates
hhdates = pd.read_parquet('../input/mtbimonthly.parquet', columns = ['DATE', 'NEWID'])

# merge the two and set index to household, date, interview date
hhdates = hhdates.merge(intdate, how='left', left_index=True, right_index=True)

hhdates = hhdates.reset_index().set_index(['CUID','DATE', 'NEWID','INTDATE'])

#%%
# ------------------------------------------------------------------------
# Create DATE and Rebate Number
# ------------------------------------------------------------------------

# frequency at which data is recorded  
timefreq = 'MS'

# Construct rebate year: has to be such that the DATE occurs at or before to 
# interview date (multiple interviews, can cause rebate to appear too early)
df['RBT01YR'] = 2001

# DATE
df['DATE'] = pd.to_datetime(dict(year = df['RBT01YR'], 
                                 month = df['RBT01MO'], 
                                 day = 1))

# ------------------------------------------------------------------------
# Create Dummies from Categories
# ------------------------------------------------------------------------


df['RBT01 INDICATOR'] = True


sum_vars = {'RBT01AMT'}
max_vars = {'RBT01 INDICATOR'}

df = aggregate_df(df, 
                        agg_by={'NEWID', 'DATE'}, 
                        sum=sum_vars, 
                        max=max_vars)


#%%
# merge interview date and number
df = df.merge(intdate[['CUID','INTDATE','INTNUM']], how='left', left_index=True, right_index=True)
#%%
#Drop rebate observations for interview months prior to August and after December since question was not in the field
df = df[(df['INTDATE'] >= '2001-08-01') & (df['INTDATE'] <= '2001-12-01')]

#%%
# we adjust the interview date next, so can no longer use NEWID as identifying index
# since it is tied to an interview date
df = df.reset_index().set_index(['CUID', 'DATE'])
#%%
# ------------------------------------------------------------------------
# Collapse at household - DATE level
# ------------------------------------------------------------------------
#%%
min_vars = {'INTDATE','INTNUM'}


df = aggregate_df(df.reset_index(), 
                        agg_by={ 'CUID', 'DATE'}, 
                        sum=sum_vars, 
                        max=max_vars,
                        min = min_vars)

#%%
# ------------------------------------------------------------------------
# Match DATE to interview date
# ------------------------------------------------------------------------

# Distance between rebate (months)
df['DISTANCE RBT01 ITW'] = (
                            (df['INTDATE'].dt.year - df.index.get_level_values(level='DATE').year)*12 
                         +   df['INTDATE'].dt.month - df.index.get_level_values(level='DATE').month
                         )


# Check if rebate was received in the current reference period
df['WITHIN REF PERIOD'] = (df['DISTANCE RBT01 ITW']>0) & (df['DISTANCE RBT01 ITW']<=3)

# Baseline DATEs
df['MATCHED INTERVIEW'] = df.loc[df['WITHIN REF PERIOD']==True, 'INTDATE']
#%%
# Adjustment (1):
# For these households the rebate was received more than 3 months ago
# the appropriately matched interview is 3 months ago
# but the interview may not exist if the current interview is the first one
# In JPS these cases are handlded differently to PSJM:
# Rebate date is changed to current interview if there was no previous report of a rebate
wrong_date = (df['DISTANCE RBT01 ITW'] == 4) | (df['DISTANCE RBT01 ITW'] == 5)
df['NEWID'] = df.index.get_level_values('CUID') * 10 + df['INTNUM']

cuid_wrong_date = df.loc[wrong_date, ['INTDATE', 'NEWID']].copy()
cuid_wrong_date['NEWID'] = cuid_wrong_date['NEWID'] - 1

has_prev_tax_int = set(cuid_wrong_date['NEWID'].unique()) & set(dftaxint.index.get_level_values('NEWID'))
no_rbt = set(dftaxint[np.isnan(dftaxint['TAXAMT1'])].index.get_level_values('NEWID'))

# create the three cases
has_prev_tax_int_yes_rbt = has_prev_tax_int - no_rbt
has_prev_tax_int_no_rbt = has_prev_tax_int - has_prev_tax_int_yes_rbt
no_prev_tax_int = set(cuid_wrong_date['NEWID'].unique()) - has_prev_tax_int

has_prev_tax_int_no_rbt_index = [[np.floor(val / 10) , val - np.floor(val / 10) * 10 + 1] for val in has_prev_tax_int_no_rbt]
has_prev_tax_int_yes_rbt_index = [[np.floor(val / 10) , val - np.floor(val / 10) * 10 + 1] for val in has_prev_tax_int_yes_rbt]
no_prev_tax_int_index = [[np.floor(val / 10) , val - np.floor(val / 10) * 10 + 1] for val in no_prev_tax_int]


df = df.reset_index().set_index(['CUID','INTNUM'])
# no prev interview, then assign to prev interview
df.loc[pd.MultiIndex.from_tuples(no_prev_tax_int_index), 'MATCHED INTERVIEW'] = df.loc[pd.MultiIndex.from_tuples(no_prev_tax_int_index), 'INTDATE'] - pd.DateOffset(months=3)

# if there is prev interview without rebate, then assume recall error
df.loc[pd.MultiIndex.from_tuples(has_prev_tax_int_no_rbt_index), 'MATCHED INTERVIEW'] = df.loc[pd.MultiIndex.from_tuples(has_prev_tax_int_no_rbt_index), 'INTDATE']

# if tehre is prev interview with rebate, then drop?
df = df.drop(pd.MultiIndex.from_tuples(has_prev_tax_int_yes_rbt_index), axis=0)


df = df.reset_index().set_index(['DATE','CUID'])

# procedure above in some occassions will override valid response, so we correct here
df.loc[df['WITHIN REF PERIOD'], 'MATCHED INTERVIEW'] = df['INTDATE']
#%%
# cuid_wrong_date = df.loc[wrong_date, ['INTDATE']].copy() - pd.DateOffset(months=3)
# cuid_wrong_date = cuid_wrong_date.reset_index()[['CUID','INTDATE','DATE']].drop_duplicates().set_index(['CUID','INTDATE','DATE'])
# match_new_date = df.reset_index()[['CUID','INTDATE']].set_index(['CUID','INTDATE']).merge(cuid_wrong_date, left_index=True, right_index=True)
# match_to_curr_intview = cuid_wrong_date.drop(match_new_date.index, axis=0).reset_index().set_index(['DATE','CUID'])


# # Need to do split based on TAXQ1
# df.loc[match_to_curr_intview.index, 'MATCHED INTERVIEW'] = df['INTDATE'] 

# Adjustment (2):
# check if DATE = interview date
# if so, set interview date is three month after DATE
# but first check if such an interview date exists
match_to_next_intview = (df['DISTANCE RBT01 ITW'] == 0) & (df['INTNUM'] < 5)

df.loc[match_to_next_intview, 'MATCHED INTERVIEW'] = df['INTDATE'] + pd.DateOffset(months=3) 
# df.loc[(df['DISTANCE RBT01 ITW'] == 0) & (df['INTNUM'] == 5), 'MATCHED INTERVIEW'] = pd.NaT 
#%%
# check that we matched all interviews unless we cannot match them to the next or 
# previous interview
assert ((df['MATCHED INTERVIEW'].isna()==False) | (match_to_next_intview.eq(0)) | (match_to_next_intview.eq(0))).all()

# keep only matched interviews:
df = df[df['MATCHED INTERVIEW'].isna()==False]


# rename interview since there is now a distinction when the rebate is reported and what interview we match to
df = df.drop(['INTDATE',   'WITHIN REF PERIOD', 'DISTANCE RBT01 ITW'], axis=1)
df = df.rename({'MATCHED INTERVIEW': 'INTDATE'}, axis=1, errors="raise")


# These variables store the household rebate data
df = df.reset_index()
df['RBT01 DATE'] = df['DATE']
df['RBT01 INTDATE'] = df['INTDATE']

# put matched interview date in index for merging
df = df.set_index(['CUID', 'DATE', 'INTDATE'])

# ------------------------------------------------------------------------
# merge rebate data with all household-date observation and fill in missing values
# do this at household level, monthly, and interview frequency
# ------------------------------------------------------------------------
#%%

for frequency, timevar in {'monthly': 'DATE', 'interview': 'INTDATE', 'cuid': ''}.items():

    # levels of aggregation:
    agg_by = list(filter(None, ['CUID', timevar]))
    min_vars = {'RBT01 DATE', 'RBT01 INTDATE'}


    # aggregates rebates to monthly
    dfagg = aggregate_df(df.reset_index(), 
                               agg_by = agg_by, 
                               sum = sum_vars, 
                               max = max_vars,
                               min = min_vars)

    # merge with all household identifiers
    dfagg = dfagg.merge(hhdates.groupby(agg_by).max(), how='right', left_index=True, right_index=True)

    # if we are in the monthly or interview dataframe
    if timevar:
        # the time the last rebate was received (in monthly or interview) or the first date
        dfagg['LAST RBT01 ' + timevar] = dfagg['RBT01 ' + timevar]

        dfagg = dfagg.drop(min_vars, axis=1)

        # forward fill last dates
        dfagg['LAST RBT01 ' + timevar] = dfagg['LAST RBT01 ' + timevar].groupby('CUID').fillna(method='ffill')

        # fill missing values
        dfagg = fill_missing_by_type(dfagg)

        # Create Leads and Lags of Rebate Set to zero for March/April 2008, missing otherwise
        if frequency =='monthly':
            timeshift = 1           # expenditures are one month apart
        elif frequency =='interview':   
            timeshift = 3           # interviews are three months apart

        lagnum = int(6 / timeshift)
        leadnum = int(3 / timeshift)           

        # these are the variables we create lags of
        laglist = ['RBT01 INDICATOR','RBT01AMT']
        dfshift = dfagg[laglist].reset_index()

        for i in range(-leadnum,lagnum+1):

            if i==0:
                continue
            elif i<0:
                prefix = 'LEAD'
            elif i>0:
                prefix = 'LAG'

            dflag = dfshift.copy()
            dflag[timevar] = dflag[timevar] + pd.DateOffset(months=i*timeshift)
            dflag = dflag.set_index(['CUID',timevar]).add_prefix(prefix + str(abs(i)))

            # merge with data
            dfagg = dfagg.join(dflag)
        
                     
    # if we are in the household dataframe
    else:
        # since we take the min, these are the first rebate date
        for var in min_vars:
            dfagg = dfagg.rename(columns={var: 'FIRST ' + var})
    
        # fill missing values
        dfagg = fill_missing_by_type(dfagg)

        # for household totals rename the variables: totals for sums, ever for maxes
        for var in dfagg.columns:
            if dfagg[var].dtype in ['int64', 'float64']:
                dfagg = dfagg.rename(columns={var: 'TOTAL ' + var}) 

            elif dfagg[var].dtype in ['bool', 'object']:     
                dfagg = dfagg.rename(columns={var: 'EVER ' + var}) 

     
    # save file as parquet
    dfagg.to_parquet('../output/rebate2001' + frequency + '.parquet')
    
   

#%%
