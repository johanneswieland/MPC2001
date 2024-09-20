cap log close
log using bea_all, replace





use ../output/psmjsampleinterview_wlabels.dta, clear
egen numrbt01s = sum(rbt01indicator), by(cuid)
tsset cuid intdate

	

di "If households have two rebates, drop all household observations"
drop if numrbt01s >1 

keep if insample01
gen b_rbt = .
gen b_lag = .
gen se_rbt = .
gen se_lag = .
gen coefname = ""
gen cattype = ""

*Food at home in PCE space should include food on out of town trips
gen d_nipa_foodhome2 = d_nipa_foodhome + d_nipa_food_out

local i = 1
foreach var of varlist d_nipa* d_psmj*{
	
	local len = length("`var'")
	local category = substr("`var'",3,4)
	
	local varname = substr("`var'",8, `len')
	
	sum `var'
	if r(sd) != 0{
	
	 ivreg2 `var' (rbt01amt  = rbt01indicator ) age d_num_adults d_perslt18 i.intdate [w=finlwt21], cluster(cuid)
	
	replace b_rbt = _b[rbt01amt] if _n == `i'
	*replace b_lag = _b[lag1rbt01amt] if _n == `i'
	replace se_rbt = _se[rbt01amt] if _n == `i'
	*replace se_lag = _se[lag1rbt01amt] if _n == `i'
	replace coefname = "`varname'" if _n == `i'
	replace cattype = "`category'" if _n == `i'
	}
	else{
	replace b_rbt = 0 if _n == `i'
	*replace b_lag = 0 if _n == `i'
	replace se_rbt = 0 if _n == `i'
	*replace se_lag = 0 if _n == `i'
	replace coefname = "`varname'" if _n == `i'
	replace cattype = "`category'" if _n == `i'
	}
	local i = `i' +1
	
	
}
*replace cattype = "psmj" if cattype == "psm"


keep coefname cattype b_rbt se_rbt 
order cattype coefname b_rbt se_rbt 
drop if coefname == ""
preserve
use ../input/agglabelsnipa.dta, clear
merge 1:m coefname using ../input/agglabels_levelnames_nipa.dta, keep(1 3)
gen in_PSMJND = ND_PSMJ ~= ""
append using ../input/agglabelspsmj.dta
drop index 
tempfile agglabels
save `agglabels'
restore


merge 1:1 coefname cattype using `agglabels', nogen
replace agg_level = 5 if coefname == "foodhome2"
drop if agg_level == .
sort cattype agg_level coefname
drop _merge

*Merge in BEA labels
preserve
import excel ../input/BEA_labels.xls, firstrow clear
tempfile bealabels
save `bealabels'
restore

merge 1:1 coefname cattype agg_level using `bealabels'



export excel ../output/coefsall_2001, firstrow(variables) replace


*Denote categories with all missing observations 
gen allmiss =  b_rbt == 0 & se_rbt == 0 //Only true for all missing observations

*Creates t-stat
gen tstat = (b_rbt/se_rbt) 


/************************************************************************
Summary Tables
************************************************************************/

gen nondurable = Level2 == "NONDURABLE_NIPA"
gen durable = Level2 == "DURABLE_NIPA"
gen service = Level2 == "SERVICE_NIPA"

local pcelist `"" "& nondurable" "& service"  "& durable"'

estimates drop _all
eststo clear

local i = 1
foreach subcat in "`pcelist'" {
	
// 	reg b_rbt if agg_level == 4 & cattype == "nipa" `subcat' & allmiss == 0
// 	qui eststo
// 	sum b_rbt if agg_level == 4 & cattype == "nipa" `subcat' & in_PSMJ == 1 & allmiss == 0
// 	local rmean = round(r(mean),.001)
// 	qui estadd local row1 `rmean'
// 	sum b_rbt if agg_level == 4 & cattype == "nipa" `subcat' & in_PSMJ == 0 & allmiss == 0
// 	local rmean = round(r(mean),.001)
// 	qui estadd local row2 `rmean'
// 	sum b_rbt if agg_level == 4 & cattype == "nipa" `subcat'  & allmiss == 0
// 	local rmean = round(r(mean),.001)
// 	qui estadd local row3 `rmean'
	
	reg b_rbt if agg_level == 4 & cattype == "nipa" `subcat' & allmiss == 0
	qui eststo
	egen _sumb = sum(b_rbt) if agg_level == 4 & cattype == "nipa" `subcat' & in_PSMJ == 1 & allmiss == 0
	format _sumb %9.2f
	sum _sumb if agg_level == 4 & cattype == "nipa" `subcat' & in_PSMJ == 1 & allmiss == 0
	local sumb = round(r(mean),.001)
	local sumb = strofreal(`sumb',"%12.2f")
	drop _sumb
	qui estadd local row1 `sumb'
	
	
	egen _sumb = sum(b_rbt) if agg_level == 4 & cattype == "nipa" `subcat' & in_PSMJ == 0 & allmiss == 0
	format _sumb %9.2f
	sum _sumb if agg_level == 4 & cattype == "nipa" `subcat' & in_PSMJ == 0 & allmiss == 0
	local sumb = round(r(mean),.001)
	local sumb = strofreal(`sumb',"%12.2f")
	drop _sumb
	qui estadd local row2 `sumb'
	
	egen _sumb = sum(b_rbt) if agg_level == 4 & cattype == "nipa" `subcat' & allmiss == 0
	format _sumb %9.2f
	sum _sumb if agg_level == 4 & cattype == "nipa" `subcat'  & allmiss == 0
	local sumb = round(r(mean),.001)
	local sumb = strofreal(`sumb',"%12.2f")
	drop _sumb
	qui estadd local row3 `sumb'
}
	
	local stats " row1 row2 row3 N"
	local stats_fmt "%9.0f "	
	local stats_label `" `"In JPS ND"' `"Outside JPS ND"' `"All"' `"Observations"' "'

	
	local ncols = 4

	local title `"Sum of Disaggregated MPCs"'

	local notes `"Notes: Average MPC is the average coefficient from 2SLS regressions of BEA subcategories on rebate amount using the indicator for rebate receipt as an instrument. Sum MPC is the sum of all rebate amount coefficients in the specified category.   "'
	local midrules1 `" \cmidrule(l{.75em}){2-2} \cmidrule(l{.75em}){3-3} \cmidrule(l{.75em}){4-4} \cmidrule(l{.75em}){5-5}"'
	local groups2 `" BEA Category &   \multicolumn{1}{c}{All} &  \multicolumn{1}{c}{ND Goods} &  \multicolumn{1}{c}{Services} &  \multicolumn{1}{c}{Durables} "'  
	local groups `" "`groups2'"  "'
	

	local filename `"bea_all"'
	local table_preamble `" "\begin{table}[!t] \centering \sisetup{table-format=3.2} \def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}" "\caption{`title'}" "\begin{tabularx}{\hsize}{@{\hskip\tabcolsep\extracolsep\fill}l*{`ncols'}{S}}" "\hline\hline" "'
	
local postfoot `"postfoot(`"\hline \end{tabularx} \begin{minipage}{\hsize} \rule{0pt}{9pt} \footnotesize `notes'  \end{minipage} \label{tab:`filename'} \end{table}"')"'	
	

	local prehead `"prehead(`table_preamble' `groups')"'			
	local posthead `"posthead( `"\\"')"'
	
	
	local prefoot(" ")

	esttab * using "../output/`filename'.tex", `extra' replace cells(pct(fmt(0) par("" "\%"))) drop(`dropvars', relax)  indicate(`indicate') `prehead' `posthead' `postfoot' label coeflabels(0 "No" 1 "Yes") nonumbers stats(`stats', layout(`layout') fmt(`stats_fmt') labels(`stats_label')) collabels(,none) nomtitles substitute(# `" X "' tabular* tabularx `"{1}{c}{("' `"{1}{L}{("') width(\hsize) 
		

		eststo clear

/********************************************************
Info for text
**********************************************************/


*Number of statistically significant (at the 10 percent level) MPCs
gen significant10 = abs(tstat)  >= 1.645 & tstat != .
gen pos_significant10 = tstat > 1.645 & tstat != .
gen pos_significant10_oneside = tstat > 1.282

gen significant5 = abs(tstat) >= 1.96 & tstat != .
gen pos_significant5 = tstat >= 1.96 & tstat != .
gen pos_significant5_oneside = tstat > 1.645

*summary table of T-Stats
tab pos_significant10 if agg_level == 4 & cattype == "nipa" & allmiss == 0 
tab pos_significant10 if agg_level == 4 & cattype == "nipa" & allmiss == 0 & in_PSMJND
preserve 
bys BEACategoryFull: gen number = _N
keep if number == 1
save ../output/pos_significant.dta, replace
restore

/******************************************************************************
APPENDIX TABLE: Exports all MPCs in table format
********************************************************************************/

*Generates level 2 and level 3 for level 2 and 3 variables

replace Level2 = upper(coefname) if  agg_level == 2
replace Level3 = upper(coefname) if agg_level == 3

replace Level2 = "DURABLE_NIPA" if Level3 == "HOME_DUR" | Level3 == "REC_DUR" | Level3 == "OTHER_DUR" | Level3 == "MV_PARTS"

replace Level2 = "NONDURABLE_NIPA" if Level3 == "CLOTHING" | Level3 == "FOODBEV_HOME" | Level3 == "GASOLINE_CAT" | Level3 == "OTHER_NONDUR"

replace Level2 = "SERVICE_NIPA" if Level3 == "ACC_SERVICE" | Level3 == "FIN_SERVICE_CAT" | Level3 == "OTHER_SERVICE" | Level3 == "REC_SERVICE" | Level3 == "TRANSPORTATION" | Level3 == "HOUSE_NIPA" | Level3 == "HEALTH_NIPA"

*Foodhome2 should replace food at home and food out
replace Level2 = "NONDURABLE_NIPA" if coefname == "foodhome2"
replace Level3 = "FOODBEV_HOME" if coefname == "foodhome2"
replace agg_level = 4 if coefname == "foodhome2"
replace in_PSMJND = 1 if coefname == "foodhome2"
replace BEACategory = "Food at home" if coefname == "foodhome2"
drop if coefname == "foodhome" | coefname == "food_out"
drop if b_rbt == .

*Removes all PSMJ categories and BEA categories with all missing observations 
keep if cattype == "nipa"
drop if b_rbt == 0 & se_rbt == 0 //Only true for all missing observations

keep if BEACategory != ""

*Sorts table so subcategories add up to categories
sort Level2 Level3 agg_level BEACategory

gen BEA1 = BEACategory if agg_level <4
gen BEA4 = BEACategory if agg_level == 4
replace BEA1 = "\textbf{" + BEACategory + "}" if agg_level < 3


forval i = 1/4{
	gen lat`i' = "&"
	label var lat`i' "&"
}

gen end = "\\"
label var end "\\"

gen _b_rbtshort = round(b_rbt,.01)
gen _se_rbtshort = round(se_rbt,.01)
gen b_rbtshort = strofreal(_b_rbtshort,"%12.2f")
gen se_rbtshort = strofreal(_se_rbtshort,"%12.2f")
replace b_rbtshort = "\textbf{" + b_rbtshort + "}" if agg_level < 3
replace se_rbtshort = "\textbf{" + se_rbtshort + "}" if agg_level < 3

replace in_PSMJND = . if agg_level < 4

order BEA1 lat1 BEA4 lat2  b_rbtshort lat3 se_rbtshort lat4 in_PSMJND end
keep  BEA1 lat1 BEA4 lat2  b_rbtshort lat3 se_rbtshort lat4 in_PSMJND end

label var BEA1 "BEA Category"
label var b_rbtshort "MPC"
label var se_rbtshort "S.E."
label var in_PSMJND "JPS (2006) Nondurable"
tostring in_PSMJND, replace
replace in_PSMJND = "No" if in_PSMJND == "0"
replace in_PSMJND = "Yes" if in_PSMJND == "1"
replace in_PSMJND = "" if in_PSMJND == "."

export excel ../output/coefsall_prettytable, firstrow(varlabels) replace



cap log close
