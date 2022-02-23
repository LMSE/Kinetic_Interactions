import package_2.constants as c2
import package_2.helpers as h

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

class Compound():
    def __init__(self,name,concentration,sd,inchikey=[],cid=0,iid=0,uid=0):
        self.name           = name
        self.concentration  = concentration
        self.std            = sd
        self.inchikey       = inchikey
        self.cid            = cid
        self.iid            = iid
        self.uid            = uid

    def __str__(self):
        return "{} with inchikey {} ".format(self.name, self.inchikey)

    def set_inchikey(self):
        url = c2.base_url + c2.input_url + self.name.replace(',','%2C').replace(' ','%20') + c2.output_url
        resurl = h.get_url(url)
        new_list = []
        if resurl.find("Status: 404") == -1:
            for item in resurl.splitlines():
                new_list.append(item)
            self.inchikey = new_list

