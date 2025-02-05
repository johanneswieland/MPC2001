# Recipes
all: ../output/jpsexpenditure.parquet \
			../output/jpsexpenditurereal.parquet


include ../../generic.make

# this is the recipe 
../output/jpsexpenditure.parquet ../output/jpsexpenditurereal.parquet : jpsexpenditure.py jpsbeamapping.py ../input/pceexpenditure.parquet ../input/pceexpenditureprice.parquet ../input/pceexpenditurereal.parquet  | ../output
	python3 $<

../input/%.parquet: ../../downloaddata/output/%.parquet | ../input
	ln -s $< $@
