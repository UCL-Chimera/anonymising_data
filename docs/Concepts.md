# Concepts

The concepts are taken from the SNOMED vocabulary and use the concept ids available in the [ATHENA](https://athena.ohdsi.org/search-terms/start) vocabulary.

In order to run the query the code needs to determine the ids of the measurements required. This is done using CSV file which uses concept_id as one of the colums.

## Example file

| concept_code | vocabulary_id | concept_id | concept_name | domain_id | Project|Comment |
| --- | --- | --- | --- | --- | --- | --- |
|1963-8|LOINC|3016293|Bicarbonate [Moles/volume] in Serum or Plasma|Measurement|ABG|bicarb POC This is also pulling in lab Bicarbonate at the moment|
|386725007|SNOMED|4302666|Body temperature|Measurement|ABG|


**NOTE** that in this case the concept id is in the third column. At present this is hard coded.