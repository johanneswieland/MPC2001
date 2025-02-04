## Recipes
all: ../output/ucc_category_map.yml \
		../output/level3to2_map.yml \
		../output/psmjcategories_map.yml \
		../output/cexname_conversion.yml \
		../output/nipacategories_map.yml \
		../output/ucc_nipa_map.yml \

include ../../generic.make

# this is the recipe that creates the yml file mapping ucc codes to expenditure
# categories
# %: will repeat this structure for both output files
# $< is first dependency (in this case the python file)
../output/%.yml: %.py | ../output
	python $<
