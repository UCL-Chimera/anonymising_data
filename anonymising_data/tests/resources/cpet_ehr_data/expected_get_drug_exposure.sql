SELECT
	p.person_id,
    vo.visit_a_currents_id AS visit,
	dre.drug_exposure_start_datetime,
	dre.drug_exposure_end_datetime, 
	(
        SELECT cc.concept_name FROM :FILL_SCHEMA:concept AS cc
        WHERE cc.concept_id = dre.drug_concept_id
            AND cc.concept_name NOT LIKE 'No matching concept'
    ) AS drug_given

FROM :FILL_SCHEMA:drug_exposure AS dre

INNER JOIN :FILL_SCHEMA:person AS p
    ON dre.person_id = p.person_id

INNER JOIN :FILL_SCHEMA:person AS p
    ON dre.person_id = vo.visit_occurrence_id    

WHERE
    dre.drug_concept_id IN :FILL_CONCEPT:

AND
	p.person_id IN :FILL_PERSON_IDS:

ORDER BY p.person_id 

