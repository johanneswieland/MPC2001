# Recipes
all: ../output/nipaexpendituresmonthly.parquet \
		../output/nipaexpendituresinterview.parquet \
		../output/nipavariablesinterview.parquet \
		../output/nipavariablesmonthly.parquet

include ../../generic.make

# this is the recipe
../output/nipaexpendituresinterview.parquet ../output/nipaexpendituresmonthly.parquet: nipaexpenditures.py ../input/fmliquarterly.parquet ../input/mtbimonthly_NIPACAT.parquet | ../output
	rm -r ../output
	mkdir ../output
	python3 $<

../output/nipavariablesinterview.parquet ../output/nipavariablesmonthly.parquet: nipamergedata.py ../output/nipaexpendituresinterview.parquet ../output/nipaexpendituresmonthly.parquet ../input/interviewvariables.parquet ../input/cohortvariables.parquet ../input/rebate2001cuid.parquet ../input/rebate2001interview.parquet ../input/rebate2001monthly.parquet | ../output
	python3 $<

# Create sim link to file with downloaded cex data. if statement checks that the file exists
../input/fmliquarterly.parquet: ../../createconsumptionvariables/output/fmliquarterly.parquet | ../input
	ln -s $< $@	

../input/mtbimonthly_NIPACAT.parquet: ../../createconsumptionvariables/output/mtbimonthly_NIPACAT.parquet | ../input
	ln -s $< $@	

../input/%variables.parquet: ../../createfamilycharacteristics/output/%variables.parquet | ../input
	ln -s $< $@

../input/rebate2001%.parquet: ../../processrebatemodule/output/rebate2001%.parquet  | ../input
	ln -s $< $@


