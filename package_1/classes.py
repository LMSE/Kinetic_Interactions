import package_1.helpers as h
import package_1.constants as c
import pandas as pd
import sys

# defining classes
class Organism:
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], floatv = [], comment = [], res=[]):
        h.append_to_log("constucting {}".format(name))
        self.name       = name
        self.cid        = cid
        self.iid        = iid
        self.uid        = uid
        self.strv       = strv
        self.floatv     = floatv
        self.res        = res
        self.comment    = comment

    def check_res(self): 
        if not self.res:
                print("no results for {}".format(self.name),file=open(c.log_file, "a"))
                print("executed query:",file=open(c.log_file, "a"))
                sys.exit()

    def close_connection(self):
        pass

    def load_results_into_object(self):
        self.cid        = [self.res[i][0] for i in range(len(self.res))]
        self.iid        = [self.res[i][1] for i in range(len(self.res))]
        self.uid        = [self.res[i][2] for i in range(len(self.res))]

    def print_results(self):
        print("results for {} are: \n {}".format(self.name, self.res))
        h.append_to_log("results for {} are: \n {}".format(self.name, self.res))
        
class EC_number(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], floatv = [], comment = [],res=[]):
        super().__init__(name,cid,iid,uid,strv,floatv,comment,res )

class Activator(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], floatv = [], comment = [], res=[]):
        super().__init__(name,cid,iid,uid,strv,floatv,comment,res)

    def load_results_into_object(self):
        super().load_results_into_object()
        self.strv       = [self.res[i][3] for i in range(len(self.res))]
        self.comment    = [self.res[i][4] for i in range(len(self.res))]
        self.floatv     = [self.res[i][5] for i in range(len(self.res))]

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