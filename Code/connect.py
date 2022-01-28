#%%
import mysql.connector
from mysql.connector import errorcode
import sys
try:
    cnx = mysql.connector.connect(user='***',password='***',host='***',database='***')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = cnx.cursor()
# print(dir(cursor))
# cnx.close()

# print(dir(cursor))
# selecting target organism's cid and iid
query = ("""select cid,iid, uid from main where uid in 
(select refv from main where refv in (select uid from main 
where cid =1 and refv = 0) and strv = %s)""")
organism = ('escherichia coli',) # which organism is your target
try:
    cursor.execute(query, organism)
    row = cursor.fetchone()
except Exception as a:
    print("Something is wrong in query one:")
    print(a)
    cnx.close()

if row == None:
    print("no results for organism {}".format(organism[0]))
else:
    organism_cid = row[0]
    organism_iid = row[1]
    organism_uid = row[2]
    print("the organism has a cid of {} an iid of {} and a uid of {}".format(organism_cid,organism_iid, organism_uid))
    
    
# select target EC number's cid and iid
cursor.reset()
query = ("""select cid, iid, uid from main where 
uid in (select refv from main where refv in 
(select uid from main where cid = 2 and refv = 0) 
and iid = 17 and strv = %s)""")
ec_number = ("1.1.1.1",)
try:
    cursor.execute(query, ec_number)
    row = cursor.fetchone()
except Exception as A:
    print("Something is wrong in query two:")
    print(A)
    cnx.close()
if row == None:
    print("no results for ec number {}".format(ec_number[0]))
    cnx.close()
    sys.exit()

EC_number_cid = row[0]
EC_number_iid = row[1]
print("the target EC number has a cid of {} and iid of {}".format(EC_number_cid,EC_number_iid))
    
# fetch all compounds linked to the reaction in the specific organism
cursor.reset()
query = (
"""(select cid,iid,uid from main where refv in 
(select uid from main where refv in 
(select uid from main where refv in 
(select uid from main where refv = %s and cid = 6 and iid = 1) 
and cid = %s and iid = %s) and cid = 6 and iid = 1))"""
 )
try:
    parameters = (organism_uid,EC_number_cid,EC_number_iid)
    cursor.execute(query,params=parameters)
    row = cursor.fetchone()
    compound_cid=[]
    compound_iid=[]
    compound_uid =[]
except Exception as B:
    print("Something is wrong in query three:")
    print(B)
    cnx.close()
while row != None:
    print(row[0])
    compound_cid.append(row[0])
    compound_iid.append(row[1])
    compound_uid.append(row[2])
    row = cursor.fetchone()
print("compounds with cid of {}, iid of {} and uid of {} are potential regulators".format(compound_cid,compound_iid,compound_uid))

# obtaining the KI values for these compounds
cursor.reset()
cursor.execute("select floatV from main where refv in (%s) and iid = 18 and cid = 5" % ",".join(map(str,compound_uid)))
# cursor._executed
kinetic_param=[]
row = cursor.fetchone()
while row != None:
    kinetic_param.append(row[0])
    row = cursor.fetchone()
print(kinetic_param)
cnx.close()
# %%
