# 2001 MPC Replication Package

Replication code for "Using Macro Counterfactuals to Assess Plausibility: An Illustration using the 2001 Rebate MPCs" by Jacob Orchard, Valerie Ramey, and Johannes Wieland

Tested on MAC and Linux using STATA version 16.1 and Python 3.11.

**The project is set up to work in a MAC or LINUX enivironment (UNIX more generally).** We provide instructions for Windows in the Github repository for the paper [Micro MPCs and Macro Counterfactuals: The Case of the 2008 Rebates](https://github.com/JakeOrchard/MPC2008-Public).

## Permissions

You can use our code with proper attribution.

Please cite as:

Orchard, Jacob, Valerie A. Ramey, and Johannes F. Wieland. Using Macro Counterfactuals to Assess Plausibility: An Illustration using the 2001 Rebate MPCs.


# To Run Entire Project

You will need your own FREDKEY and BEA keys to download the source data. Place the FREDKEY in line 34 of `MPC/forecasting/code/build_forecast_data.do` and place the BEA key in line 14 of `MPC/downloaddata/code/pcefromBEA.py`. 

We use `make` to run the entire project. `cd` into the base directory and run the following commands in your terminal:

1. `make venv`

2. `make`

The first command builds the Python virtual environment, the second command executes the project. 

Once `make` executes successfully, the paper figures and tables are available in the folder `_finaltablesandfigures/output`.


# Order of Tasks to Create Final Output

This project is divided into a series of subfolders that execute all of the tasks leading to final output beginning with downloaddata and ending with _finaltablesandfigures. Each subfolder contains both a code directory and, once-executed,  input and output directories. The `makefile` in the code folder documents how the inputs are converted in the outputs for the task. The input directory will have symbolic links to output from previous tasks, while the output directroy will include all of the output used by subsequent tasks. 

The `makefile` in the main folder shows the order of execution of the subfolders. The final output for the paper is mostly created in the forecasting, psmjregressions, model, and narrative subfolders. 

# Data Citation

This project downloads data from the Bureau of Labor Statistics (BLS), and the Bureau of Economic Analysis (BEA). It includes public data from the Federal Reserve Bank of Philadelphia (the SPF surveys) and the Federal Reserve Board (Greenbook). 

Bureau of Economic Analysis (2000-2002). ‘National income and product accounts’, US
Department of Commerce

Bureau of Labor Statistics (2000-2002). ‘Consumer expenditure survey’, US Department of
Labor.

Federal Reserve Bank of Philadelphia (2001). ‘Second quarter 2001 survey of professional
forecasters’, Survey of Professional Forecasters.

Federal Reserve Board of Governors, S. (2001a). ‘Current economic and financial conditions:
Summary and outlook’, May 9, 2001 Greenbook.

Federal Reserve Board of Governors, S. (2001b). ‘Current economic and financial conditions:
Summary and outlook’, September 27, 2001 Greenbook.


