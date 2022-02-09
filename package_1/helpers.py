# %%
import package_1.constants as c
import package_1.classes as cl
import mysql.connector
from mysql.connector import errorcode
import json
import os
from datetime import datetime
import sys

def is_file_nonempty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.exists(file_path) and os.stat(file_path).st_size >= 10

def generate_key():
    if not os.path.exists(c.data_dir):
        print("generating directory {}".format(c.data_dir))
        os.makedirs(c.data_dir)
        
    if is_file_nonempty(c.key_file):
        # non empty file exists
        return 0

    print("Please input following information to connect to the SQL database on the remote server")
    key1 = input("Please input the username?")
    key2 = input("please input the passwprd?")
    key3 = input("please input the host URL?")
    key4 = input("please input the database name?")
    mysql_connection ={'user':key1,'password':key2,'host':key3,'database':key4}

    with open(c.key_file, 'w') as fp:
        json.dump(mysql_connection,fp)
    print("key.json is generated in the data folder")
    return 1

def NoDuplicates(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def newline2string(newString):
    return newString + '\n' if not newString.endswith('\n') else newString

def append_to_log(res, End_flag=False):
    s = '*'
    n = 30
    separator = ''.join([char*n for char in s])
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    with open(c.log_file,'a') as f:
        if isinstance(res, str):
            line2print = res
        else:    
            line2print = res.to_string(header=True,index=False)
        if not c.Log_flag:
            f.write(newline2string(separator+f"run_{date}"+separator))
            c.Log_flag = True
        f.write(newline2string(line2print))
        if End_flag:
            f.write(newline2string(separator))

def generate_output(df2print, name):
    output_file = os.path.join(c.output_dir , name + ".txt")
    with open(output_file,'a') as f:
        line2print = df2print.to_string(header=True,index=False)
        f.write(newline2string(line2print))
    
# connect to mysql and return cursor
def connect_to_mysql():
    with open(c.key_file) as jsonfile:
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
        sys.exit(0)
    return cnx

#  Function main_analyze  
def analyze_organism():
    # constructing object for organism
    query = ("""select distinct cid,iid, uid from main where uid in 
    (select refv from main where refv in (select uid from main 
    where cid =1 and refv = 0) and strv = %s)""")
    O_obj               = cl.Organism(c.organism)
    parameter           = (O_obj.name,)
    O_obj.get_db_info(query,parameter)
    O_obj.load_results_into_object()
    O_obj.print_results()
    O_obj.close_connection()
    return O_obj

def analyze_EC():
    # constructing EC Object
    append_to_log("cunstructing EC object...\n")
    query = ("""select distinct cid, iid, uid from main where 
    uid in (select refv from main where refv in 
    (select uid from main where cid = 2 and refv = 0) 
    and iid = 17 and strv = %s)""")
    ec_obj              = cl.EC_number(c.ec_number)
    parameter           = (ec_obj.name,)
    ec_obj.get_db_info(query,parameter)
    ec_obj.load_results_into_object()
    ec_obj.print_results()
    ec_obj.close_connection()
    return ec_obj

def analyze_regulator():
    # call EC information from DB
    append_to_log("cunstructing regulator object...\n")
    ec_obj = analyze_EC()
    # inhibitor uid
    query = (
    """select distinct t1.cid as `cid`, t1.iid as `iid` ,t1.uid as `uid`, t3.strv as `Compound_name`,
    if(t4.iid=10,"Inhibitor",if(t4.iid=11,"Activator", if(t4.iid=12,"Cofactor","Else"))) as `Tag` ,
    t5.floatV as `K_I_value`
    from main as t1 # level of compound under the reaction
    join main as t2 # level of compound itself
    on t2.cid=t1.cid and t2.iid = t1.iid
    join main as t3 # level of compound properties i.e. name
    on t3.refv = t2.uid
    join main as t4 # level of inhibitor properties i.e inhibitory tag
    on t4.refv = t1.uid
    join main as t5 # level of inhibitor properties i.e kinetic parameter K_I
    on t5.refv = t1.uid
    where t1.refv in 
    (select uid from main where refv in 
    (select uid from main where refv in 
    (select uid from main where cid = 6 and iid = 1) 
    and cid = %s and iid = %s ) and cid = 6 and iid = 1)
    and t2.refv = 0 and t3.cid = 5 AND t3.iid in (1,2,3) and t4.iid in (10,11,12) and t5.iid = 18
    order by uid, CHAR_LENGTH(t3.strv) ASC
    """
    )
    parameter           = (ec_obj.cid[0],ec_obj.iid[0])
    param_obj           = cl.Activator("activators")
    param_obj.get_db_info(query,parameter)
    param_obj.load_results_into_object()
    param_obj.close_connection()
    results = param_obj.cleared_result()
    append_to_log(results, True)
    generate_output(results,ec_obj.name.replace(".","-"))
    return results


    


    

# %%
