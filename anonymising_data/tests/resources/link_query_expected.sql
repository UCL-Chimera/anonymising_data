SELECT
    person_id
FROM _link AS m

INNER JOIN person AS p
    ON m.person_id = p.person_id

WHERE m.mrn = %s
