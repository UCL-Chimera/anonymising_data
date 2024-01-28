SELECT
	p.person_id,
    p.birth_datetime AS age,
    p.gender_source_value AS gender,
    p.race_source_value AS ethnicity,
	de.device_source_value AS oxygen_delivery_device,
	de.device_exposure_start_datetime,
	de.device_exposure_end_datetime

FROM :FILL_SCHEMA:device_exposure AS de

INNER JOIN :FILL_SCHEMA:person AS p
    ON de.person_id = p.person_id
	
--WHERE