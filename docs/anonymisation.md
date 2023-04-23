# anonymisation

The queries are run against OMOP data which has already to an extent been anonymised. The code here does 2 futher steps in the anonymisation process

## age

The age of a person is calculated from their date of birth using the following algorithm


> returns an integer 'age'
> 
> in weeks if  < 1 yr                    
> in months if < 18 yrs                  
> in years if < 99 yrs                           
> 100 otherwise


## date of measurement 

The date of the original measurement is then changed by the number of days specified in the configuration file

> EXAMPLES
>
> offset specified 30  31/03/2023 becomes 01/03/2023