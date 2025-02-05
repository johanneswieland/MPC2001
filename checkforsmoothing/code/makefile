# Recipes
all: ../output/checkforsmoothing.txt

include ../../generic.make

# testing for smoothing
../output/checkforsmoothing.txt: checkforsmoothing.py ../input/mtbimonthly.parquet | ../output
	python3 $<

../input/mtbimonthly.parquet: ../../createconsumptionvariables/output/mtbimonthly.parquet | ../input
	ln -s $< $@