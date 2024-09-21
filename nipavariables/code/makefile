## Definitions

# Folders we will be looking for in the task directory
folders := ../input ../output

# This generates the list of zip files we should see in the input folder 	
input= \
		../input/fmliquarterly.parquet \
		../input/mtbimonthly_NIPACAT.parquet \
		../input/cohortvariables.parquet \
		../input/interviewvariables.parquet \
		../input/rebate2001cuid.parquet \
		../input/rebate2001interview.parquet \
		../input/rebate2001monthly.parquet 


# This generates the list of processed data files	
output= \
		../output/nipaexpendituresmonthly.parquet \
		../output/nipaexpendituresinterview.parquet \
		../output/nipavariablesinterview.parquet \
		../output/nipavariablesmonthly.parquet


# Recipes
all: $(folders) $(input) $(output)

# Create folders if they do not already exist
$(folders):
	mkdir $@

# Create sim link to file with downloaded cex data. if statement checks that the file exists
../input/fmliquarterly.parquet ../input/mtbimonthly_NIPACAT.parquet: | ../input
	if [ -e ../../createconsumptionvariables/output/$(@F) ] ; then ln -s ../../createconsumptionvariables/output/$(@F) $@ ; else exit 1; fi	

../input/cohortvariables.parquet  ../input/interviewvariables.parquet:  | ../input
	if [ -e ../../createfamilycharacteristics/output/$(@F) ] ; then ln -s ../../createfamilycharacteristics/output/$(@F) $@ ; else exit 1; fi	

../input/rebate2001cuid.parquet  ../input/rebate2001interview.parquet ../input/rebate2001monthly.parquet:  | ../input
	if [ -e ../../processrebatemodule/output/$(@F) ] ; then ln -s ../../processrebatemodule/output/$(@F) $@ ; else exit 1; fi	

# this is the recipe
../output/nipaexpendituresinterview.parquet ../output/nipaexpendituresmonthly.parquet: nipaexpenditures.py ../input/fmliquarterly.parquet ../input/mtbimonthly_NIPACAT.parquet
	rm -r ../output
	mkdir ../output
	python $<

../output/nipavariablesinterview.parquet ../output/nipavariablesmonthly.parquet: nipamergedata.py ../output/nipaexpendituresinterview.parquet ../output/nipaexpendituresmonthly.parquet $(input)
	python $<
