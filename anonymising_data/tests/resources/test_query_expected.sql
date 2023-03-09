SELECT
    c.concept_name AS measurement_type,
    m.person_id,
    m.measurement_datetime,
    m.value_as_number,
	m.unit_source_value AS units,
    (
        SELECT cc.concept_name FROM concept AS cc
        WHERE cc.concept_id = m.value_as_concept_id
            AND cc.concept_name NOT LIKE 'No matching concept'
    ) AS value_as_string,
    2000 - p.year_of_birth AS age,
    p.gender_source_value AS gender,
    p.race_source_value AS ethnicity
FROM measurement AS m

INNER JOIN person AS p
    ON m.person_id = p.person_id

INNER JOIN concept AS c
    ON c.concept_id = m.measurement_concept_id

WHERE

    m.measurement_concept_id IN (1, 23, 5872)

ORDER BY m.person_id
