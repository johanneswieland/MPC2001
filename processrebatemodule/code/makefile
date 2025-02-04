# Recipes
all: ../output/rebate2001cuid.parquet \
		../output/rebate2001monthly.parquet \
		../output/rebate2001interview.parquet 

include ../../generic.make

# this is the recipe that creates the 2001 rebate files
../output/rebate2001cuid.parquet ../output/rebate2001monthly.parquet ../output/rebate2001interview.parquet: rebate2001.py ../input/fmliquarterly.parquet  ../input/mtbimonthly.parquet  ../input/TAX.parquet | ../output
	python $<

# Create sim link to file RBT file
../input/TAX.parquet: -e ../../appendCEXfiles/output/TAX.parquet | ../input
	ln -s $< $@

# Create sim link to file FMLI file
../input/fmliquarterly.parquet: ../../createconsumptionvariables/output/fmliquarterly.parquet | ../input
	ln -s $< $@ 

../input/fmliquarterly.parquet: ../../createconsumptionvariables/output/mtbimonthly.parquet  | ../input
	ln -s $< $@ 



