import package_1.helpers as h
import package_1.constants as c
import pandas as pd
import sys
import warnings

# defining classes
class Organism:
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], floatv = [], comment = [], res=[], structure=[]):
        h.append_to_log("constucting {}".format(name))
        self.name       = name
        self.cid        = cid
        self.iid        = iid
        self.uid        = uid
        self.strv       = strv
        self.floatv     = floatv
        self.res        = res
        self.comment    = comment
        self.structure  = structure

    def check_res(self): 
        if not self.res:
                print("no results for {}".format(self.name),file=open(c.log_file, "a"))
                print("executed query:",file=open(c.log_file, "a"))
                sys.exit()

    def load_results_into_object(self):
        self.cid        = [self.res[i][0] for i in range(len(self.res))]
        self.iid        = [self.res[i][1] for i in range(len(self.res))]
        self.uid        = [self.res[i][2] for i in range(len(self.res))]

    def print_results(self):
        print("results for {} are: \n {}".format(self.name, self.res))
        h.append_to_log("results for {} are: \n {}".format(self.name, self.res))
        
class EC_number(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], floatv = [], comment = [],res=[], structure =[]):
        super().__init__(name,cid,iid,uid,strv,floatv,comment,res,structure )

class Activator(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], floatv = [], comment = [], res=[], structure=[]):
        super().__init__(name,cid,iid,uid,strv,floatv,comment,res, structure)

    def load_results_into_object(self):
        super().load_results_into_object()
        self.strv       = [self.res[i][3] for i in range(len(self.res))]
        self.comment    = [self.res[i][4] for i in range(len(self.res))]
        self.floatv     = [self.res[i][5] for i in range(len(self.res))]
        self.structure  = [self.res[i][6] for i in range(len(self.res))]

    def cleared_result(self):
        results             = {}
        unique_set          = h.NoDuplicates(self.uid)
        results["uid"]      = self.uid
        results["cid"]      = self.cid
        results["iid"]      = self.iid
        results["strv"]     = self.strv
        results["lstrv"]    = [len(item) for item in self.strv]
        results["floatv"]   = self.floatv
        results["tag"]      = self.comment
        results["InChIkey"] = self.structure

        df                  = pd.DataFrame.from_dict(results)
        res_df              = pd.DataFrame(data = None, columns= df.columns)

        for i in range(len(unique_set)):
            lenmin          = min(df.loc[(df.uid == unique_set[i]), "lstrv"].values)
            temp_df         = df.loc[ (df.uid==unique_set[i]) & (df.lstrv == lenmin)]
            minin           = min(temp_df.index)
            temp_df         = temp_df.loc[minin,:].to_frame().T
            res_df          = pd.concat( [res_df, temp_df ], axis = 0, ignore_index=True)
        res_df          = res_df.drop(columns=['lstrv'])
        return res_df

class Ec_list():
    def __init__(self,name=[],cid=[],iid=[],res=[]):
        self.name   = name
        self.cid    = cid
        self.iid    = iid
        self.res    = res

    def cleared_result(self):
        di = {"name":[],"iid":[],"cid":[]}
        for item in self.res:
            di["name"].append(item[0])
            di["iid"].append(item[1])
            di["cid"].append(item[2])
        return di


# each reaction should be linked to EC number and reaction string of Database
class Reaction():
    def __init__(self, name, ec, compounds, cid, iid, uid):
        self.ec             = ec
        self.name           = name
        self.compounds      = compounds
        self.cid            = cid
        self.iid            = iid
        self.uid            = uid
    
    def __str__(self):
        return "Reaction( {}, {}, {})".format(self.name, self.ec, self.iid)

# compounds that are part of a reaction
class Compound():
    def __init__(self,name,concentration,sd,inchikey=[],cid=0,iid=0, first14 = ""):
        self.name           = name
        self.concentration  = concentration
        self.std            = sd
        self.inchikey       = inchikey
        self.cid            = cid
        self.iid            = iid
        self.first14        = first14

    def __str__(self):
        return "{}: inchikey {}, firt fourteen letters {}, cid {}, iid {} "\
        .format(self.name, self.inchikey, self.first14, self.cid, self.iid)

    # Instead of a JSON serializable class, implement a serializer method
    def to_dict(self):
        return {"name": self.name, "concentration": str(self.concentration) \
            , "std": str(self.std), "inchikey":self.inchikey, "cid":str(self.cid),\
                 "iid":str(self.iid), "first14":self.first14}
    
    def set_inchikey(self):
        """
        this function queries PubChem to reterive InChiKeys for a given compound name
        returns: populates compound object InChiKeys for each compound or None 
        if there is an server error.
        """
        enco_name = self.name.replace(',','%2C').replace(' ','%20')
        url = c.base_url + c.input_url + enco_name + c.output_url
        resurl = h.get_url(url)
        new_list = []
        if resurl.find("Status:") == -1:
            for item in resurl.splitlines():
                new_list.append(item)
            self.inchikey = new_list
    
    def set_first14(self):
        key         = ""
        key_list    = []
        error_comp  = ""
        if not self.inchikey:
            self.first14 = []
        else:
            for item in self.inchikey:
                key_list.append(item.split("-")[0])

                # print(key_list)
            flag = all(element == key_list[0] for element in key_list)
            if (flag):
                # "All the elements are Equal"
                key = key_list[0]
            else:
                # throw errors
                # "All Elements are not equal"
                # append to log and raise a warning

                h.append_to_log("Compound {} has multiple inchikeys".format(self.name))
                warnings.warn("first fourteen letters of inchikeys are not the same for {} compound. Inchikeys are {} .end".format(self.name, self.inchikey))
                error_comp = self.name

            self.first14 = key
            
            return error_comp
    
    def set_attributes(self):
        """
        This function queries database to retrive cid, and iid of a given inchikey
        returns: populates the compound object with cid and iid information
        """
        if not self.inchikey:
            self.cid = 0
            self.iid = 0
        else:
            new_list = h.get_cid_iid_uniquekey(self.first14)[0]
            self.cid = new_list[0]
            self.iid = new_list[1]
    
        
