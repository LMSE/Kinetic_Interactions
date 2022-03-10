

class Bigg ():
    def __init__(self,bigg_id="",name ="",reaction_string="",old_bigg_ids=[], ec=""):

        self.bigg_id        = bigg_id
        self.name           = name
        self.reaction_string= reaction_string
        self.old_bigg_ids   = old_bigg_ids
        self.ec             = ec 

    def __str__(self):
        return "bigg_id: {}, name: {}, reaction_string: {}, old_bigg_ids: \
            {} , ec: {}".format(self.bigg_id, self.name, self.reaction_string,\
                self.old_bigg_ids, self.ec)

    def set_ec(self,newlist):
        for item in newlist:
            if item.split(': ')[0].strip() == "EC Number":
                self.ec = item.split(': ')[1].split('/')[-1]
                # print("************{}*******8".format(item.split(': ')[1].split('/')[-1]))
class Reaction():
    def __init__(self, name="", EC=[]):
        self.name           = name
        self.ec             = EC
    

    def __str__(self):
        return "reaction name: {} with ec: {}".format(self.name,self.ec)

    def __eq__ (self,other):
        return self.name == other.bigg_id
            


