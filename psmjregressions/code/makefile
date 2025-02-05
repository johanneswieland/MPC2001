# Recipes
all: ../output/Table_2001_NDCompare.tex\
	 ../output/bea_all.tex

include ../../generic.make

# we first delete the output folders to make sure all data is new 
../output/Table_2001_NDCompare.tex ../output/bea_all.tex:  variablelabels.do Table2001_aggdef.do Table2001_bea_all.do ../input/psmjsampleinterview.dta  ../input/psmjsamplemonthly.dta  ../input/agglabelsnipa.dta ../input/agglabels_levelnames_nipa.dta ../input/agglabelspsmj.dta ../input/BEA_labels.xls  | ../output
#2001 Tables and charts
	stata-se -b run variablelabels.do
	stata-se -b run Table2001_aggdef.do
	stata-se -b run Table2001_bea_all.do


../input/agglabels%.dta: ../../createconsumptionvariables/output/agglabels%.dta | ../input
	ln -s $< $@


../input/BEA_labels.xls : ../../external_data/output/BEA_labels.xls | ../input
	ln -s $< $@


../input/psmjsample%.dta: ../../psmjsample/output/psmjsample%.dta | ../input
	ln -s $< $@