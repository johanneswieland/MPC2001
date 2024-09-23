## Definitions

# Folders we will be looking for in the task directory
folders := ../input ../output 

# This generates the list of processed data files and figures

input= \
	 ../input/pce_apparel_health.csv \
	 ../input/rebates.xlsx \
	 ../input/cndur_jpscat.dta

outputdata =  	   ../output/narrative_data.dta

outputnarrative =  ../output/fig_cy_combo01.eps \
				   ../output/fig_rebates01.eps \
				   ../output/fig_pce_type01.eps \
				   ../output/fig_pconsnorm_combo01.eps \
				   ../output/fig_ffrante_combo01.eps 
	 

# Recipes
all: $(folders) $(input) $(outputdata) $(outputnarrative)


# Create folders if they do not already exist
$(folders):
	mkdir $@

../input/rebates.xlsx :  | ../input
		if [ -e ../../external_data/$(@F) ] ; then ln -s ../../external_data/$(@F) $@ ; else exit 1; fi	

../input/pce_apparel_health.csv:  | ../input
		if [ -e ../../downloaddata/output/$(@F) ] ; then ln -s ../../downloaddata/output/$(@F) $@ ; else exit 1; fi	

../input/cndur_jpscat.dta:	  | ../input
		if [ -e ../../forecasting/output/$(@F) ] ; then ln -s ../../forecasting/output/$(@F) $@ ; else exit 1; fi	

$(outputdata): build_narrative_data.do $(input)
	stata-se -b run $<

$(outputnarrative): narrative_graphs.do $(outputdata)
	stata-se -b run $<	