SELECT
    dre.drug_exposure_id,
	dre.person_id,
    dre.visit_occurrence_id AS visit,
	dre.drug_exposure_start_datetime,
	dre.drug_exposure_end_datetime, 
	(
        SELECT cc.concept_name FROM :FILL_SCHEMA:concept AS cc
        WHERE cc.concept_id = dre.drug_concept_id
            AND cc.concept_name NOT LIKE 'No matching concept'
    ) AS drug_given

FROM :FILL_SCHEMA:drug_exposure AS dre

WHERE
    dre.drug_concept_id IN :FILL_CONCEPT:

AND
	dre.person_id IN :FILL_PERSON_IDS:

ORDER BY dre.person_id 
