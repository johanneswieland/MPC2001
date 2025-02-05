# Recipes
all: ../output/fig_cy_combo01.eps \
				   ../output/fig_rebates01.eps \
				   ../output/fig_pce_type01.eps \
				   ../output/fig_pconsnorm_combo01.eps \
				   ../output/fig_ffrante_combo01.eps 

include ../../generic.make


../output/narrative_data.dta: build_narrative_data.do ../input/rebates.xlsx ../input/pce_apparel_health.csv ../input/cndur_jpscat.dta | ../output
	stata-se -b run $<

../output/fig_cy_combo01.eps  ../output/fig_rebates01.eps  ../output/fig_pce_type01.eps  ../output/fig_pconsnorm_combo01.eps  ../output/fig_ffrante_combo01.eps : narrative_graphs.do ../output/narrative_data.dta
	stata-se -b run $<	

../input/rebates.xlsx : ../../external_data/output/rebates.xlsx | ../input
		ln -s $< $@

../input/pce_apparel_health.csv: ../../downloaddata/output/pce_apparel_health.csv | ../input
		ln -s $< $@

../input/cndur_jpscat.dta: ../../forecasting/output/cndur_jpscat.dta  | ../input
		ln -s $< $@