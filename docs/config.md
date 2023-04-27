# configuration

## Template of config.yaml

```
files:
  input:
    concept_mapping:
    db_query:
  output:
    query:
    omop_data:
    final_data:
database:
  path:
  schema:
anonymisation:
  date_offset:
```

## Values needed

### **files**:
Files needed during run.

#### **input:**
Files needed for input to code.

##### **concept_mapping:**
Path to csv file containing the [concept ids](concepts.md).

##### **db_query:**
Path to sql file containing the [template query](query.md).

#### **output:**
Files that will be output by code.

##### **query:**
Path to where the completed sql [query](query.md) file is to be written.

##### **omop_data:**
Path to where the omop extracted by the query is to be written as a csv file.

##### **final_data:**
Path to where the anonymised data is to be written as a csv file.

### **database:**
Information about the database to query.

#### **path:**
Path to the database.

#### **schema:**
The schema in the database to be queried.

### **anonymisation:**
Information specifying how anonymisation is done.

#### **date_offset:**
The number of days by which any date has been changed. 