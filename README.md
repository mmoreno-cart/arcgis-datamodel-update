# How to run the Data Model update script

## Description and context

//TODO

This script assumes that Python is installed in the local environment, as well as the module dependencies (`os` and `csv`)

## Step by step

### 1. Update Input files in local environment

#### 1.1. "domains" folder

Create one .csv file per domain (new domain or domain to be updated). The .csv file name will be used as domain name

\\!/ Domains of type `SHORT` are not supported yet.

#### 1.2. inputs.xlsx

* Sheet actions: Enter the list of actions to be done
  * ASSIGN_DOMAIN : Create or update domain and assign it to existing field
  * NEW_FIELD : Create a new field and assign a new or existing domain
* Sheet fc
  * Enter the list of Feature Classes to be used (var_name is used on layer column of actions sheet)

### 2. Once the excel file is filled

1. copy/paste the action sheet on "_actions.csv"
2. replace tabulation by ","
3. copy/paste the fc sheet on "_feature_classes.csv"
4. replace tabulation by ","

### 3. Move the domain files to the server

1. Copy/paste the "domains" folder containing the .csv files of new domains in the server
2. Copy the path to the folder where you stored the files
3. Update the file "_config.csv" with the correct FolderPath to the server's domain folder you just copied (`DOMAIN_PATH`) and update .sde name (`DB_CONNECTION`)

### 4. Run scriptBuilder.py in the local environment

1. Run "scriptBuilder.py"
2. Open "output/output.py" and copy the content (this is the result of scriptBuilder.py)

### 5. Apply the changes on the server

1. Open ArcGIS Pro on the server. It can be the country aprx
2. Open a new notebook
3. Paste the output.py content and run the notebook
4. Check that the domains are properly updated

Data model is updated !

For any questions you can contact the author ! :)