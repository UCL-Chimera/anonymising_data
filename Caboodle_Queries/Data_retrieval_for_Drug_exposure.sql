SELECT
	    dbo.PatientDim.PatientKey,
	    dbo.DrgEventFact.DrgEventKey,
    	dbo.DrgEventFact.DrgKey,
	    dbo.DrgDim.Name,
	    dbo.DrgDim.Type,
    	dbo.DrgEventFact._CreationInstant,
    	dbo.DrgEventFact._LastUpdatedInstant
FROM
    dbo.DrgEventFact
    INNER JOIN dbo.PatientDim ON dbo.PatientDim.PatientKey = dbo.DrgEventFact.PatientKey
    INNER JOIN dbo.DrgDim ON dbo.DrgDim.DrgKey = dbo.DrgEventFact.DrgKey;
