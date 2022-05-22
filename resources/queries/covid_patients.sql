SELECT DISTINCT

  live_mrn.mrn mrn,
  hv.admission_time admission,
  hv.discharge_time

 FROM star_a.hospital_visit hv


  -- has covid 
  INNER JOIN star_a.patient_condition inf

  ON inf.hospital_visit_id = hv.hospital_visit_id

  INNER JOIN star_a.condition_type condtype

    ON condtype.condition_type_id = inf.condition_type_id
  
    AND condtype.internal_code like '%COVID-19'


INNER JOIN  star_a.mrn original_mrn  

  ON hv.mrn_id = original_mrn.mrn_id 

-- get mrn to live mapping  

INNER JOIN star_a.mrn_to_live mtl   

  ON original_mrn.mrn_id = mtl.mrn_id  

-- get live mrn  

INNER JOIN star_a.mrn live_mrn   

  ON mtl.live_mrn_id = live_mrn.mrn_id  

