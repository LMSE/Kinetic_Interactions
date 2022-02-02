#%%
# liberaries
from matplotlib.font_manager import list_fonts
import mysql.connector
from mysql.connector import errorcode
import sys
import json
import os
from os.path import dirname, abspath

# defining variables
input_folder = "\Input\\"
file_name = "key.json"
organism = 'escherichia coli'
ec_number = "5.3.1.9"
input_dir = dirname(dirname(abspath(__file__))) +input_folder
key = input_dir + file_name

# defining functions
# connect to mysql and return cursor
def connect_to_mysql():
    with open(key) as jsonfile:
        data = json.load(jsonfile)
    try:
        cnx = mysql.connector.connect(user=data["user"],password=data["password"],host=data["host"],database=data["database"])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return cnx

# defining classes
class Organism:
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], res=[]):
        self.name = name
        self.cid  = cid
        self.iid  = iid
        self.uid  = uid
        self.strv = strv
        self.res  = res

    def get_db_info(self,query, parameters):
        self.cnx = connect_to_mysql()
        cursor = self.cnx.cursor()
        try:
            cursor.execute(query, parameters)
            row = cursor.fetchone()
            while row != None:
                self.res.append(row)
                row = cursor.fetchone()
        except Exception as a:
            print("Something is wrong in the query:")
            print(a)
            print("Mysql warnings:")
            print(cursor._fetch_warnings())
            print("executed query:")
            print(cursor._executed)
            self.cnx.close()

        if not self.res:
            print("no results for {}".format(self.name))
            print("executed query:")
            print(cursor._executed)
            exit()

    def close_connection(self):
        self.cnx.close()

    def load_results(self):
        print("loading results ...")
        self.cid = [self.res[i][0] for i in range(len(self.res))]
        self.iid = [self.res[i][1] for i in range(len(self.res))]
        self.uid = [self.res[i][2] for i in range(len(self.res))]
        print("cid = {} ,iid = {} and uid = {}".format(self.cid,self.iid, self.uid))


class EC_number(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], res=[]):
        super().__init__(name,cid,iid,uid,strv,res )

class Activator(Organism):
    def __init__(self, name, cid=[] ,iid=[],uid=[], strv = [], res=[]):
        super().__init__(name,cid,iid,uid,strv,res)

    def load_results(self):
        super().load_results()
        self.strv = [self.res[i][3] for i in range(len(self.res))]
        print("strv = {} ".format(self.strv))


# %% EC query
def main():
    # constructing object for organism
    print("constructing Organism Object ***")
    query = ("""select distinct cid,iid, uid from main where uid in 
    (select refv from main where refv in (select uid from main 
    where cid =1 and refv = 0) and strv = %s)""")
    parameter = (organism,)
    O_obj = Organism(organism)
    O_obj.get_db_info(query,parameter)
    O_obj.load_results()
    O_obj.close_connection()
    
    # constructing EC Object
    print("constructing EC Object ***")
    query = ("""select distinct cid, iid, uid from main where 
    uid in (select refv from main where refv in 
    (select uid from main where cid = 2 and refv = 0) 
    and iid = 17 and strv = %s)""")
    parameter = (ec_number,)
    ec_obj = EC_number(ec_number)
    ec_obj.get_db_info(query,parameter)
    ec_obj.load_results()
    ec_obj.close_connection()

    # inhibitor uid
    print("constructing Inhibitor Object ***")
    query = (
    """select distinct t1.cid,t1.iid,t1.uid, t3.strv from main as t1 
    join main as t2 
    on t2.cid=t1.cid and t2.iid = t1.iid
    join main as t3
    on t3.refv = t2.uid
    where t1.refv in 
    (select uid from main where refv in 
    (select uid from main where refv in 
    (select uid from main where cid = 6 and iid = 1 and refv = %s) 
    and cid = %s and iid = %s) and cid = 6 and iid = 1)
    and t2.refv = 0 and t3.cid = 5 AND t3.iid in (1,2,3)
    having CHAR_LENGTH(t3.strv) < 4
"""
    )
    parameter = (O_obj.uid[0], ec_obj.cid[0],ec_obj.iid[0])
    print(parameter)
    param_obj = Activator("test")
    param_obj.get_db_info(query,parameter)
    param_obj.load_results()
    param_obj.iid = [169,1]
    param_obj.cid = [4,4]
    param_obj.res = [(4,169,178798)]
main()
 
    
# %%
