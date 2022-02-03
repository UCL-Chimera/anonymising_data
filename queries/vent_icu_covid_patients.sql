SELECT DISTINCT

  inf.mrn_id
    FROM star.patient_condition inf

  -- has covid 

  JOIN star.condition_type condtype

    ON condtype.condition_type_id = inf.condition_type_id
  
    AND condtype.internal_code like '%COVID-19'

  -- were in ICU

  JOIN star.hospital_visit hv

    ON hv.mrn_id = inf.mrn_id

  JOIN star.location_visit lv

    ON lv.hospital_visit_id = hv.hospital_visit_id

  JOIN star.location loc

    ON loc.location_id = lv.location_id

  JOIN star.department dept

    ON loc.department_id = dept.department_id

    AND dept.speciality like '%ICU'

 -- make sure current live mrn

-- original MRN that may or may not be live  

INNER JOIN  star.mrn original_mrn  

  ON hv.mrn_id = original_mrn.mrn_id 

-- get mrn to live mapping  

INNER JOIN star.mrn_to_live mtl   

  ON original_mrn.mrn_id = mtl.mrn_id  

-- get live mrn  

INNER JOIN star.mrn live_mrn   

  ON mtl.live_mrn_id = live_mrn.mrn_id  


-- was ventilated

--JOIN star.visit_observation vo

--  ON hv.hospital_visit_id = vo.hospital_visit_id

--INNER JOIN star.visit_observation_type AS vot  

--  ON vo.visit_observation_type_id = vot.visit_observation_type_id  

--  AND vot.id_in_application = '3040102607'  
