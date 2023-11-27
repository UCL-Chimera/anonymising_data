# Data

This is a brief description of the column headers and what is meant by them for each CSV file.

## ABG Files (data)

This file contains the measurements relating to blood gases taken for particular patients

| Column Header | Explanation | 
| --- | --- |
| measurement_type | The type of measurement|
| measurement_source | The source of the measurement, this might be AQURE UREA or WINPATH MAGNESIUM|
| person_id | Unique number referencing a particular patient |
| visit_id | Unique number referencing the visit of this patient in which this measurement was taken.This allows you to distinguish between Measurements taken for a patient who may have been on the ward on two or more separate occasions. |
| measurement_datetime | The date and time at which the measurement was taken|
| value_as_number | If the measurement yields numeric value then it will be in this column|
| units | Any units associated with numeric value in the previous column |
| value_as_string | If the measurement is given as a string value it will be here. Note this value should be null if there is a value_as_number and vice versa |
| age | The age of the patient in the years |
| gender | The gender of the patient  |
| ethnicity | The ethnicity of the patient |


## Co-morbidity Files

This file contains the co-morbidities related to the patient and the visit.

| Column Header | Explanation | 
| --- | --- |
| condition_id | Unique number referencing this condition recorded for the patient  |
| person_id | Unique number referencing a particular patient - refers to **person_id** in the ABG table  |
| visit_id | Unique number referencing the visit of this patient - refers to **visit_id** in the ABG table |
| condition_start_date | The date and time at which this condition began  |
| condition_end_date | The date and time at which this condition ended  |
| status | The status of the condition |
| condition | The condition recorded for this patient  |


## Ventilation Files

This file contains the ventilation type of the patient and the visit.

| Column Header | Explanation | 
| --- | --- |
| procedure_id | Unique number referencing the RecordedTalon wake ventilation for this person  |
| person_id | Unique number referencing a particular patient - refers to **person_id** in the ABG table  |
| visit_id |  Unique number referencing the visit of this patient - refers to **visit_id** in the ABG table |
| date | The date and time at which the ventilation status was recorded  |
| ventilation | The ventilation status |
