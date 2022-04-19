CREATE TABLE PatientDim (
    DurableKey    INTEGER PRIMARY KEY,
    Sex           TEXT,
    BirthDate     TEXT,
    IsCurrent     INTEGER DEFAULT 1,
    PrimaryMrn    TEXT
    );
