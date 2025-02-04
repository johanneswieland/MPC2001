# Recipes
all: ../output/psmjsampleinterview.parquet \
		../output/psmjsamplemonthly.parquet \
		../output/psmjsampleinterview.dta \
		../output/psmjsamplemonthly.dta 

# this is the recipe that creates the zip file with cex data  --downloadopt ../input/cexdownloadoptions.yml
 ../output/psmjsampleinterview.dta ../output/psmjsampleinterview.parquet ../output/psmjsamplemonthly.dta ../output/psmjsamplemonthly.parquet: psmjsample.py ../input/psmjvariablesinterview.parquet  ../input/psmjvariablesmonthly.parquet | ../output
	rm -f ../output/*
	python3 $<

# Create sim link to file with downloaded cex data. if statement checks that the file exists
../input/%.parquet: ../../psmjvariables/output/%.parquet | ../input
	ln -s $< $@