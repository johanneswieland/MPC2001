
drop _all
clear all

set more 1

capture log close

set scheme s1color

use ../output/completedata_for_forecasting.dta

drop if mdate>=m(2020m1) | mdate < m(1984m1)

gen dum911 = 0
replace dum911 = 1 if mdate==m(2001m9)


********************************************************************************
* I. CREATE FORECASTS - A, B, C, and D baseline
********************************************************************************

********************************************************************************
*A.  Exogenous recession and consumer sentiment
********************************************************************************

local lagcontrols L(1/6).lrcndur_jpscat L(1/6).lrdisp_income L(1/6).lpcons ///
   L(1/6).recession L(1/6).umcsent L.dum911
   
local lagcontrols_norecession L(1/6).lrcndur_jpscat L(1/6).lrdisp_income L(1/6).lpcons  ///
   L(1/6).umcsent  L.dum911

reg lrcndur_jpscat `lagcontrols' recession umcsent dum911

estimates store consreg

reg lrdisp_income `lagcontrols'  recession umcsent dum911

estimates store yreg

reg lpcons `lagcontrols' recession umcsent dum911

estimates store preg

reg umcsent `lagcontrols' recession dum911

estimates store sentreg

forecast create mymodel
forecast estimates consreg
forecast estimates yreg
forecast estimates preg

forecast exogenous recession umcsent dum911

forecast solve, begin(m(2001m6)) end(m(2002m12)) suffix(forA) simulate(betas, statistic(stddev,  suffix(forA_sd)) reps(100))

replace dum911 = 0 if mdate==m(2001m9)
forecast solve, begin(m(2001m6)) end(m(2002m12)) suffix(forAno911) simulate(betas, statistic(stddev,  suffix(forA_sdno911)) reps(100))
replace dum911 = 1 if mdate==m(2001m9)

gen diff911 = lrcndur_jpscatforA - lrcndur_jpscatforAno911
egen sum911 = sum(diff911) if mdate<=ym(2001,12)
su rcndur_jpscat if mdate==ym(2001,5)
replace diff911 = diff911 * `=r(mean)' if mdate==ym(2001,9)
replace sum911 = sum911 * `=r(mean)' if mdate==ym(2001,9)
su diff911 sum911 if mdate==ym(2001,9)
drop diff911 sum911


********************************************************************************
* B. Endogenous consumer sentiment, with recession dummy
********************************************************************************

reg lrcndur_jpscat `lagcontrols' umcsent recession dum911

estimates store consreg

reg lrdisp_income `lagcontrols' umcsent recession dum911

estimates store yreg

reg lpcons `lagcontrols' umcsent recession dum911
estimates store preg

reg umcsent `lagcontrols' recession dum911

estimates store sentreg

forecast create mymodelb, replace
forecast estimates consreg
forecast estimates yreg
forecast estimates preg
forecast estimates sentreg

forecast exogenous recession dum911

forecast solve, begin(m(2001m6)) end(m(2002m12)) suffix(forB) 

replace dum911 = 0 if mdate==m(2001m9)
forecast solve, begin(m(2001m6)) end(m(2002m12)) suffix(forBno911)
replace dum911 = 1 if mdate==m(2001m9)

gen diff911 = lrcndur_jpscatforB - lrcndur_jpscatforBno911
egen sum911 = sum(diff911) if mdate<=ym(2001,12)
su rcndur_jpscat if mdate==ym(2001,5)
replace diff911 = diff911 * `=r(mean)' if mdate==ym(2001,9)
replace sum911 = sum911 * `=r(mean)' if mdate==ym(2001,9)
su diff911 sum911 if mdate==ym(2001,9)
drop diff911 sum911

********************************************************************************
* C. Exogenous consumer sentiment, no recession dummy
********************************************************************************

reg lrcndur_jpscat `lagcontrols_norecession' umcsent 

estimates store consreg

reg lrdisp_income `lagcontrols_norecession' umcsent 

estimates store yreg

reg lpcons `lagcontrols_norecession' umcsent 
estimates store preg

reg umcsent `lagcontrols_norecession'

estimates store sentreg

forecast create mymodelc, replace
forecast estimates consreg
forecast estimates yreg
forecast estimates preg

forecast exogenous umcsent

forecast solve, begin(m(2001m6)) end(m(2002m12)) suffix(forC) 

********************************************************************************
* D. Endogenous consumer sentiment, no recession dummy
********************************************************************************

reg lrcndur_jpscat `lagcontrols_norecession' umcsent 

estimates store consreg

reg lrdisp_income `lagcontrols_norecession' umcsent 

estimates store yreg

reg lpcons `lagcontrols_norecession' umcsent 
estimates store preg

reg umcsent `lagcontrols_norecession'

estimates store sentreg

forecast create mymodeld, replace
forecast estimates consreg
forecast estimates yreg
forecast estimates preg
forecast estimates sentreg

forecast solve, begin(m(2001m6)) end(m(2002m12)) suffix(forD) 

********************************************************************************
* II. GRAPH FORECASTS
********************************************************************************

* add greenbook forecasts
local ndshare = 1590.6 / (4532.1 + 1590.6)
gen gbfc = `ndshare' * 0 + (1 - `ndshare') * 1.8 if mdate == ym(2001,5)
replace gbfc = `ndshare' * 1.6 + (1 - `ndshare') * 2.3 if mdate == ym(2001,8)
replace gbfc = `ndshare' * 4.1 + (1 - `ndshare') * 5.1 if mdate == ym(2001,11)
replace gbfc = `ndshare' * 1 + (1 - `ndshare') * 1.9 if mdate == ym(2002,2)

gen jpsnd_gbfc = 309.982 if mdate == ym(2001,2)
replace jpsnd_gbfc = L3.jpsnd_gbfc * (1 + gbfc / 100) ^ 0.25 if mdate <= ym(2002,2) & L3.jpsnd_gbfc<.

assert abs(jpsnd_gbfc - 317.669)<0.01 if mdate == ym(2002,2)

label var jpsnd_gbfc "Greenbook, May 2001"

drop if mdate<m(2001m4)


* Normalize starting value to 0

  scalar umcsent_start = umcsent
 
  replace umcsent = umcsent - umcsent_start
  label var umcsent "Actual"
  foreach model in B D {
  	scalar umcsentfor`model'_start = umcsentfor`model'
	replace umcsentfor`model' = umcsentfor`model' - umcsentfor`model'_start
	label var umcsentfor`model' "Forecast `model'"
  }
 


foreach var in lrcndur_jpscat lrdisp_income lpcons {
	
	scalar `var'_start = `var'
	replace `var' = exp(`var')
	
	
	
	 foreach model in A B C D {
	  	scalar `var'for`model'_start = `var'for`model'
		replace `var'for`model' = exp(`var'for`model')
     }
     
     *Most pessimistic forecast with error bounds (standard deviation of forecasts)
	replace `var'forA_sd = exp(`var'forA_sd)
	gen `var'forA_lowerbound = 	`var'forA - 1.96*`var'forA_sd
	gen `var'forA_upperbound = 	`var'forA + 1.96*`var'forA_sd
	label var `var'forA_lowerbound "Forecast A Lower Bound"
	label var `var'forA_upperbound "Forecast A Upper Bound"

	*Labels	 
	label var `var' "Actual"
	label var `var'forA "Forecast A"
	label var `var'forB "Pessimistic Forecast"
	label var `var'forC "Forecast C"
	label var `var'forD "Regular Forecast"
}





preserve
keep if mdate>=m(2001m4) & mdate<=m(2002m4)

/*
local var lrcndur_jpscat
	tw scatter `var' `var'forA mdate ///
	if mdate>=m(2001m4) & mdate<=m(2002m4), clc(black red blue green gray) ///
  c(l l l l l l) clp(l -) ms(i i i i i i) clw(medthick medthick medthick medthick medthick) ///
  xlabel(, valuelabel) xtitle(Forecast) ytitle("billions of $, monthly rate")   ///
  scale(1.2)  yscale(titlegap(*10)) xlabel(`=ym(2001,4)'(3)`=ym(2002,4)') 
*/

/*
local var lrcndur_jpscat
	tw scatter `var' `var'forA `var'forB `var'forC `var'forD mdate ///
	if mdate>=m(2001m4) & mdate<=m(2002m4), clc(black red blue green gray) ///
  c(l l l l l l) clp(l l - _ -) ms(i i i i i i) clw(medthick medthick medthick medthick medthick) ///
  xlabel(, valuelabel) xtitle(Forecast) ytitle("billions of $, monthly rate")   ///
  scale(1.2)  yscale(titlegap(*10)) xlabel(`=ym(2001,4)'(3)`=ym(2002,4)') 
  graph export ../output/fig_forecasts_cons2001.eps, replace
*/




local var lrcndur_jpscat
	tw scatter `var' `var'forB `var'forD jpsnd_gbfc mdate ///
	if mdate>=m(2001m4) & mdate<=m(2002m4), clc(black red blue green gray) mcolor(black red blue green gray) ///
  c(l l l) clp(l - -) ms(i i i) clw(medthick medthick medthick)  ///
  legend(cols(1) ring(0) position(10)) ytitle("Billion $") scale(1)

graph export ../output/fig_forecasts2001_jpsnondur.eps, replace



local var lrcndur_jpscat
	tw scatter `var' `var'forA `var'forB `var'forC `var'forD mdate ///
	if mdate>=m(2001m4) & mdate<=m(2002m4), clc(black red blue green gray) ///
  c(l l l l l l) clp(l l - _ -) ms(i i i i i i) clw(medthick) title("Real Consumption") name(`var')

local var lrdisp_income
	tw scatter `var' `var'forA `var'forB `var'forC `var'forD mdate  ///
	if mdate>=m(2001m4) & mdate<=m(2002m4), clc(black red blue green gray) ///
  c(l l l l l l) clp(l l - _ -) ms(i i i i i i) clw(medthick) title("Real Disposable Income") name(`var')
  
local var lpcons
	tw scatter `var' `var'forA `var'forB `var'forC `var'forD mdate  ///
	if mdate>=m(2001m4) & mdate<=m(2002m4), clc(black red blue green gray) ///
  c(l l l l l l) clp(l l - _ -) ms(i i i i i i) clw(medthick) title("Consumption Deflator") name(`var')
  
local var umcsent
	tw scatter `var' `var'forB `var'forD mdate  ///
	if mdate>=m(2001m4) & mdate<=m(2002m4), clc(black blue gray) ///
  c(l l l l l l) clp(l - -) ms(i i i i i i) clw(medthick)  title("Consumer Sentiment") name(`var')

 
grc1leg lrcndur_jpscat lrdisp_income lpcons umcsent, cols(2) ysize(4) xsize(4) iscale(0.7) ///
  legendfrom(lrcndur_jpscat) name(forecasts)
 

  graph export ../output/fig_forecasts2001.eps, replace

restore 

 foreach ending in "forA" "forB" "forC" "forD"{
	  	
	rename lrcndur_jpscat`ending' rcndur_jpscat`ending'
     }
     
//  save ../output/forecasts2001.dta, replace  
 
 
keep mdate rcndur_jpscatforA  rcndur_jpscatforB  
save ../output/forecasts2001.dta, replace  

