# %%
from package_1 import helpers as h1
from package_1 import constants as c1
#%%
# debuging here for compounds and reaction objects
b = h1.etha_regulation([(10,0.02,"Inhibitor"),(5,0.08,"Activator")])
print(b)
#%% main code to run package_1
h1.generate_EC_list()
h1.generate_key()
#ideally a data lake should be created and at each run time should be populated with new data
met_lake = h1.Load_metabolomics() 
count = 0
for item in c1.EC_list_Obj["name"]: 
    a = h1.analyze_regulator(item)
    b = h1.etha_regulation([(10,0.02,"Inhibitor"),(5,0.08,"Activator")])
    # query regulators in metabolomics lake
    # calculate etha regulation with STD
    if count > 10:
        break
    count+= 1
# %%
