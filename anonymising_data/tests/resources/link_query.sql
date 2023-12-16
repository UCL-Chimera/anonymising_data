SELECT
    person_id
FROM :FILL_SCHEMA:_link AS m

INNER JOIN :FILL_SCHEMA:person AS p
    ON m.person_id = p.person_id

WHERE m.mrn = %s
