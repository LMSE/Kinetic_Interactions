
import os 
from os.path import dirname, abspath

data_folder         = "data"
output_folder       = "output"
BIGG_RXN_file_name = "bigg_reactions.txt"
BIGG_MET_file_name = "bigg_metabolites.txt"
RXN_file_name  = "reaction_names.txt"
Res_file_name  = "ec_rxn_ecoli.txt"

dir  = dirname(dirname(abspath(__file__)))
data_dir = os.path.join(dir , data_folder)
output_dir = os.path.join(dir, output_folder)
BIGG_RXN_file = os.path.join(data_dir , BIGG_RXN_file_name)
BIGG_MET_file = os.path.join(data_dir, BIGG_MET_file_name)
RXN_file  = os.path.join(data_dir, RXN_file_name)
Res_file  = os.path.join(output_dir, Res_file_name)

if not os.path.exists(BIGG_RXN_file) \
    or os.path.exists(BIGG_MET_file)\
        or os.path.exists(RXN_file):
    raise FileExistsError("BIGG model file does not exists in the data directory")