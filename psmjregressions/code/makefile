## Definitions

# Folders we will be looking for in the task directory
folders := ../input ../output

# This generates the list of zip files we should see in the input folder 	
input= \
		../input/psmjsampleinterview.dta  \
		../input/psmjsamplemonthly.dta  \
		../input/agglabelsnipa.dta \
		../input/agglabels_levelnames_nipa.dta \
		../input/agglabelspsmj.dta \
		../input/BEA_labels.xls \


# This generates the list of output files
output= \
		../output/Table_2001_NDCompare.tex\
		../output/bea_all.tex


# Recipes
all: $(folders) $(input) $(output)

# Create folders if they do not already exist
$(folders):
	mkdir $@



../input/agglabelsnipa.dta ../input/agglabels_levelnames_nipa.dta ../input/agglabelspsmj.dta:  | ../input
	if [ -e ../../createconsumptionvariables/output/$(@F) ] ; then ln -s ../../createconsumptionvariables/output/$(@F) $@ ; else exit 1; fi	


../input/BEA_labels.xls :  | ../input
	if [ -e ../../external_data/$(@F) ] ; then ln -s ../../external_data/$(@F) $@ ; else exit 1; fi	

# Create sim link to file with downloaded cex data. if statement checks that the file exists
../input/psmjsampleinterview.dta ../input/psmjsamplemonthly.dta: | ../input
	if [ -e ../../psmjsample/output/$(@F) ] ; then ln -s ../../psmjsample/output/$(@F) $@ ; else exit 1; fi	


# we first delete the output folders to make sure all data is new 
$(output):  variablelabels.do Table2001_aggdef.do Table2001_bea_all.do Table2001_bias.do $(input)
#2001 Tables and charts
	stata-se -b run variablelabels.do
	stata-se -b run Table2001_aggdef.do
	stata-se -b run Table2001_bea_all.do
	stata-se -b run Table2001_bias.do