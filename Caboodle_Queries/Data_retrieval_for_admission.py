SELECT
    dbo.HospitalAdmissionFact.HospitalAdmissionKey,
	  dbo.PatientDim.PatientKey,
    dbo.PatientDim.GenderIdentity,
  	dbo.PatientDim.Sex,
  	dbo.PatientDim.Ethnicity,
  	dbo.PatientDim.BirthDate,
  	dbo.HospitalAdmissionFact._CreationInstant,
  	dbo.HospitalAdmissionFact.DischargeInstant,
  	dbo.HospitalAdmissionFact.AdmissionSource,
  	dbo.HospitalAdmissionFact.AdmissionType,
  	dbo.HospitalAdmissionFact.DischargeDisposition,
  	dbo.HospitalAdmissionFact.DischargeDestination_X

FROM
    dbo.PatientDim
    INNER JOIN dbo.HospitalAdmissionFact ON dbo.PatientDim.PatientKey = dbo.HospitalAdmissionFact.PatientKey;





SELECT
    dbo.VisitFact.VisitKey,
	  dbo.PatientDim.PatientKey,
    dbo.PatientDim.GenderIdentity,
  	dbo.PatientDim.Sex,
  	dbo.PatientDim.Ethnicity,
  	dbo.PatientDim.BirthDate,
  	dbo.VisitFact._CreationInstant,
  	dbo.VisitFact._LastUpdatedInstant,
  	dbo.VisitFact.SchedulingSource,
  	dbo.VisitFact.VisitType
    
FROM
    dbo.VisitFact
    INNER JOIN dbo.PatientDim ON dbo.VisitFact.PatientKey = dbo.PatientDim.PatientKey;
