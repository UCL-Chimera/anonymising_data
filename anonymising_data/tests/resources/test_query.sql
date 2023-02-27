SELECT
    c.concept_name AS measurement_type,
    :FILL_YEAR: - p.year_of_birth AS age
FROM :FILL_SCHEMA:.measurement AS m

INNER JOIN :FILL_SCHEMA:.person AS p
    ON m.person_id = p.person_id

WHERE

    m.measurement_concept_id IN :FILL_CONCEPT:

ORDER BY m.person_id
