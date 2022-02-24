import os
from os.path import dirname, abspath 


# folders and files name

data_folder         = "data"
output_folder       = "output"
log_folder          = "log"
log_file_name       = "log.txt"
key_file_name       = "key.json"
ec_file_name        = "ec_list.json"
met_dlake_name      = 'metomics_dlake.json'
organism            = 'escherichia coli'
Log_flag            = False
run_metabolomics    = False  # run load metabolomics function again? produce data lake again?
EC_list_Obj         = []
met_file_name       = "metabolomics.txt"
decimal_prec        = 4
base_url            = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/'
input_url           = 'compound/name/'
output_url          = '/property/InChIKey/TXT'
error_compound_list = [] # these compound names are too general and have multiple inchikeys


# defining directories
dir                 = dirname(dirname(abspath(__file__))) 
data_dir            = os.path.join(dir , data_folder)
output_dir          = os.path.join(dir , output_folder)
log_dir             = os.path.join(dir , log_folder)

# defining file names
key_file            = os.path.join(data_dir , key_file_name)
log_file            = os.path.join(log_dir , log_file_name)
ec_list_file        = os.path.join(data_dir , ec_file_name)
met_file            = os.path.join(data_dir , met_file_name)
met_dlake_file      = os.path.join(data_dir, met_dlake_name)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)




