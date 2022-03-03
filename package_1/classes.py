from ctypes import Structure
import package_1.helpers as h
import package_1.constants as c
import pandas as pd
import sys
import warnings
import pandas as pd
# defining classes
class Organism:
    def __init__(self, name, cid=[] ,iid=[]):
        h.append_to_log("constucting {}".format(name))
        self.name       = name
        self.cid        = cid
        self.iid        = iid

    def __str__(self):
        return "{} {}, with cid: {}, iid: {}".format(self.__class__.__name__,self.name,self.cid,self.iid)

 
        
class EC_number(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[]):
        super().__init__(name,cid,iid)
        self.uid = uid
    
    def __str__(self):
        return super().__str__()
        

class Regulator(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], floatv = [], comment = [], structure=[],concentration=0,sd=0 ):
        super().__init__(name,cid,iid)
        self.uid        = uid
        self.strv       = strv
        self.floatv     = floatv
        self.comment    = comment
        self.structure  = structure
        self.conc       = concentration
        self.sd         = sd

    def __str__(self):
        return super().__str__()
    
    def __equ__(self,other):
        try:
            if isinstance(other):
                return self.structure == other.first14
            else:
                return self.structure == other
        except AttributeError:
            return NotImplemented

    def to_dict(self):
        return {"uid": self.uid, "cid": self.cid, "iid":self.iid, "KI":self.floatv,\
            "tag":self.comment, "first14":self.structure}
            
    def to_df(self):
        new_dict = {"uid": self.uid, "cid": self.cid, "iid":self.iid, "KI":self.floatv,\
            "tag":self.comment, "first14":self.structure}
        return pd.DataFrame.from_dict(new_dict)
    
    def set_metabolomics(self,other):
        self.conc = other.concentration     # new value for concentration
        self.sd   = other.sd                # new value for standard deviation

# compounds that are part of a reaction
class Compound():
    def __init__(self,name="",concentration=0,sd=0,inchikey=[],cid=0,iid=0, first14 = ""):
        self.name           = name
        self.concentration  = concentration
        self.sd             = sd
        self.inchikey       = inchikey
        self.cid            = cid
        self.iid            = iid
        self.first14        = first14

    def __str__(self):
        return "name:{} inchikey: {}, firt_fourteen_letters: {}, cid: {},\
             iid: {}, concentration: {}, sd: {} "\
        .format(self.name, self.inchikey, self.first14, \
            self.cid, self.iid, self.concentration, self.sd)

    # Instead of a JSON serializable class, implement a serializer method
    def to_dict(self):
        return {"name": self.name, "concentration": str(self.concentration) \
            , "std": str(self.sd), "inchikey":self.inchikey, "cid":str(self.cid),\
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
    
        
