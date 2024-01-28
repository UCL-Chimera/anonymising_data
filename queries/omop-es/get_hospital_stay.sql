SELECT
    vo.visit_occurrence_id,
	vo.person_id,
	vo.visit_start_datetime AS hospital_admission_datetime,
	vo.admitting_source_value,
	vo.visit_end_datetime AS a_hospital_discharge_datetime,
	vo.discharge_to_source_value
FROM :FILL_SCHEMA:visit_occurrence AS vo

INNER JOIN :FILL_SCHEMA:person AS p
	ON p.person_id = vo.person_id
	
 WHERE p.person_id IN (1, 2)