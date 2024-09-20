clear all
set more off
version 16

cap cd ../psmjregressions/code


/*******************************************************************************

Step 0: Preliminaries: Formatting program and Locals for Regressions

*******************************************************************************/


*Formatting for tabulation
cap program drop format_lag
program format_lag ,eclass
	args b V N
	
    
    ereturn post b V 
    ereturn scalar N = N

   
end




local dependentvars_table "lag_ndexp lag_ndpce lag_spce lag_dpce lag_pce" 

local absorbvars "intdate"

local controlvars "age d_num_adults d_perslt18"
local extravar "_Iincdinte* lag_pce lag_mv"

local versionlist `"lag"' 
local exclude2rebate `"v1" ""'
local exclude2rebate `""'

local samplelist `"& everrbt01indicator"'





/*******************************************************************************

Step 1: Pull in data and label variables

*******************************************************************************/
foreach rebatesample in "`samplelist'" {
local regnumber = 1

foreach depvar in `dependentvars_table'{



foreach version in "`versionlist'"{
		

use ../output/psmjsampleinterview_wlabels.dta, clear


*Separate cohort variable for heterogenous TWFE specications
gen firstrbt01intdate_esi = firstrbt01intdate
gen rel_interview = intdate-firstrbt01intdate
replace rel_interview = -9 if rel_interview < -7

egen numrbt01s = sum(rbt01indicator), by(cuid)
tsset cuid intdate

	
		di "If households have two rebates, drop all household observations"
		drop if numrbt01s >1 
	


keep if insample01 


xtset cuid intdate

*Label Dependent Variables
label var lag_sndexp "Strict Non-Durables"
label var lag_ndexp "Nondurables"
label var lag_ndpce "ND Goods"
label var lag_dpce "Durables"
label var lag_spce "Services"
label var lag_pce "Total"
local variablename "`: variable label `depvar''"
label var rbt01indicator "Lead Rebate Indicator"
label var lag1rbt01indicator "Rebate Indicator"

xi gen i.incdinterview 


/*******************************************************************************

Step 2: Regressions

*******************************************************************************/

		
		
		di "`version'"		
 				


        if "`version'" == "lag"{ // Column 2: TWFE with lag
	
	local weighttype "OLS"

				
        noi di "reg  `depvar' rbt01indicator lag1rbt01indicator `controlvars' i.intdate [w=finlwt21] if insample01 `rebatesample', cluster(cuid)"
	reg  `depvar' rbt01indicator lag1rbt01indicator  `controlvars'  i.intdate [w=finlwt21] if insample01 `rebatesample', cluster(cuid)
	
	
	
	
	
        }
	
	 	
	
		

		

	}
				
	*Saves estimate
		qui eststo 
		
	local groups1 `"`groups1' &  \multicolumn{1}{c}{`: variable label `depvar''} "' 
	local regnumber = `regnumber' + 1
}
		
	
	
		local tablename `"Table_bias"'
		local filename `"Table2001_bias"'


	
	

	* this code produces the regression table
	local nregs = 5
	
	local stats_label `"`"Observations"' "'
	
	
	local varorder "rbt01indicator lag1rbt01indicator"
	local order `"`varorder'"' 
	local midrules1 `" \cmidrule(l{.75em}){2-2} \cmidrule(l{.75em}){3-6}"'
		local groups2 `" &  \multicolumn{1}{c}{JPS Definitions} &  \multicolumn{4}{c}{BEA Definitions} "' 

	local groups `" "`groups2'" \\ "`midrules1'" "`groups1'" \\ "'
	local stats "N"
	
	local stats_fmt " %12.0fc"
	
	
	local num_stats: word count `stats' 
	local layout
	forvalues l = 1/`num_stats' {
		local layout `"`layout' "\multicolumn{1}{c}{@}" "'
	}
	local keepvars `"`varorder'"' 
	local dropvars 
	
	local title `"Positive effect of future rebate receipt on current expenditure"'
	
	local notes `"Notes: All regressions include only rebate recipients.   Regressions include interview (time) fixed effects, and household level controls for age, change in number of adults, and change in number of children.Standard errors, in parentheses, are clustered at the household level: $ \:^{*}\:p<0.1,\:\:^{**}\:p<0.05,\:\:^{***}\:p<0.01 $."'
		
	

	local table_preamble `" "\begin{table}[!t] \centering \sisetup{table-format=1.2} \def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}"  "\small \caption{`title'}" "\begin{tabularx}{\hsize}{@{\hskip\tabcolsep\extracolsep\fill}l*{`nregs'}{S}} \midrule""'
	
			local postfoot `"postfoot(`"\hline\hline \end{tabularx} \begin{minipage}{\hsize} \rule{0pt}{9pt} \footnotesize `notes'  \end{minipage} \label{tab:`tablename'} \end{table}"')"'
	
	local prehead `"prehead(`table_preamble' `groups')"'			
	local posthead `"posthead(`"\hline"' `"\\"')"'
	
	local prefoot(" ")
	


	esttab * using "../output/`filename'.tex", rename(tau0 rbt01indicator tau3 lag1rbt01indicator 0b.lag1rbt01indicator#581b.firstrbt01intdate_esi lag1rbt01indicator) replace cells(b(star fmt(a2)) se(par fmt(a2) abs)) starlevels(\$^{*}$ 0.1 \$^{**}$ 0.05 \$^{***}$ 0.01) drop(`dropvars', relax) ///
		keep(`keepvars') `prehead' `posthead' `postfoot' order(`order') label varlabel(`varlabels') stats(`stats', layout(`layout') fmt(`stats_fmt') ////
		labels(`stats_label')) collabels(,none) numbers nomtitles substitute(# `" X "' tabular* tabularx `"{1}{c}{("' `"{1}{L}{("') width(\hsize) eqlabels("" "")
		
		
	
	eststo clear
	
	
	}
	
	
		

	
	
	
	
	
	
	
	
	
	
	
