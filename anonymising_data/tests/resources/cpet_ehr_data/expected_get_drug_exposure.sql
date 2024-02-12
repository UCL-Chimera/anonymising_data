SELECT
    dre.drug_exposure_id,
	dre.person_id,
    dre.visit_occurrence_id AS visit,
	dre.drug_exposure_start_datetime,
	dre.drug_exposure_end_datetime, 
	(
        SELECT cc.concept_name FROM concept AS cc
        WHERE cc.concept_id = dre.drug_concept_id
            AND cc.concept_name NOT LIKE 'No matching concept'
    ) AS drug_given

FROM drug_exposure AS dre

WHERE
    dre.drug_concept_id IN (35775967, 4239021, 32817)

AND
	dre.person_id IN (1, 325)

ORDER BY dre.person_id 
