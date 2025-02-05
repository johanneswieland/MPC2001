# Recipes
all: ../output/fmli.parquet \
		../output/mtbi.parquet \
		../output/TAX.parquet

# Create folders if they do not already exist
include ../../generic.make

# this is the recipe that creates the zip file with cex data  --downloadopt ../input/cexdownloadoptions.yml
../output/fmli.parquet ../output/mtbi.parquet ../output/TAX.parquet: appendCEXfiles.py ../input/cexdownload.zip | ../output
	python3 appendCEXfiles.py

../input/cexdownload.zip: ../../downloaddata/output/cexdownload.zip | ../input
	ln -s $< $@