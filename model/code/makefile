## Definitions

# Folders we will be looking for in the task directory
folders := ../input ../output

# This generates the list of zip files we should see in the input folder 	
input = \
		../input/pceexpenditure.parquet \
		../input/pceexpenditureprice.parquet \
		../input/pceexpenditurereal.parquet \
		../input/forecasts2001.dta 

inputjps = 	../input/jpsexpenditure.parquet \
			../input/jpsexpenditurereal.parquet 	

inputrebate = ../input/rel_rebate2001.dta 

modelfiles = nk_rebates_mpc_model.py \
			 nk_rebates_mpc_monthly_ss.py

# This generates the list of processed data files	
output= ../output/mpcsgammanondurablesonly2001.tex 

# Recipes
all: $(folders) $(input) $(inputjps) $(inputrebate) $(output)
# Create folders if they do not already exist
$(folders):
	mkdir $@

# Create sim link to file with downloaded cex data. if statement checks that the file exists
../input/pceexpenditure.parquet ../input/pceexpenditurereal.parquet ../input/pceexpenditureprice.parquet: | ../input
	if [ -e ../../downloaddata/output/$(@F) ] ; then ln -s ../../downloaddata/output/$(@F) $@ ; else exit 1; fi	

../input/forecasts2001.dta: | ../input
	if [ -e ../../forecasting/output/$(@F) ] ; then ln -s ../../forecasting/output/$(@F) $@ ; else exit 1; fi		

$(inputjps): | ../input
	if [ -e ../../jpsexpenditure/output/$(@F) ] ; then ln -s ../../jpsexpenditure/output/$(@F) $@ ; else exit 1; fi

$(inputrebate): | ../input
	if [ -e ../../narrative/output/$(@F) ] ; then ln -s ../../narrative/output/$(@F) $@ ; else exit 1; fi		

# run model file and move outputs
$(output): nk_rebates_mpc_analysis2001.py nk_rebates_mpc_plot2001.py $(input) $(modelfiles) $(inputrebate)
	rm -f ../output/*
	python $<
	python nk_rebates_mpc_plot2001.py