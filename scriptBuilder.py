import os
import csv

#WORKING_DIR = r'C:/miguel/trabajo/projects/unhcr/GDS/2022/site mapping/Mauritania/script'
WORKING_DIR = r'D:\dev\repos\python\arcgis-datamodel-update'
#WORKING_DIR = r'C:/NextCloud/CartONG Team/10_Projects/UNHCR-GDS/Site Mapping/Country support/Data model update script'

os.chdir(WORKING_DIR)
#print(os.getcwd())

# Init config variables
SDE_DB_CONNECTION_PATH = ""
DB_CONNECTION = ""
DOMAIN_PATH = ""

# Init output commands
fcs = []
new_domains = []
create_domains = []
domain_assigns = []
new_fields = []

# Read config csv
with open('input/_config.csv', mode='r', encoding='utf-8') as csv_file:
  print(f'Opened config file.')

  csv_reader = csv.DictReader(csv_file)
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      print(f'Column names are {", ".join(row)}')
      line_count += 1
    
    # Get config variables
    SDE_DB_CONNECTION_PATH = row["SDE_DB_CONNECTION_PATH"]
    DB_CONNECTION = row["DB_CONNECTION"]
    DOMAIN_PATH = row["DOMAIN_PATH"] + '/'

    line_count += 1

  print(f'Processed {line_count} lines.')

# Read feature class csv
with open('input/_feature_classes.csv', mode='r', encoding='utf-8') as csv_file:
  print(f'Opened feature class file.')

  csv_reader = csv.DictReader(csv_file)
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      print(f'Column names are {", ".join(row)}')
      line_count += 1
    
    # Build Feature Class variable
    if row["skip"] != "true":
      new_fc = f'{row["var_name"]} = \'{row["fc_name"]}\''
      fcs.append(new_fc)

    line_count += 1

  print(f'Processed {line_count} lines.')


# List path variables for new domains
domain_files = os.listdir("input/domains")
domain_count = 0
for domain_filename in domain_files:

  # Build new domain path variables
  domain_name = os.path.splitext(domain_filename)[0]
  domain_varname = "dom_" + domain_name
  new_domain_path = f'{domain_varname} = DOMAIN_PATH + \'{domain_filename}\''
  new_domains.append(new_domain_path)

  # Build arcpy command TableToDomain_management
  new_domain_creation = f'arcpy.TableToDomain_management({domain_varname}, \'code\', \'description\', DB_CONNECTION, \'{domain_name}\', \'{domain_name}\', \'REPLACE\')'
  create_domains.append(new_domain_creation)

# Read actions csv
with open('input/_actions.csv', mode='r', encoding='utf-8') as csv_file:
  print(f'Opened actions file.')

  csv_reader = csv.DictReader(csv_file)
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      print(f'Column names are {", ".join(row)}')
      line_count += 1
    
    # Process line
    if row["action"] == "ASSIGN_DOMAIN":

      # Build arcpy command AssignDomainToField
      new_domain_assign = f'arcpy.management.AssignDomainToField({row["layer"]}, \'{row["field"]}\', \'{row["domain"]}\', None)'
      domain_assigns.append(new_domain_assign)

    elif row["action"] == "NEW_FIELD":

      # Catch field length for numeric fields
      if row["field_type"] == "LONG" or row["field_type"] == "DOUBLE" or row["field_type"] == "DATE":
        row["field_length"] = None

      # Build arcpy command AddField
      new_field = f'arcpy.management.AddField({row["layer"]}, \'{row["field"]}\', \'{row["field_type"]}\', None, None, {row["field_length"]}, \'{row["field_alias"]}\', "NULLABLE", "NON_REQUIRED", \'{row["domain"]}\')'
      new_fields.append(new_field)

    line_count += 1

  print(f'Processed {line_count} lines.')


# Build site mapping update script
with open('output/output.py', 'w', encoding='utf-8') as f:
  f.write('# REMEMBER TO STOP SERVICES (EDIT AND VIEW)')
  f.write('\n')

  f.write('\n')
  f.write('# Import system modules')
  f.write('\n')
  f.write('import arcpy')
  f.write('\n')
  
  f.write('\n')
  f.write('# Init config variables')
  f.write('\n')
  f.write(f'SDE_DB_CONNECTION_PATH = r\'{SDE_DB_CONNECTION_PATH}\'')
  f.write('\n')
  f.write(f'DB_CONNECTION = r\'{DB_CONNECTION}\'')
  f.write('\n')
  f.write(f'DOMAIN_PATH = r\'{DOMAIN_PATH}\'')
  f.write('\n')

  f.write('\n')
  f.write('# Set target feature classes')
  f.write('\n')
  f.writelines('\n'.join(fcs))
  f.write('\n')

  f.write('\n')
  f.write('# Set path of new domains')
  f.write('\n')
  f.writelines('\n'.join(new_domains))
  f.write('\n')

  f.write('\n')
  f.write('# Set the workspace for the domain creation')
  f.write('\n')
  f.write(f'arcpy.env.workspace = r\'{SDE_DB_CONNECTION_PATH}\'')
  f.write('\n')

  f.write('\n')
  f.write('# Create domains from CSV files')
  f.write('\n')
  f.writelines('\n'.join(create_domains))
  f.write('\n')

  f.write('\n')
  f.write('# Change the workspace for the field creation')
  f.write('\n')
  f.write(f'arcpy.env.workspace = r\'{SDE_DB_CONNECTION_PATH}/{DB_CONNECTION}\'')
  f.write('\n')

  f.write('\n')
  f.write('# Assign new domains to existing fields')
  f.write('\n')
  f.writelines('\n'.join(domain_assigns))
  f.write('\n')

  f.write('\n')
  f.write('# Create new fields (assigning corresponding domains)')
  f.write('\n')
  f.writelines('\n'.join(new_fields))
  f.write('\n')