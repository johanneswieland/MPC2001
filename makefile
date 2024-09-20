# Years for which we download from BLS

all:
	. venv/bin/activate && make -C downloaddata/code
	. venv/bin/activate && make -C appendCEXfiles/code
	. venv/bin/activate && make -C ucccodemappings/code
	. venv/bin/activate && make -C createconsumptionvariables/code
	. venv/bin/activate && make -C checkforsmoothing/code
	. venv/bin/activate && make -C testingconsumptionaggregation/code
	. venv/bin/activate && make -C processrebatemodule/code
	. venv/bin/activate && make -C createfamilycharacteristics/code
	. venv/bin/activate && make -C nipavariables/code
	. venv/bin/activate && make -C psmjvariables/code
	. venv/bin/activate && make -C psmjsample/code
	. venv/bin/activate && make -C _finaltablesandfigures/code

# virtual environment
install: venv
	. venv/bin/activate && pip install -r requirements.txt

venv:
	test -d venv || python3 -m venv venv	

# clean build
clean:
	sh cleanbuild.sh
	make all


# . venv/bin/activate && make -C download_clean_retail/code
# . venv/bin/activate && make -C download_NIPA/code

# . venv/bin/activate && make -C psmjregressions/code
# . venv/bin/activate && make -C descriptive_stats/code
# . venv/bin/activate && make -C graph_nipaVcex/code
# . venv/bin/activate && make -C bea_vehicle_expenditure/code
# . venv/bin/activate && make -C predictaggregateexpenditures/code
# . venv/bin/activate && make -C createvehicletimeseriesgraph/code
# . venv/bin/activate && make -C createrecipientexp_graphs/code
# . venv/bin/activate && make -C createcohortgraph/code
# . venv/bin/activate && make -C pcestatistics/code
# . venv/bin/activate && make -C michigan_survey/code
# . venv/bin/activate && make -C survey_prof_fore/code
# . venv/bin/activate && make -C greenbook_forecast/code
# . venv/bin/activate && make -C forecasting/code
# . venv/bin/activate && make -C graph_forecasts_all/code
# . venv/bin/activate && make -C relativepriceofautos/code
# . venv/bin/activate && make -C jpsexpenditure/code
# . venv/bin/activate && make -C narrative/code
# . venv/bin/activate && make -C model/code
# . venv/bin/activate && make -C montecarlo/code