SELECT
    c.concept_name AS measurement_type,
    2000 - p.year_of_birth AS age
FROM mock_omop_es.measurement AS m

INNER JOIN mock_omop_es.person AS p
    ON m.person_id = p.person_id

WHERE

    m.measurement_concept_id IN (432, 543)

ORDER BY m.person_id
