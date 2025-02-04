## Recipes
all: ../output/cexdownload.zip  \
		../output/pceexpenditure.parquet \
		../output/pce_apparel_health.csv

include ../../generic.make


# this is the recipe that creates the zip file with cex data
../output/cexdownload.zip: downloadfromBLS.py ../input/cexdownloadoptions.yml | ../output
	python3 downloadfromBLS.py --downloadopt ../input/cexdownloadoptions.yml

# this is the recipe that creates PCE expenditure files
../output/pceexpenditure.parquet: pcefromBEA.py | ../output
	python3 pcefromBEA.py

../output/pce_apparel_health.csv: pull_pce_detail.py | ../output
	python3 pull_pce_detail.py

../input/cexdownloadoptions.yml: ../../globaloptions/hand/cexdownloadoptions.yml | ../input
	ln -s $< $@