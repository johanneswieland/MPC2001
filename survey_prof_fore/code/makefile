# Recipes
all: ../output/spf_rcons.dta\
	../output/levels_SPF0102.dta

include ../../generic.make

../output/spf_rcons.dta ../report/spf_rcons.csv: pull_SPF.py | ../output ../report
	python3 pull_SPF.py

# this is the recipe 
 ../output/levels_SPF0102.dta : graph_SPF_cons_dist.do ../output/spf_rcons.dta
	stata-se -b run graph_SPF_cons_dist.do
