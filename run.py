# %%
from package_1 import helpers as h1
from package_1 import constants as c1
from package_2 import helpers as h2
from package_2 import constants as c2

# debuging here for package_2
l   = h2.load_from_text_to_dict()
for item in l:
    item.set_inchikey()
    print(str(item))

#%% main code to run package_1
h1.generate_EC_list()
h1.generate_key()

for item in c1.EC_list_Obj["name"]: 
    a = h1.analyze_regulator(item)
# %%
