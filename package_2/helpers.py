
import constants as c
import classes as cl

def load_bigg():
    """
    This function load BIGG model and create objects for each entery of BIGG model.
    it returns a list of objects 
    """
    with open(c.BIGG_RXN_file, 'r') as f:
            lines = f.readlines()

    meta_data = []
    database_links = []
    # model_list=[]
    count = 0
    for line in lines:
        count += 1
        if count == 1:
            continue # skip header
        item            = line.rstrip("\n").split('\t')
        # print(item)
        bigg_obj        = cl.Bigg(item[0],item[1].split(';'),\
            item[2].split(';'),item[5].split(';'))
        # model_list = item[3].split(';')
        database_links = item[4].split(';')
        # print(database_links)
        bigg_obj.set_ec(database_links)
        # print(str(bigg_obj))
        meta_data.append(bigg_obj)
        
        
    return meta_data

def load_reaction():
    """
    This function returns a list of reaction objects with attribute name already assigned
    """
    meta_data = []
    with open(c.RXN_file,'r') as f:
        lines = f.readlines()
    
    for name in lines:
        RXN_obj = cl.Reaction(name.strip().rstrip("\n"))
        meta_data.append(RXN_obj)
    return meta_data


def set_ec_rxn(bigg_data, rxn_data):
    """
    This function assignes ec numbers from BIGG model to reaction names.
    """
    for rxn_obj in rxn_data:
        for item in bigg_data:
            if rxn_obj == item:
                rxn_obj.ec = item.ec

    

