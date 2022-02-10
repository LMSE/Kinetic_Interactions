import os
from os.path import dirname, abspath 


# folders and files name
global Log_flag

data_folder     = "data"
output_folder   = "output"
log_folder      = "log"
log_file_name   = "log.txt"
key_file_name   = "key.json"
ec_file_name    = "ec_list.json"
organism        = 'escherichia coli'
ec_number       = [] 
Log_flag        = False
EC_list_Obj     = []

# defining directories
dir             = dirname(dirname(abspath(__file__))) 
data_dir        = os.path.join(dir , data_folder)
output_dir      = os.path.join(dir , output_folder)
log_dir         = os.path.join(dir , log_folder)

# defining file names
key_file        = os.path.join(data_dir , key_file_name)
log_file        = os.path.join(log_dir , log_file_name)
ec_list_file    = os.path.join(data_dir , ec_file_name)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
