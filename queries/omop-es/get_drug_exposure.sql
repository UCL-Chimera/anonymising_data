SELECT
	p.person_id,
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
WHERE

--	p.person_id IN (1,2,4)
	
--AND
dre.drug_concept_id = 35780880  -- 41345719 

