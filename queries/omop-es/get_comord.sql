select c.condition_occurrence_id as condition_id,
	c.person_id as person,
	c.visit_occurrence_id as visit,
	c.condition_source_value as condition,
	c.condition_start_date,
	c.condition_end_date,
	(
        SELECT cc.concept_name FROM hic_cc_003.concept AS cc
        WHERE cc.concept_id = c.condition_status_concept_id
     ) AS status



from hic_cc_003.condition_occurrence as c
where c.person_id > 0
and   c.person_id < 500