
# %%

#%% Packages
import pandas as pd
import requests
import io
import numpy as np
from time import strptime



#%%  Download all sheets

url = 'https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/survey-of-professional-forecasters/data-files/files/individual_rconsum.xlsx'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # This will raise an error if the download failed

# Convert the response content into a BytesIO object
data = io.BytesIO(response.content)

# Read the Excel file into a DataFrame
df = pd.read_excel(data)




#%% Labels industries

df['INDUSTRY_LABEL'] = 'Financial Service Provider'
df.loc[df['INDUSTRY']== 2,'INDUSTRY_LABEL'] = 'Non-Financial Service Provider'
df.loc[df['INDUSTRY']== 3,'INDUSTRY_LABEL'] = "Unknown"
df.loc[df['INDUSTRY']== np.nan,'INDUSTRY_LABEL'] = "Unknown"

# %%

df.to_stata('../output/spf_rcons.dta')
df.to_csv('../report/spf_rcons.csv')


# %%
