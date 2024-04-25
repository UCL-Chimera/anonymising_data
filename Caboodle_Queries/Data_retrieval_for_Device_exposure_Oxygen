SELECT
	  dbo.PatientDim.PatientKey,
	  dbo.LabComponentResultFact.LabComponentResultKey,
	  dbo.LabComponentResultFact.LabComponentKey,
	  dbo.LabComponentDim.Name,
    dbo.LabComponentResultFact._CreationInstant,
    dbo.LabComponentResultFact._LastUpdatedInstant
FROM
    dbo.LabComponentResultFact
    INNER JOIN dbo.PatientDim ON dbo.PatientDim.PatientKey = dbo.LabComponentResultFact.PatientKey
    INNER JOIN dbo.LabComponentDim ON dbo.LabComponentResultFact.LabComponentKey = dbo.LabComponentDim.LabComponentKey
    WHERE LabComponentDim.Name LIKE '%Oxygen%';
