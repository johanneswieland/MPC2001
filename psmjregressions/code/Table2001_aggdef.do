clear all
set more off

cap cd ../psmjregressions/code


*Formatting for tabulation
cap program drop format_lag
program format_lag ,eclass
	args b V N
	
    
    ereturn post b V 
    ereturn scalar N = N

   
end


/*******************************************************************************

Step 0: Load Data

*******************************************************************************/


use ../output/psmjsampleinterview_wlabels.dta, clear
drop nipa* psmj*

*Separate cohort variable for heterogenous TWFE specications
gen firstrbt01intdate_esi = firstrbt01intdate
gen rel_interview = intdate-firstrbt01intdate
replace rel_interview = -9 if rel_interview < -7

egen numrbt01s = sum(rbt01indicator), by(cuid)
tsset cuid intdate

	
		
	
		di "If households have two rebates, drop all household observations"
		drop if numrbt01s >1 
	





/*******************************************************************************

Step 1: Locals for regressions

*******************************************************************************/





local absorbvars "intdate"





local controlvars "age d_num_adults d_perslt18"
local versionlist `"2SLS" "2SLSlag" "did_imputation"' 
local samplelist `"" "& everrbt01indicator"'

keep if insample01


xtset cuid intdate






/*******************************************************************************

Step 2: Table 2 Column 4 for individual components

*******************************************************************************/


xi gen i.incdinterview




forval i = 1/1{


if `i' == 1{
	
	local dependentvars_table "d_ndexp d_ndpce d_spce d_dpce d_pce"

	local extravar "_Iincdinte* lag_pce lag_mv"
	label var d_sndexp "Strict Non-Durables"
	label var d_ndexp "Nondurables"
	label var d_ndpce "ND Goods"
	label var d_dpce "Durables"
	label var d_spce "Services"
	label var d_pce "Total"
	label var rbt01amt "Rebate Amount"
	label var lag1rbt01amt "Lag Rebate Amount"
	label var rbt01indicator "Rebate Indicator"
	
	

	
}





foreach version in "`versionlist'"{
	local regnumber =  1

foreach rebatesample in "`samplelist'" {

*Change directory to ado files for Boryusak and Jaravel 2021
if "`rebatesample'" ==""{
	
		local rebatename ""
		local rebatetitle ""
		
	}
	else{
		local rebatename "rbtonly"
		local rebatetitle "Rebate Only Sample"
	}

local groups1 ""
foreach depvar in `dependentvars_table' {





local variablename "`: variable label `depvar''"


	if "`version'" == "2SLS"{ // Column 1: TWFE with no lag
			
				
	*Estimates coefficients 
	noi di "ivreghdfe  `depvar' (rbt01amt = rbt01indicator)  `controlvars'  [w=finlwt21] if insample01 `rebatesample', cluster(cuid) absorb(intdate) "
	ivreghdfe  `depvar' (rbt01amt = rbt01indicator)  `controlvars'   [w=finlwt21] if insample01 `rebatesample', cluster(cuid) absorb(intdate)
	
	local filename `"Table_2001_NDcompare`rebatename'"'
	local filename2 `"Table_2001_NDcompare_pres`rebatename'"'
	local varorder "rbt01amt "
		
	}
	
	if "`version'" == "2SLSlag"{ // Column 1: TWFE with lag
			
				
	*Estimates coefficients 
	noi di "ivreghdfe  `depvar' (rbt01amt lag1rbt01amt = rbt01indicator lag1rbt01indicator)  `controlvars'  [w=finlwt21] if insample01 `rebatesample', cluster(cuid) absorb(intdate) "
	ivreghdfe  `depvar' (rbt01amt lag1rbt01amt = rbt01indicator lag1rbt01indicator)   `controlvars'   [w=finlwt21] if insample01 `rebatesample', cluster(cuid) absorb(intdate)
	
	*6 month coefficient incorporates information from lagged spending

	nlcom (2*_b[rbt01amt] + _b[ lag1rbt01amt])
		local temp_mpc6mo: di %3.2f r(b)[1,1]
		local temp_mpc6mo_se: di %3.2f sqrt(r(V)[1,1])
	
	local filename `"Table_2001_NDcompare_wlag`rebatename'"'
	local filename2 `"Table_2001_NDcompare_wlag_pres`rebatename'"'
	local varorder "rbt01amt lag1rbt01amt"

			
	}
	
	if "`version'" == "did_imputation"{ 
			
	*Estimate size of rebate.
	did_imputation rbt01amt cuid intdate firstrbt01intdate [w=finlwt21] if insample01 `rebatesample' , cluster(cuid) fe(`absorbvars' `hhfe') controls(`controlvars' `extra') horizons(0) autosample maxit(10000)
	local rebatecoef = _b[tau0]
	
	*Estimate dollar effect  of rebate indicator
	display "did_imputation `depvar' cuid intdate firstrbt01intdate [w=finlwt21] if insample01 `rebatesample' , cluster(cuid) fe(`absorbvars' `hhfe') controls(`controlvars' `extra') horizons(0) maxit(10000)"
			did_imputation `depvar' cuid intdate firstrbt01intdate [w=finlwt21] if insample01 `rebatesample' , cluster(cuid) fe(`absorbvars' `hhfe') controls(`controlvars' `extra') horizons(0) autosample maxit(10000)
			
	local coef = _b[tau0]
	
	local filename `"Table_2001_NDcompare_BJS`rebatename'"'
	local filename2 `"Table_2001_NDcompare_BJS_pres`rebatename'"'
	
	local temp_mpc: di %3.2f `coef'/`rebatecoef'
	local varorder "rbt01indicator"

	}
	
	
	qui eststo	
	
	if "`version'" == "did_imputation"{ 
		qui estadd local implied_mpc "`temp_mpc'"
	}
	
	if "`version'" == "2SLSlag"{
		
		qui estadd local mpc6 "`temp_mpc6mo'"
		qui estadd local mpc6se "(`temp_mpc6mo_se')"


	}
		
	local groups1 `"`groups1' &  \multicolumn{1}{c}{`: variable label `depvar''} "' 
	local regnumber = `regnumber' + 1
		}

	
	
	




	

	
	
	* this code produces the regression table
	local nregs = 6

	
	
	local order `"`varorder'"' 
	local indicate
	local midrules1 `" \cmidrule(l{.75em}){2-2} \cmidrule(l{.75em}){3-6}"'
		local groups2 `" &  \multicolumn{1}{c}{JPS Definitions} &  \multicolumn{4}{c}{BEA Definitions} "' 

	local groups `" "`groups2'" \\ "`midrules1'" "`groups1'" \\ "'
	local stats "N"
	local stats_fmt " %12.0fc"
	
	
	
	local stats_label `" `"Observations"' "'
	local title `"Household  Spending Response to Rebate by Subcategory: 2SLS `rebatetitle'"'

	if "`version'" == "did_imputation"{ 
		local stats "implied_mpc N"
	local stats_fmt " %12.0fc"
	local stats_label `" `"Implied MPC"' `"Observations"' "'
	local title `"Household  Spending Response to Rebate by Subcategory: BJS"'

	}
	
	if "`version'" == "2SLSlag"{ 
	local stats "mpc6 mpc6se N"
	local stats_fmt " %12.0fc"
	local stats_label `" `"6-Month MPC"' `"6-Month MPC S.E."' `"Observations"' "'
	local title `"Household  Spending Response to Rebate by Subcategory: 2SLS with Lag"'


	}
	local num_stats: word count `stats' 
	local layout
	forvalues l = 1/`num_stats' {
		local layout `"`layout' "\multicolumn{1}{c}{@}" "'
	}
	local keepvars `"`varorder'"' 
	local dropvars 
	

	local tablename `"JPS rep PCE v JPS"'
	local notes `"Notes:  Standard errors, in parentheses, are clustered at the household level. Significance is indicated by: \$ \:^{*}\:p<0.1,\:\:^{**}\:p<0.05,\:\:^{***}\:p<0.01 \$. All regressions include interview (time) fixed effects, as well as household level controls for age, change in number of adults, and change in number of children. The 2SLS results use $ I(Rebate>0)$ and the other regressors as instruments for the rebate amount."'

	


	
	if "`rebatesample'" == ""{
	local table_preamble `" "\begin{table}[!t] \centering \sisetup{table-format=3.2} \def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}" "\caption{`title'}" "\begin{tabularx}{\hsize}{@{\hskip\tabcolsep\extracolsep\fill}l*{`nregs'}{S}}"  "\toprule     \multicolumn{`nregs'}{l}{\textbf{Panel A: Full Sample}} \\ \midrule" "\hline" "'
	local postfoot `"postfoot(`"\hline \end{tabularx} \vspace{5mm}"')"'
	}
	else{
		local table_preamble `" "\vspace{3mm}  \\ \begin{tabularx}{\hsize}{@{\hskip\tabcolsep\extracolsep\fill}l*{`nregs'}{S}}" "\toprule     \multicolumn{`nregs'}{l}{\textbf{Panel B: Rebate Only Sample}} \\ \midrule" "\hline" "'
		local postfoot `"postfoot(`"\hline\hline \end{tabularx} \begin{minipage}{\hsize} \rule{0pt}{9pt} \footnotesize `notes'  \end{minipage} \label{tab:`tablename'} \end{table}"')"'
	}
	if "`version'" == "did_imputation"{ 
		local table_preamble `" "\begin{table}[!t] \centering \sisetup{table-format=3.2} \def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}" "\caption{`title'}" "\begin{tabularx}{\hsize}{@{\hskip\tabcolsep\extracolsep\fill}l*{`nregs'}{S}}"  "\toprule     \multicolumn{`nregs'}{l}{\textbf{Full Sample}} \\ \midrule" "\hline" "'
		local notes `"Notes:  Standard errors, in parentheses, are clustered at the household level. Significance is indicated by: \$ \:^{*}\:p<0.1,\:\:^{**}\:p<0.05,\:\:^{***}\:p<0.01 \$. All regressions include interview (time) fixed effects, as well as household level controls for age, change in number of adults, and change in number of children. "'
		local postfoot `"postfoot(`"\hline\hline \end{tabularx} \begin{minipage}{\hsize} \rule{0pt}{9pt} \footnotesize `notes'  \end{minipage} \label{tab:`tablename'} \end{table}"')"'
	}
	
	local prehead `"prehead(`table_preamble' `groups')"'			
	local posthead `"posthead(`"\hline"' `"\\"')"'
	
	local prefoot(" ")
	
	
	
		esttab * using "../output/`filename'.tex", rename(tau0 rbt01indicator __00000V rbt01indicator) replace cells(b(star fmt(%5.2f)) se(par fmt(%5.2f) abs)) starlevels(\$^{*}$ 0.1 \$^{**}$ 0.05 \$^{***}$ 0.01) drop(`dropvars', relax) ///
		keep(`keepvars') indicate(`indicate') `prehead' `posthead' `postfoot' order(`order') label varlabel(`varlabels') stats(`stats', layout(`layout') fmt(`stats_fmt') ////
		labels(`stats_label')) collabels(,none) numbers nomtitles substitute(# `" X "' tabular* tabularx `"{1}{c}{("' `"{1}{L}{("') width(\hsize)
		
		*Presentation
		local table_preamble `" "\begin{table}[!t] \centering \sisetup{table-format=1.2} \def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"  "\scriptsize" "\begin{tabularx}{\hsize}{@{\hskip\tabcolsep\extracolsep\fill}l*{`nregs'}{S}} \toprule" "'
	
			local postfoot `"postfoot(`"\hline\hline \end{tabularx} \label{tab:`tablename'} \end{table}"')"'
	
	
	
	local prehead `"prehead(`table_preamble' `groups')"'			
	local posthead `"posthead(`"\hline"' `"\\"')"'
	
	local prefoot(" ")
	
	
	
		esttab * using "../output/`filename2'.tex", rename(tau0 rbt01indicator __00000V rbt01indicator) replace cells(b(star fmt(%5.2f)) se(par fmt(%5.2f) abs)) starlevels(\$^{*}$ 0.1 \$^{**}$ 0.05 \$^{***}$ 0.01) drop(`dropvars', relax) ///
		keep(`keepvars') indicate(`indicate') `prehead' `posthead' `postfoot' order(`order') label varlabel(`varlabels') stats(`stats', layout(`layout') fmt(`stats_fmt') ////
		labels(`stats_label')) collabels(,none) numbers nomtitles substitute(# `" X "' tabular* tabularx `"{1}{c}{("' `"{1}{L}{("') width(\hsize)
		
	eststo clear
		}
		}
	
		}		
