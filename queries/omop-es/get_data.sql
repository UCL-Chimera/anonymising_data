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
        SELECT cc.concept_name FROM hic_cc_002.concept AS cc
        WHERE cc.concept_id = m.value_as_concept_id
            AND cc.concept_name NOT LIKE 'No matching concept'
    ) AS value_as_string,
    :FILL_YEAR: - p.year_of_birth AS age,
    p.gender_source_value AS gender,
    p.race_source_value AS ethnicity
FROM hic_cc_002.measurement AS m

INNER JOIN hic_cc_002.person AS p
    ON m.person_id = p.person_id

INNER JOIN hic_cc_002.concept AS c
    ON c.concept_id = m.measurement_concept_id

INNER JOIN hic_cc_002.visit_occurrence AS v
    ON v.visit_occurrence_id = m.visit_occurrence_id
WHERE

    m.measurement_concept_id IN :FILL_CONCEPT:

ORDER BY m.person_id
--LIMIT 10
