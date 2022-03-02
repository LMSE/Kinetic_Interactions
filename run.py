#%%
from package_1 import helpers as h1
from package_1 import constants as c1
from pprint import pprint
import sys

# debuging here for compounds and reaction objects
# b = h1.etha_regulation([(10,0.02,"Inhibitor"),(5,0.08,"Activator")])
# print(b)
# sys.exit()
# main code to run package_1
h1.generate_key()
metabolomics_obj_list = h1.Load_metabolomics() 
pprint(str(metabolomics_obj_list[0])) # sample
a = h1.generate_organism_list()
for indx, organism_obj in enumerate(a):
    ec_list = h1.generate_EC_list(organism_obj)
    if ec_list:
        print(ec_list)
        break
sys.exit()


# ideally a data warehouse should be created and at each run time should be populated with new data


count = 0
for item in c1.EC_list_Obj["name"]: 
    a = h1.analyze_regulator(item) # [(2, 1, 876602)]
    print(a)
    
    b = h1.etha_regulation([(10,0.02,"Inhibitor"),(5,0.08,"Activator")])
    # query regulators in metabolomics lake
    # calculate etha regulation with STD
    if count > 10:
        break
    count+= 1

# %%
