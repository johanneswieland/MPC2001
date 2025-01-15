# 2001 MPC Replication Package

Replication code for "Using Macro Counterfactuals to Assess Plausibility: An Illustration using the 2001 Rebate MPCs" by Jacob Orchard, Valerie Ramey, and Johannes Wieland

Tested on MAC and Linux using STATA version 16.1 and Python 3.11.

**The project is set up to work in a MAC or LINUX enivironment (UNIX more generally).** We provide instructions for Windows in the Github repository for the paper [Micro MPCs and Macro Counterfactuals: The Case of the 2008 Rebates](https://github.com/JakeOrchard/MPC2008-Public).

## Permissions

You can use our code with proper attribution.

Please cite as:

Orchard, Jacob, Valerie A. Ramey, and Johannes F. Wieland. Using Macro Counterfactuals to Assess Plausibility: An Illustration using the 2001 Rebate MPCs. Economic Journal, Forthcoming.

### Statement about Rights

   The authors of the manuscript have legitimate access to and permission to use the data used in this manuscript. The authors of the manuscript have documented permission to redistribute/publish the data contained within this replication package. 



# To Run Entire Project

You will need your own FREDKEY and BEA keys to download the source data. Place the FREDKEY in line 34 of `MPC/forecasting/code/build_forecast_data.do` and place the BEA key in line 14 of `MPC/downloaddata/code/pcefromBEA.py` and line 16 of  `MPC/downloaddata/code/pull_pce_detail.py`. 

We use `make` to run the entire project. `cd` into the base directory and run the following commands in your terminal:

1. `make install`
  
2. `make venv`

3. `make`

The first command builds the Python virtual environment, the second command executes the project. 

Once `make` executes successfully, the paper figures and tables are available in the folder `_finaltablesandfigures/output`.

## Expected Running Time

Around 2 hours. 

# Order of Tasks to Create Final Output

This project is divided into a series of subfolders that execute all of the tasks leading to final output beginning with downloaddata and ending with _finaltablesandfigures. Each subfolder contains both a code directory and, once-executed,  input and output directories. The `makefile` in the code folder documents how the inputs are converted in the outputs for the task. The input directory will have symbolic links to output from previous tasks, while the output directroy will include all of the output used by subsequent tasks. 

The `makefile` in the main folder shows the order of execution of the subfolders. The final output for the paper is mostly created in the forecasting, psmjregressions, model, and narrative subfolders. 

# Data Citation

This project code downloads data from the Bureau of Labor Statistics (BLS), the Federal Reserve Bank of Philadelphia (the SPF surveys), the University of Michigan Survey Research Center,  and the Bureau of Economic Analysis (BEA). The user of these replication files will be under the license requirments of these files when they run the replication code.  


## Downloaded Data Citation 

Bureau of Economic Analysis (2000-2002). ‘National income and product accounts’, US
Department of Commerce

Bureau of Labor Statistics (2000-2002). ‘Consumer expenditure survey’, US Department of
Labor.

Federal Reserve Bank of Philadelphia (2001). ‘Second quarter 2001 survey of professional
forecasters’, Survey of Professional Forecasters.

Survey Research Center (2001). ‘Surveys of consumers’, University of Michigan.

## External datasets

All datasets that are not downloaded directly by the code are included in the folder `external_data`. There are also .csv versions of all of the below data files.

| Name        | Source | Citation    | License |
|-------------|-----|---------------|---------------|
|    rebates.xlsx      | Authors and  Shapiro and Slemrod Table 6 and Sahm, Shapiro and Slemrod | Shapiro, and Slemrod (2003), Sahm, Shapiro, Slemord (2012)   | Creative Commons and GNU General Public License v3.0*|
| JPS_consumption_rebate.xlsx     | Authors and BEA | Orchard, Ramey, Wieland (Forthcoming) and BEA (2000-2002)    | Public domain and GNU General Public License v3.0|
| ce-pumd-interview-diary-dictionary.xlsx      | BLS | BLS (2024)      | Public domain|
| BEA_labels.xls      | Authors |    Orchard, Ramey, Wieland (Forthcoming)   | GNU General Public License v3.0|


*Authors use "GNU General Public License v3.0" while Sahm, Shapiro, and Slemord (2012) use the Creative Commons license. The creative commons license is copied in this replication folder under license_sss.


Bureau of Economic Analysis (2000-2002). ‘National income and product accounts’, US
Department of Commerce

Bureau of Labor Statistics (2024). ‘Consumer expenditure survey’, US Department of
Labor.

Orchard, Jacob, Valerie A. Ramey, and Johannes F. Wieland. Using Macro Counterfactuals to Assess Plausibility: An Illustration using the 2001 Rebate MPCs. Economic Journal, Forthcoming.

Sahm, Claudia R, Matthew D Shapiro, and Joel Slemrod, 2012. “Check in the mail
or more in the paycheck: does the effectiveness of fiscal stimulus depend on how it
is delivered?” American Economic Journal: Economic Policy 4(3): 216–50.

Shapiro, Matthew D and Joel Slemrod, 2003b. “Did the 2001 tax rebate stimulate
spending? Evidence from taxpayer surveys.” Tax policy and the economy 17: 83–109.




