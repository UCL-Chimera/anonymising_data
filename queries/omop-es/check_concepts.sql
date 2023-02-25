SELECT 
	DISTINCT c.concept_name AS measurement_type,
    m.measurement_concept_id AS con_id
FROM hic_cc_002.measurement AS m

INNER JOIN hic_cc_002.concept AS c
    ON c.concept_id = m.measurement_concept_id
WHERE
    m.measurement_concept_id IN (3012501, 21490733, 4302666, 3021119, 3033203, 3013290, 
    3023081, 3018572, 3006442, 3011689, 4353938, 3047181, 3033836, 3007930, 3013702, 3027315,
     3015968, 3013502, 3010421, 3030091, 3003458, 21490733, 3000285, 3020779)
