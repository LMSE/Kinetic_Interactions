# %%
from package_1 import helpers as h1
from package_1 import constants as c1

# debuging here for compounds and reaction objects
l   = h1.Load_metabolomics()
for item in l:
    item.set_inchikey()
    print(str(item))

#%% main code to run package_1
h1.generate_EC_list()
h1.generate_key()

for item in c1.EC_list_Obj["name"]: 
    a = h1.analyze_regulator(item)
# %%
