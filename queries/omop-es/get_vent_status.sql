SELECT

v.procedure_occurrence_id as procedure_id,
v.person_id as person,
v.visit_occurrence_id as visit,
v.procedure_datetime as date,
v.modifier_source_value as ventilation


FROM :FILL_SCHEMA:procedure_occurrence AS v
--LEFT JOIN :FILL_SCHEMA:measurement AS m
--ON m.person_id = v.person_id

ORDER BY person