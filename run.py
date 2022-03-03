
from package_1 import helpers as h1
from package_1 import constants as c1
import sys
from itertools import compress

# main code to run package_1
h1.generate_key()
metabolomics_obj_list = h1.Load_metabolomics() 
    # print(metabolomics_obj_list)
    #pprint(str(metabolomics_obj_list[0])) # sample
# generate or load the list of organisms in the database
a = h1.generate_organism_list()
for indx, organism_obj in enumerate(a):
    # calculate average concentration and sd values for each organism
    hypos_comp = h1.calculate_ave_metabolomics(metabolomics_obj_list)
    # generate the list of ec numbers for each organism
    ec_list = h1.generate_EC_list(organism_obj)
    print("{} ECs were found for {}".format(len(ec_list),organism_obj.name))
    # ec found
    if ec_list:
        for ec_obj in ec_list:
            print("analyzing regulators for {}".format(str(ec_obj)))
            # generate a list of regulators for each ec of each organism
            regulator_list = h1.generate_regulator_list(ec_obj)
            if regulator_list:# assign concentration
                etha_reg = 0  # set regulation coeficient to zero for this compound
                # set metabolomics for regulators in the list.
                for regulator in regulator_list:
                    # if regulator found, assign concenration and sd values using metabolomics dataset
                    # print(str(regulator))
                    filter_conc = list(map(lambda a: regulator==a,metabolomics_obj_list))
                    if any(filter_conc):
                        obj_list = list(compress(metabolomics_obj_list, filter_conc))
                        if len(obj_list)>1:
                            raise ValueError("multiple compound objects exists for compound concentration")
                        regulator.set_metabolomics(obj_list[0])
                        
                    else:
                        regulator.set_metabolomics(hypos_comp)
                    #print(regulator.conc)
                    #print(regulator.std)
                print(regulator_list)
                etha_reg = h1.etha_regulation(regulator_list)
                print(etha_reg)
                sys.exit()
                    
            


"""
# ideally a data warehouse should be created and at each run time should be populated with new data


count = 0

     # [(2, 1, 876602)]
    print(a)
    
    
    # query regulators in metabolomics lake
    # calculate etha regulation with STD
    if count > 10:
        break
    count+= 1
    """
