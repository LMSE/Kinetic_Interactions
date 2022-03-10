
import os 
from os.path import dirname, abspath

data_folder         = "data"
BIGG_file_name = "BIGG_MODEL.txt"
RXN_file_name  = "reaction_names.txt"

dir  = dirname(dirname(abspath(__file__)))
data_dir = os.path.join(dir , data_folder)
BIGG_file = os.path.join(data_dir , BIGG_file_name)
RXN_file  = os.path.join(data_dir, RXN_file_name)


if not os.path.exists(BIGG_file):
    raise FileExistsError("BIGG model file does not exists in the data directory")


if not os.path.exists(RXN_file):
    raise FileExistsError("reaction file does not exists in the data directory")