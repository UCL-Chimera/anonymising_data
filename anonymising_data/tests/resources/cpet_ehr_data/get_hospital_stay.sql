SELECT
    vo.visit_occurrence_id AS visit,
	vo.person_id,
	p.birth_datetime AS age,
    p.gender_source_value AS gender,
    p.race_source_value AS ethnicity,
	vo.visit_start_datetime AS hospital_admission_datetime,
	vo.admitting_source_value,
	vo.visit_end_datetime AS a_hospital_discharge_datetime,
	vo.discharge_to_source_value
FROM :FILL_SCHEMA:visit_occurrence AS vo

INNER JOIN :FILL_SCHEMA:person AS p
	ON p.person_id = vo.person_id

WHERE
	p.person_id IN :FILL_PERSON_IDS:

ORDER BY p.person_id