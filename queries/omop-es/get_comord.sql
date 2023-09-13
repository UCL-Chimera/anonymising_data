select c.condition_occurrence_id as condition_id,
	c.person_id as person,
	c.visit_occurrence_id as visit,
	c.condition_source_value as condition,
	c.condition_start_date,
	c.condition_end_date,
	(
        SELECT cc.concept_name FROM :FILL_SCHEMA:concept AS cc
        WHERE cc.concept_id = c.condition_status_concept_id
     ) AS status
from :FILL_SCHEMA:condition_occurrence as c
