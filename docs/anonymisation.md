# anonymisation
the queries are run against OMOP data which has already to an extent been anonymised. the code here does 2 futher steps in the anonymisation process

## age

the age of a person is calculated from their date of birth using the following algorithm


> age in weeks if  < 1 yr

                    in months if < 18 yrs
                     in years if < 99 yrs
                     100 otherwise


## date of measurement 

the date of the original measurement is then changed by the number of days specified in the configuration file