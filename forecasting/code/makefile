# Recipes
all: ../output/forecasts2001.dta  ../output/fig_forecasts2001.eps

include ../../generic.make


# run model file and move outputs
../output/forecasts2001.dta ../output/fig_forecasts2001.eps  : build_forecast_data.do forecast2001.do ../input/auxiliary_forecasting_data.csv ../input/rebates.csv  ../input/JPS_consumption_rebate.xlsx | ../output
	stata-se -b run build_forecast_data.do
	stata-se -b run forecast2001.do
	

../input/%.csv: ../../external_data/output/%.csv | ../input
	ln -s $< $@

../input/%.xlsx: ../../external_data/output/%.xlsx | ../input
	ln -s $< $@