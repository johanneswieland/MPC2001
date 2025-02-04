# Recipes
all: ../output/checkforsmoothing.txt

input ../../generic.make

# testing for smoothing
../output/checkforsmoothing.txt: checkforsmoothing.py $(input)
	python $<

../input/mtbimonthly.parquet: ../createconsumptionvariables/output/mtbimonthly.parquet | ../input
	ln -s $< $@