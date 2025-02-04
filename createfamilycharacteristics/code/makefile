# Recipes
all: ../output/cohortvariables.parquet \
		../output/interviewvariables.parquet

include ../../generic.make

# this is the recipe that creates the zip file with cex data  --downloadopt ../input/cexdownloadoptions.yml
 ../output/%.parquet: %.py ../input/fmliquarterly.parquet | ../output
	python $<

../input/fmliquarterly.parquet: ../../createconsumptionvariables/output/fmliquarterly.parquet | ../input
	ln -s $< $@