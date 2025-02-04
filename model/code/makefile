# Recipes
all: ../output/mpcsgammanondurablesonly2001.tex 

include ../../generic.make

# run model file and move outputs
../output/mpcsgammanondurablesonly2001.tex: nk_rebates_mpc_analysis2001.py nk_rebates_mpc_plot2001.py nk_rebates_mpc_model.py nk_rebates_mpc_monthly_ss.py ../input/rel_rebate2001.dta ../input/forecasts2001.dta ../input/jpsexpenditure.parquet ../input/jpsexpenditurereal.parquet  ../input/pceexpenditure.parquet ../input/pceexpenditurereal.parquet ../input/pceexpenditureprice.parquet | ../output
	rm -f ../output/*
	python $<
	python nk_rebates_mpc_plot2001.py

# Create sim link to input files
../input/pce%.parquet: ../../downloaddata/output/pce%.parquet | ../input
	ln -s $< $@	

../input/forecasts2001.dta: ../../forecasting/output/forecasts2001.dta | ../input
	ln -s $< $@	

../input/jps%.parquet: ../../jpsexpenditure/output/jps%.parquet | ../input
	ln -s $< $@	

../input/rel_rebate2001.dta: ../../narrative/output/rel_rebate2001.dta  | ../input
	ln -s $< $@		