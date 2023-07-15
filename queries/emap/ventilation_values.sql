--  query to display the possible values recorded 
--  for the ventilator mode flowsheet
--  EPIC ID = 3040102607

SELECT DISTINCT vo.value_as_text AS vent_result

FROM star.visit_observation AS vo

INNER JOIN star.visit_observation_type AS vot

  ON vo.visit_observation_type_id = vot.visit_observation_type_id

    AND vot.id_in_application = '3040102607'
