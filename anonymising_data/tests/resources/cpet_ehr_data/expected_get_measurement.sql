-- create table of measurement_type with measurement value and time
-- for patient, with age, gender and ethnicity
SELECT
    c.concept_name AS measurement_type,
    m.person_id,
    v.visit_occurrence_id AS visit,
    m.measurement_datetime,
    m.value_as_number,
	m.unit_source_value AS units,
    -- if value is not a number it lists the concept_id
    -- look up name if there is a value
    (
        SELECT cc.concept_name FROM concept AS cc
        WHERE cc.concept_id = m.value_as_concept_id
            AND cc.concept_name NOT LIKE 'No matching concept'
    ) AS value_as_string
    
FROM measurement AS m

INNER JOIN concept AS c
    ON c.concept_id = m.measurement_concept_id

INNER JOIN visit_occurrence AS v
    ON v.visit_occurrence_id = m.visit_occurrence_id

WHERE

    m.measurement_concept_id IN (35775967, 4239021, 32817)

AND 

    m.person_id IN :FILL_PERSON_IDS:
    
ORDER BY m.person_id
--LIMIT 10
