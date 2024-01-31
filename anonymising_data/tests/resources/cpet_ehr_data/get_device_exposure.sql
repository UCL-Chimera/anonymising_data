SELECT
	de.device_exposure_id,
	p.person_id,
    vo.visit_occurrence_id AS visit,
	de.device_source_value AS oxygen_delivery_device,
	de.device_exposure_start_datetime,
	de.device_exposure_end_datetime

FROM :FILL_SCHEMA:device_exposure AS de

INNER JOIN :FILL_SCHEMA:person AS p
    ON de.person_id = p.person_id

INNER JOIN :FILL_SCHEMA:visit_occurrence AS vo
    ON de.visit_occurrence_id = vo.visit_occurrence_id   
	
WHERE

	p.person_id IN :FILL_PERSON_IDS:

ORDER BY p.person_id
