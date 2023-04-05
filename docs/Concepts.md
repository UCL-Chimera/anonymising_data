# concepts

the concepts are taken from the SNOMED vocabulary and use the concept ids available in the [ATHENA](https://athena.ohdsi.org/search-terms/start) vocabulary.

in order to run the query the code needs to determine the ids of the measurements required. this is done using CSV file which uses concept_id as one of the colums.

## example file

| concept_code | vocabulary_id | concept_id | concept_name | domain_id | Comment |

| ---| ---| ---| ---| ---|
| 400| SNOMED| 1| Body temperature| Measurement| 

note that in this case the concept id is in the third colum. at present this is hard coded.