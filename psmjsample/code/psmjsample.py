# %%
import pandas as pd
# import mpc_utilities as utils
from statsmodels.formula.api import ols


# MAY WANT TO OUTSOURCE ALL OF THIS INTO A FUNCTION SO WE CAN APPLY IT TO OTHER DATASETS
# Would have to supply input/output file name as a parameter
#Currently computes the 2001 and 2008 rebate samples in the same .py file

# ------------------------------------------------------------------------
# Loading the variables file
# ------------------------------------------------------------------------

df = pd.read_parquet('../input/psmjvariablesinterview.parquet')

# ------------------------------------------------------------------------
# Create sample filters
# ------------------------------------------------------------------------

# There are nine sample filters which PSMJ implement based on JPS (2006, AER, p.1608)
# 
# 1. In waves 2001-2002 and 2001? 
df['Wave_filter01'] = (df.index.get_level_values('INTDATE') >= '2001-01-01') & (df.index.get_level_values('INTDATE') <= '2002-03-31')

# 2. At least one interview during rebate module
# we check whether any interview for a CUID ( groupby(level=1) ) is in this frame
df['Rebate_module_filter01'] = df['EVER RBTINTVIEW_2001']  #df['RBTINTVIEW'].groupby(level=1).transform(any)


# 3. Omits the bottom 1 percent of nondurable consumption expenditures in levels (after adjusting for family size and allowing for a time trend)
# to use the date as a time trend in the regression it has to be in the columns
df['INT_DATE_COPY'] = df.index.get_level_values(1)

# this fits the regression as I understand it from Parker-Johnson-Souleles (2006, p.1608)
fit01 = ols('NDEXP ~ C(FAM_SIZE) + INT_DATE_COPY ', data=df[df['Wave_filter01']==1]).fit() 

# creates residuals and checks if observation are below first percentile for both 2008 and 2001 waves
df['resid01'] = df['NDEXP'][df['Wave_filter01']==1] - fit01.predict()
df['Not_low_expen_filter01'] = (df['resid01']>df['resid01'].quantile(0.01))

# drop the variables we created
df.drop(['resid01','INT_DATE_COPY'], axis = 1, inplace=True)


# 4. HH tenure filter: drop student housing (CUTENURE=6)
df['HH_tenure_filter']  = (df['CUTENURE']!=6)


# 5. Age level filter: between 21 and 85
df['Age_level_filter']  = (df['AGE']>=21)  & (df['AGE']<=85) 


# 6. Age change filter: age change between 0 and 1
df['Age_change_filter'] = ((df['d_AGE']>=0) & (df['d_AGE']<=1)) | (df['d_AGE'].isna()==1)


# 7. Household change filter: absolute number of adults/children changes by less than or equal to 3
df['HH_size_filter'] = ((abs(df['d_NUM_ADULTS'])<=3) & (abs(df['d_PERSLT18'])<=3)) | (df['d_PERSLT18'].isna()==1)



# 8. Drop if any (non-lead/lag/income/nipa) variable or missing

excludelist = ['NEWTRUCKS','NEWPCARS','EDUCA', 'MAINRP', 'VEHINS', 'ENTERT',  'VRNTLO',  'VEHFIN',  'SHELT', 'pcars_n','cars_downpayment','trucks_n','usedautos','usedlighttrucks' ,'mv_parts', 'net_used', 'cars_nu','cars_n', 'home_dur', 'rec_dur', 'other_dur', 'durable_nipa', 'foodbev_home', 'clothing', 'gasoline', 'other_nondur', 'nondurable_nipa', 'house_nipa', 'health_nipa', 'transportation', 'rec_service', 'acc_service', 'fin_service', 'other_service', 'service_nipa','pce', 'tuition','mv_parts_ser', 'sndexp_nipa']
shortlist = ['d_TOTEXP2','d_NDEXP','d_SNDEXP','d_FOODBEVS','FOODBEVS', 'AGE','d_AGE', 'd_NUM_ADULTS','d_PERSLT18','TOTEXP2','NDEXP','SNDEXP','l_TOTEXP2', 'l_FOODBEVS', 'd_l_FOODBEVS', 'd_l_TOTEXP2', 'd_l_NDEXP']


df['Not_missing_filter01'] = df[shortlist].notna().all(axis=1)

# Separate filter for level variables
df['Not_missing_level_filter01'] = df['Not_missing_level_filter'] = df[[col for col in shortlist if (col.startswith('d_') == False)]].notna().all(axis=1)


# looks like an issue with shift:
# test = df.loc[df['Wave_filter01'],:].isna().sum(axis=0)
# l_TOTEXP2              3
# l_TOTEXP_NMV           3
# d_psmj_            12885
# d_psmj_CUID        12885
# d_psmj_ELDERLY     12885
# d_psmj_VEHFIN      12885
# d_VEHFIN           12885
# d_EDUCA            12885
# d_VEHINS           12885
# d_psmj_CLOTHD      12885
# d_psmj_APPAR       12885
# d_psmj_index       12885
# d_CARTKU           12885
#%%
# ------------------------------------------------------------------------
# Combine the sample filters into one and drop all the individual filters
# ------------------------------------------------------------------------

# Combine the filters
for year in {'01'}:
 
   df['INSAMPLELVL'+year] = (
                     df['Wave_filter'+year]              # 1.
                     & df['Rebate_module_filter'+year]   # 2.
                     & df['Not_low_expen_filter'+year]   # 4.
                     & df['HH_tenure_filter']       # 5.
                     & df['Age_level_filter']       # 6.
                     & df['Age_change_filter']      # 7.
                     & df['HH_size_filter']         # 8.
                     & df['Not_missing_level_filter'+year]     # 9.
                  )

   df['INSAMPLE'+year] = (
                     df['INSAMPLELVL'+year]              # 1-8.
                     & df['Not_missing_filter'+year]     # 9.
                  )


   df['INSAMPLE RBT'+year] = (df['INSAMPLE'+year]) & (df['EVER RBT' + year + ' INDICATOR']>=1)



# checking sample size is correct (with the larger sample, there are 3 missing insample and 2 missing rbt)
# print('Checking Sample Size is Unchanged.\n Expect 17229 insample, 28843 insamplelvl, and 10343 insample rbt')
print('Insample = ' + str(df['INSAMPLE01'].sum()))
print('Insamplelvl = ' + str(df['INSAMPLELVL01'].sum()))
print('Insample rbt = ' + str(df['INSAMPLE RBT01'].sum()))
# assert df['INSAMPLE01'].sum() == 12018
# assert df['INSAMPLELVL'].sum() == 28843
# assert df['INSAMPLE RBT01'].sum() == 5875

# Drop all the individual filters
df.drop([colname for colname in df if colname.endswith('_filter')], axis=1, inplace=True)
#%%
# ------------------------------------------------------------------------
# Load monthly data and add sample filter
# ------------------------------------------------------------------------

dfmonthly = pd.read_parquet('../input/psmjvariablesmonthly.parquet')

# keep only 2007-2009
#dfmonthly = dfmonthly.loc[pd.IndexSlice[:,:,'2007':'2009',:],:]

dfmonthly = dfmonthly.merge(df[['INSAMPLE01', 'INSAMPLELVL01', 'INSAMPLE RBT01']], 
                            how='left', left_index=True, right_index=True)

# ------------------------------------------------------------------------
# Save dataset to be used in regression analysis
# ------------------------------------------------------------------------

for frequency, df0 in {'interview': df, 'monthly': dfmonthly}.items():

   # save combined file as csv to output folder and then zip
   df0.to_parquet('../output/psmjsample' + frequency + '.parquet')

   # converts all True/False booleans to numeric
   for col in df0.select_dtypes(include='bool').columns:
      df0[col] = df0[col].astype(int)

   for col in df0.select_dtypes(include='object').columns:
      df0[col] = df0[col].multiply(1)
      df0[col] = df0[col].astype('float64')

   # make all columns and index names lower case
   df0.columns = [col.lower().replace(' ', '') for col in df0.columns ]
   df0.index = df0.index.rename([x.lower() for x in list(df0.index.names)])

   # save as stata and csv
   dates_format = {'intdate': 'tm','firstrbt01date':'tm','firstrbt01intdate':'tm'}
   if frequency=='monthly':
      dates_format['date'] = 'tm'
   
   df0= df0.loc[:,~df0.columns.duplicated()] #Removes duplicates

   df0.to_stata('../output/psmjsample' + frequency + '.dta',
                  convert_dates = dates_format)




# %%
