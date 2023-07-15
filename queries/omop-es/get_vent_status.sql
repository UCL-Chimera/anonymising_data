SELECT

v.procedure_occurrence_id as procedure_id,
v.person_id as person,
v.visit_occurrence_id as visit,
v.procedure_datetime as date,
v.modifier_source_value as ventilation


FROM hic_cc_003.procedure_occurrence AS v
--LEFT JOIN hic_cc_003.measurement AS m
--ON m.person_id = v.person_id
where v.person_id > 499
and v.person_id < 1000

ORDER BY person