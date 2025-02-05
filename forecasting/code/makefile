# Recipes
all: ../output/forecasts2001.dta  ../output/fig_forecasts2001.eps

include ../../generic.make


# run model file and move outputs
../output/forecasts2001.dta ../output/fig_forecasts2001.eps ../output/cndur_jpscat.dta ../report/completedata_for_forecasting.csv: build_forecast_data.do forecast2001.do  ../input/JPS_consumption_rebate.xlsx | ../output ../report
	stata-se -b run build_forecast_data.do
	stata-se -b run forecast2001.do

../input/%.csv: ../../external_data/output/%.csv | ../input
	ln -s $< $@

../input/%.xlsx: ../../external_data/output/%.xlsx | ../input
	ln -s $< $@