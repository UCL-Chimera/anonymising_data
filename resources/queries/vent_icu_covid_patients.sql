SELECT DISTINCT

  live_mrn.mrn mrn,
  hv.admission_time admission,
  lv.admission_time loc_admit,
  dept.name

 FROM star_a.hospital_visit hv


  -- has covid 
  INNER JOIN star_a.patient_condition inf

  ON inf.hospital_visit_id = hv.hospital_visit_id

  INNER JOIN star_a.condition_type condtype

    ON condtype.condition_type_id = inf.condition_type_id
  
    AND condtype.internal_code like '%COVID-19'

    -- were in ICU


  INNER JOIN star_a.location_visit lv

    ON lv.hospital_visit_id = hv.hospital_visit_id

  INNER JOIN star_a.location loc

    ON loc.location_id = lv.location_id

  INNER JOIN star_a.department dept

    ON loc.department_id = dept.department_id

    AND dept.speciality like '%ICU'

-- was ventilated

  INNER JOIN star_a.visit_observation vo

  ON hv.hospital_visit_id = vo.hospital_visit_id

INNER JOIN star_a.visit_observation_type AS vot  

  ON vo.visit_observation_type_id = vot.visit_observation_type_id  

  AND vot.id_in_application = '3040102607'  

  -- check for live mrn
INNER JOIN  star_a.mrn original_mrn  

  ON hv.mrn_id = original_mrn.mrn_id 

-- get mrn to live mapping  

INNER JOIN star_a.mrn_to_live mtl   

  ON original_mrn.mrn_id = mtl.mrn_id  

-- get live mrn  

INNER JOIN star_a.mrn live_mrn   

  ON mtl.live_mrn_id = live_mrn.mrn_id  

