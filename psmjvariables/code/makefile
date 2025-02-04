# Recipes
all: ../output/psmjexpendituresmonthly.parquet \
		../output/psmjexpendituresinterview.parquet \
		../output/psmjvariablesinterview.parquet \
		../output/psmjvariablesmonthly.parquet 

include ../../generic.make

# this is the recipe
../output/psmjexpendituresinterview.parquet ../output/psmjexpendituresmonthly.parquet: psmjexpenditures.py ../input/fmliquarterly.parquet ../input/mtbimonthly.parquet | ../output
	rm -r ../output
	mkdir ../output
	python3 $<

../output/psmjvariablesinterview.parquet ../output/psmjvariablesmonthly.parquet: psmjmergedata.py ../output/psmjexpendituresinterview.parquet ../output/psmjexpendituresmonthly.parquet
	python3 $<

# Create sim link to file with downloaded cex data. if statement checks that the file exists
../input/fmliquarterly.parquet: ../../createconsumptionvariables/output/fmliquarterly.parquet | ../input
	ln -s $< $@	

../input/mtbimonthly.parquet: ../../createconsumptionvariables/output/mtbimonthly.parquet | ../input
	ln -s $< $@	

../input/%variables.parquet: ../../createfamilycharacteristics/output/%variables.parquet | ../input
	ln -s $< $@

../input/rebate2001%.parquet: ../../processrebatemodule/output/rebate2001%.parquet  | ../input
	ln -s $< $@

../input/nipaexpenditures%.parquet : ../../nipavariables/output/nipaexpenditures%.parquet | ../input
	ln -s $< $@



