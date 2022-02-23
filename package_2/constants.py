import os
from os.path import dirname, abspath 
from package_1 import constants as c

# folders and files name
met_file_name   = "metabolomics.txt"
decimal_prec    = 4
base_url        = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/'
input_url       = 'compound/name/'
output_url      = '/property/InChIKey/TXT'


# defining file names
met_file         = os.path.join( c.data_dir , met_file_name)

