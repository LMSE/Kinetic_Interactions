# %%
from package_1 import helpers as h1
from package_1 import constants as c


h1.generate_EC_list()
h1.generate_key()

for item in c.EC_list_Obj["name"]: 
    a = h1.analyze_regulator(item)
# %%
