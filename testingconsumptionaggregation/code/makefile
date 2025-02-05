# Recipes
all: ../output/testingaggregation.txt

include ../../generic.make

# this is the recipe that creates the zip file with cex data  --downloadopt ../input/cexdownloadoptions.yml
../output/testingaggregation.txt: testingaggregation.py ../input/fmliquarterly.parquet ../input/mtbimonthly.parquet ../input/level3to2_map.yml ../input/cexname_conversion.yml | ../output
	rm -r ../output
	mkdir ../output
	python3 $<

../input/%.yml: ../../ucccodemappings/output/%.yml | ../input
	ln -s $< $@

../input/%.parquet: ../../createconsumptionvariables/output/%.parquet | ../input
	ln -s $< $@