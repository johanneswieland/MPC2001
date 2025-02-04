# Recipes
all: ../output/spf_rcons.dta\
	../output/levels_SPF0704.dta

include ../../generic.make

../output/spf_rcons.dta: pull_SPF.py
	python3 pull_SPF.py

# this is the recipe 
 ../output/levels_SPF0102.dta : graph_SPF_cons_dist.do ../output/spf_rcons.dta
	stata-se -b run graph_SPF_cons_dist.do
