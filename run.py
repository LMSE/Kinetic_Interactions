
from package_1 import helpers as h1
from package_1 import constants as c1
import sys
from itertools import compress, filterfalse

# main code to run package_1
# ideally a data warehouse should be created and at each run time should be populated with new data
# print(dir(h1))

h1.generate_key()
metabolomics_obj_list = h1.Load_metabolomics() 
    # print(metabolomics_obj_list)
    #pprint(str(metabolomics_obj_list[0])) # sample
# generate or load the list of organisms in the database
a = h1.generate_organism_list()
# print(len(metabolomics_obj_list))
h1.generate_output(["Organism", "EC Number",  "Etha Regulation","Etha sd",\
    "regulators" , "regulator_iid", "condition"])
for indx, organism_obj in enumerate(a):
    # select part of metabolomics_obj_list where organism is the same
    # print(metabolomics_obj_list[0].organism)
    # print(organism_obj.name)
    if c1.organism_specific_concentration:
        filter = list(map(lambda a: a==organism_obj,metabolomics_obj_list))
        metabolomics_obj_list_cut = list(compress(metabolomics_obj_list, filter))
    else:
        metabolomics_obj_list_cut = metabolomics_obj_list
    # print(len(metabolomics_obj_list_cut))
    # calculate average concentration and sd values for each organism
    hypos_comp = h1.calculate_ave_metabolomics(metabolomics_obj_list_cut)
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
                    filter_conc = list(map(lambda a: regulator==a,metabolomics_obj_list_cut))
                    if any(filter_conc):
                        obj_list = list(compress(metabolomics_obj_list_cut, filter_conc))
                        print(str(obj_list[0]))
                        regulator.set_metabolomics(obj_list[0])
                        if len(obj_list)>1:
                            raise ValueError("multiple compound objects exists for compound concentration")
                    else:
                        print(str(hypos_comp))
                        regulator.set_metabolomics(hypos_comp)
                    
                    
                    regulator.set_name()
                    print(regulator.name)
                    #print(regulator.conc)
                    #print(regulator.std)
                etha_reg = h1.etha_regulation(regulator_list)
                print(etha_reg)
            
                # Append results to output file.
                h1.generate_output([organism_obj.name, ec_obj.name, \
                     etha_reg[0],etha_reg[1],\
                         [regulator.name for regulator in regulator_list],\
                            [regulator.iid for regulator in regulator_list],\
                                 [regulator.condition for regulator in regulator_list]])    