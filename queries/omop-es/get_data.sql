
SELECT c.concept_name AS measurement_type,
       m.person_id,
	   v.visit_occurrence_id AS visit,
       m.measurement_datetime,
	   m.value_as_number,
	   2023 - p.year_of_birth AS age,
	   p.gender_source_value AS Gender,
	   p.race_source_value AS Ethnicity
FROM hic_cc_002.measurement AS m

INNER JOIN hic_cc_002.person AS p
ON m.person_id = p.person_id

INNER JOIN hic_cc_002.concept AS c
ON c.concept_id = m.measurement_concept_id

INNER JOIN hic_cc_002.visit_occurrence AS v
ON v.visit_occurrence_id = m.visit_occurrence_id
WHERE 
-- 4302666  -- Body temperature
-- 3010421  -- pH of Blood

m.measurement_concept_id IN (3010421, 4302666)
ORDER BY m.person_id 
--LIMIT 10