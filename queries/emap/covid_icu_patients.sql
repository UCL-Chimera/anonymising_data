-- Code to retrieve patients who have 
-- a COVID diagnosis
-- been in ICU

SELECT DISTINCT

    live_mrn.mrn mrn,
    hv.admission_time admission,
    lv.admission_time loc_admit,
    dept.name

FROM star.hospital_visit hv


-- has covid 
INNER JOIN star.patient_condition inf

    ON inf.hospital_visit_id = hv.hospital_visit_id

INNER JOIN star.condition_type condtype

    ON condtype.condition_type_id = inf.condition_type_id

        AND condtype.internal_code like '%COVID-19'

-- were in ICU
INNER JOIN star.location_visit lv

    ON lv.hospital_visit_id = hv.hospital_visit_id

INNER JOIN star.location loc

    ON loc.location_id = lv.location_id

INNER JOIN star.department dept

    ON loc.department_id = dept.department_id

        AND dept.speciality LIKE '%ICU'


INNER JOIN star.mrn original_mrn

    ON hv.mrn_id = original_mrn.mrn_id

-- get mrn to live mapping  

INNER JOIN star.mrn_to_live mtl

    ON original_mrn.mrn_id = mtl.mrn_id

-- get live mrn  

INNER JOIN star.mrn live_mrn

    ON mtl.live_mrn_id = live_mrn.mrn_id
