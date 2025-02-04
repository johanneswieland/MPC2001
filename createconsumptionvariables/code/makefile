# Recipes
all: ../output/fmliquarterly.parquet \
	 ../output/mtbi_wnewUCC.parquet  \
	 ../output/mtbimonthly.parquet \
	 ../output/mtbimonthly_NIPACAT.parquet \
	 ../output/agglabelsnipa.dta \
	 ../output/agglabelspsmj.dta \
	 ../output/agglabels_levelnames_nipa.dta 

include ../../generic.make

# this is the recipe that creates the zip file with cex data  --downloadopt ../input/cexdownloadoptions.yml
 ../output/fmliquarterly.parquet : sumFMLIquarterlyconsumption.py ../input/fmli.parquet
	python sumFMLIquarterlyconsumption.py

# Creates new UCC codes
 ../output/mtbi_wnewUCC.parquet : create_new_UCC.py ../input/mtbi.parquet
	python create_new_UCC.py


# Create MTBI monthly files
 ../output/mtbimonthly.parquet ../output/mtbimonthly_NIPACAT.parquet :  aggregateMTBIucc.py  ../input/mtbi.parquet ../input/ucc_category_map.yml ../output/mtbi_wnewUCC.parquet ../input/nipacategories_map.yml ../input/ucc_nipa_map.yml $(downloads)
	python aggregateMTBIucc.py


# Create aggregation labels
 ../output/agglabelsnipa.dta ../output/agglabelspsmj.dta ../output/agglabels_levelnames_nipa.dta  :  aggregation_labels.py   ../input/ucc_category_map.yml  ../input/nipacategories_map.yml ../input/ucc_nipa_map.yml 
	python aggregation_labels.py


../input/ce-pumd-interview-diary-dictionary.xlsx: ../../external_data/output/ce-pumd-interview-diary-dictionary.xlsx | ../input
	ln -s $< $@

# Create sim link to file with downloaded cex data. if statement checks that the file exists
../input/%.parquet: ../../appendCEXfiles/output/%.parquet | ../input
	ln -s $< $@

# Create sim link to file with ucc mappings to expenditure categories
../input/%.yml: ../ucccodemappings/output/%.yml | ../input
	ln -s $< $@	