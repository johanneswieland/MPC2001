## Definitions

# Folders we will be looking for in the task directory
folders := ../input ../output

# This generates the list of processed data files and figures
input = ../input/pceexpenditure.parquet \
		../input/pceexpenditureprice.parquet \
		../input/pceexpenditurereal.parquet 

output = ../output/jpsexpenditure.parquet \
			../output/jpsexpenditurereal.parquet
		 

# Recipes
all: $(folders) $(input) $(output)

# Create folders if they do not already exist
$(folders):
	mkdir $@

# Link Inputs
$(input): | ../input
	if [ -e ../../downloaddata/output/$(@F) ] ; then ln -s ../../downloaddata/output/$(@F) $@ ; else exit 1; fi	

# this is the recipe 
$(output) : jpsexpenditure.py $(input)
	python3 $<
