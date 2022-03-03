# libraries
import package_1.constants as c
import package_1.classes as cl
import mysql.connector
from mysql.connector import errorcode
import json
import os
from datetime import datetime
import sys
from decimal import *
import pycurl
import certifi
from io import BytesIO
from itertools import chain

# global variables:
global organism_list_Obj
organism_list_Obj = []


# Function definition for compounds class
def calculate_ave_metabolomics(new_list_obj):
    """
    calculate_ave_metabolomics(new_list_obj) calculates average concentration and sd in a list of compound objects
    this value should be used for compounds that dont have a concentration value in the metabolomics file.
    @param_1: a list of compound obj
    return  : a compound obj with ave concentration and ave sd value.
    """

    length = len(new_list_obj)
    sum_conc = 0
    sum_sd   = 0
    for obj in new_list_obj:
        sum_conc += obj.concentration
        sum_sd   += obj.sd
    return cl.Compound(concentration=sum_conc/length,sd=sum_sd/length)

def etha_regulation(new_list_obj):
    getcontext().prec = c.decimal_prec
    """
    This function calculates etha regulation for certain types of allosteric regulation.
    Param_1: new_list contains regulatior objects. each tuple belongs to a regulator
    first element is concentration, second is KI and third is tag of inhibitor or activator

    returns: etha regulation
    """
    sum_reg = 0  # term in the denominator of etha regualation
    etha    = 0  # etha regulation variable

    if new_list_obj[0].sd == 0: # no Standard Deviation has passed to the function
        for item in new_list_obj:
            if item.comment == "Inhibitor": # it is an inhibitor
                sum_reg += Decimal(item.conc/item.floatv)
            elif item.comment == "Activator": # it is an activator
                sum_reg += Decimal(-item.conc/item.floatv)
            else:
                raise ValueError("Tag should be either Inhibitor or Activator")

        etha = Decimal(1/(1+sum_reg))
        if etha < 0:
            raise ValueError("Etha regulation is negative. modify input numbers")
    else:  # standard deviation has passed to the function
        print("this section of code is not implemented yet")

    return etha


def Load_metabolomics():
    """
    Load concentration data for each metabolites from data/metabolomics.txt
    Then, it opens metabolomics data lake if exists and will not run again.
    it creates a compound object for each line of the text file

    returns: a list of compound objects
    """
    met_data_lake = []
    getcontext().prec = c.decimal_prec # set decimal numbers

    # if the file exists and flag is false ony load the file
    if os.path.exists(c.met_dlake_file) and not c.run_metabolomics:
        met_data_lake = []
        # Load data from file
        with open(c.met_dlake_file) as json_file:
            met_json = json.load(json_file)
            # convert diction of list of dictionary to compound object
        for item in met_json["results"]:
            met_data_lake.append(cl.Compound(item["name"],Decimal(item["concentration"])\
                ,Decimal(item["std"]), item["inchikey"], item["cid"]\
                    , item["iid"], item["first14"]))
        append_to_log("Metabolomics data lake is loaded to memory... \n")
        append_to_log("Metabolomics data is available for {} compounds... \n".format(len(met_data_lake)+1))

    else: # first time run or wish to run again?
        append_to_log("Running to create metabolomics data lake ... \n")
        S2f = lambda X: tryconvert(X,X,Decimal)
        met_file = open(c.met_file)
        for line in met_file:
            name, CONC, SD, LB, UP, OOM  = list(map(S2f,line.split("\t")))
            append_to_log("Obtaining results for {} compound... \n".format(name))

            if name in c.error_compound_list:
                append_to_log ("Compound {} is in the error list".format(name))
                continue # do not add compounds with general names

            comp_obj = cl.Compound(name,CONC*OOM,SD*OOM)
            comp_obj.set_inchikey() # setting inchikey from PubChem
            error_comp = comp_obj.set_first14() # setting first fourteen letters of inchikey
            if error_comp:
                c.error_compound_list.append(error_comp)
                append_to_log("compound {} cannot be analyzed as it has too many different inchikeys".format(error_comp))
                continue 
            comp_obj.set_attributes()  # setting cid and iid
            met_data_lake.append(comp_obj)
            
        # write the file to pc and save for the next run
        with open(c.met_dlake_file,'w') as of:
            results = [item.to_dict() for item in met_data_lake]
            json.dump({"results": results}, of, indent = 4)

    return met_data_lake


def get_cid_iid_uniquekey(new_first14):
    query =("SELECT 4, id FROM LMSE.unique_key WHERE Unique_key = %s ")
    parameter = (str(new_first14),)
    # print(parameter)
    result = get_db_info(query,parameter)
    if result:
        return result
    else:
        return []

# General Functions
def tryconvert(value, default, *types):
    """
    this function tries to convert a string to mentioned type.
    if it succeed, it will return a converted string.
    Otherwise, it will return string itself.
    """
    for t in types:
        try:
            return t(value)
        except (ValueError, TypeError, InvalidOperation):
            continue
    return default

def get_url(url):
    """
    get_url(url) uses pycurl for REST API for transferring the data to and from a serve.

    @param_1: url: input url for which results must be obtained
    returns: resulted text file which can have multiple lines. 
    """
    buffer = BytesIO()
    curl_obj = pycurl.Curl()
    curl_obj.setopt(curl_obj.URL, url)
    curl_obj.setopt(curl_obj.WRITEDATA, buffer)
    curl_obj.setopt(curl_obj.CAINFO, certifi.where())
    curl_obj.perform()
    curl_obj.close()
    body = buffer.getvalue()
    return body.decode("utf-8").rstrip()

def is_file_nonempty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.exists(file_path) and os.stat(file_path).st_size >= 10

def generate_key():
    """
        generate_key() generates a key.json file in the data folder. this file holds
        necessary information to connect to the mysql server.
        the user should enter necessary information for the first time to create key.json
        From then, the code extracts information from key.json
    """
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
    """
    NoDuplicates(seq, idfun=None) remove duplicates from a given list.
    This function does not sort the output list and data order is reserved.

    param_1: seq: is an input list with duplicate enteries
    param_2: a given function default returns the value

    returns: a unique list.
    """
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
    """
    newline2string(newString) adds a newline char to the end of a sting

    param @newString: the string to which the newline chat should be added
    returns: a string with a newline char added to the end
    """
    return newString + '\n' if not newString.endswith('\n') else newString

def append_to_log(res, End_flag=False):
    """
    append_to_log(res, End_flag=False) opens log file and append a string to it

    param_1 @res: string/dataframe/dictionary to be inserted in the log file 
    parame_2 @End_flag: if true, insert a final separator in the file. default = False 
    returns: NULL
    """
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
    """
    connect_to_mysql() creates a connection to LMSE DB using key.json file in the data folder

    returns: connection object cnx
    """
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
        sys.exit()
    return cnx

def get_db_info(query, parameters=()):
    """
    get_db_info(query, parameters=()) send a given query to LMSE DB and reterives results

    param_1: given query type tuple
    param_2: given parameters type tuple default is an empty tuple

    return: obtained results from DB
    """
    res = []
    cnx        = connect_to_mysql()
    cursor          = cnx.cursor()
    try:
        if not parameters:
            cursor.execute(query)
        else: 
            cursor.execute(query, parameters)
        row         = cursor.fetchone()
        while row  != None:
            res.append(row)
            row     = cursor.fetchone()
    except Exception as a:
        delim = '\n'
        error = "Something is wrong in the query:"
        print(error , a, cursor._fetch_warnings(), sep=delim)
        error = error +delim+ str(a) +delim+ str(cursor._fetch_warnings())
        print("executed query:")
        print(cursor._executed)
        append_to_log(error)
    cnx.close()
    return res

# Function definition for Organims and Activators
#  Function main_analyze  
def analyze_organism():
    """
    analyze_organism() queries LMSE DB to obtain uid, cid and iid of a given organism name
    organism should be defined in constants.py

    return: organism object with all necessary information filled.
    """
    # constructing object for organism
    query = ("""select distinct cid,iid, uid from main where uid in 
    (select refv from main where refv in (select uid from main 
    where cid =1 and refv = 0) and strv = %s)""")
    O_obj               = cl.Organism(c.organism)
    parameter           = (O_obj.name,)
    O_obj.res = get_db_info(query,parameter)
    O_obj.check_res()
    O_obj.load_results_into_object()
    O_obj.print_results()
    return O_obj

def analyze_EC(new_EC): 
    """
    analyze_EC() query LMSE DB to obtain uid, cid and iid of a given EC number
    EC number should be defined in constants.py .

    return: EC object with all necessary information filled
    param_1: EC number to be queried
    """
    # constructing EC Object
    append_to_log("cunstructing EC object...\n")
    query = ("""select distinct cid, iid, uid from main where 
    uid in (select refv from main where refv in 
    (select uid from main where cid = 2 and refv = 0) 
    and iid = 17 and strv = %s)""")
    ec_obj              = cl.EC_number(new_EC)
    parameter           = (ec_obj.name,)
    ec_obj.res = get_db_info(query,parameter)
    ec_obj.check_res()
    ec_obj.load_results_into_object()
    ec_obj.print_results()
    return ec_obj

def generate_regulator_list(ec_obj):
    """
    analyze_regulator query LMSE DB to obtain information for all regulators under each EC number
    
    return: a dataframe with columns = [uid,cid,iid,strv,floatv,tag, InChIkey]
    param_1 : EC number for which regulators are to be extracted
    """ 
    # call EC information from DB
    append_to_log("cunstructing regulator object...\n")
    # ec_obj = analyze_EC(new_EC)
    # inhibitor uid
    query = (
    """\
        select distinct t1.cid as `cid`, t1.iid as `iid` ,t1.uid as `uid`, 
    if(t4.iid=10,"Inhibitor",if(t4.iid=11,"Activator", if(t4.iid=12,"Cofactor","Else"))) as `Tag` ,
    t5.floatV as `K_I_value`,
    SUBSTRING(t6.strv,1,14) as `first14Inchikey`
    from main as t1 # level of compound under the reaction
    join main as t2 # level of compound itself
    on t2.cid=t1.cid and t2.iid = t1.iid
    join main as t3 # level of compound properties i.e. name
    on t3.refv = t2.uid
    join main as t6
    on t3.refv = t6.refv
    join main as t4 # level of inhibitor properties i.e inhibitory tag
    on t4.refv = t1.uid
    join main as t5 # level of inhibitor properties i.e kinetic parameter K_I
    on t5.refv = t1.uid
    where t1.refv in 
    (select uid from main where refv = %s and cid = 6 and iid = 1) and t1.cid = 4
    and t2.refv = 0 and t3.cid = 5 AND t3.iid in (1,2,3) and t4.iid in (10,11,12) and t5.iid = 18
    and t6.cid = 5 and t6.iid = 7 order by uid, CHAR_LENGTH(t3.strv) ASC;
    """
    )
    parameter           = (ec_obj.uid,)
    # print(parameter)
    regulator_list_tuple = get_db_info(query,parameter)
    regulator_list_obj   = []
    for item in regulator_list_tuple:
        regulator_list_obj.append(cl.Regulator(name="",cid=item[0],iid=item[1],\
            uid=item[2],comment=item[3],floatv=item[4],structure=item[5]))
    return regulator_list_obj

def generate_organism_list():
    """
    enerate_organism_list loads a list of unique organisms in the database and save it localy.
    save a json file for all unique organisms in the data folder
    """
    keys = ['name', 'cid','iid']
    Organism_list_dict = []
    if os.path.exists(c.organism_list_file):
        print("Loading Organism List")
        with open(c.organism_list_file) as json_file:
            Organism_list_dict = json.load(json_file)
            
    else:
        print("Query db for Organisms ...")
        query           = "select distinct t2.strv,t1.cid,t1.iid from main t1 \
            inner join main t2 on t1.uid=t2.refv where t1.cid = 1 and t1.refv = 0\
                 and t2.cid = 5 and t2.iid = 1 and t2.row=1;"
        organism_list = get_db_info(query)
        Organism_list_dict = [dict(zip(keys, organism)) for organism in organism_list]
        
        with open(c.organism_list_file,'w') as of:
            json.dump(Organism_list_dict, of, indent=4)
    
    # convert dictionary to list of objects       
    Organism_list_obj = []
    print("Creating Organism List Obj ...")
    for val in Organism_list_dict:
        Organism_list_obj.append(cl.Organism(name=val["name"],cid=val["cid"],iid=val["iid"]))
    return Organism_list_obj


def generate_EC_list(new_Organism_Obj):
    """
    generate_EC_list Loads a list of unique EC numbers from LMSE DB for each organism.

    returns: a list of ec objects
    """ 
    parameters      = (new_Organism_Obj.cid, new_Organism_Obj.iid)
    query           = "select t5.strv,t4.cid,t4.iid, t3.uid from main t1 inner join main t2 \
        on t1.uid = t2.refv inner join main t3 \
            on t3.refv = t2.uid inner join main t4\
                on t4.cid=t3.cid and t4.iid = t3.iid \
                    inner join main t5 on t5.refv = t4.uid\
                        where t1.cid = %s and t1.iid = %s and t2.cid = 6 and \
                            t4.refv = 0 and t5.cid = 5 and t5.iid = 17"
    EC_list_tuple = get_db_info(query, parameters)
    EC_list_obj   = []
    for item in EC_list_tuple:
        EC_list_obj.append(cl.EC_number(name=item[0],cid=item[1],iid=item[2],uid=item[3]))
    return EC_list_obj
    