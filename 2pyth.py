import sqlite3
import sys

"""
commandline arguments is te_ledger.txt

this code creates columns for person_INFO
although unnecessary at first, it shows my fist try at dynamic coding here.

"""

db=sqlite3.connect("test.db")
filname=str(sys.argv[1])
f=open(filname, "r")
flag=1;
my_string=""
for line in f:
	if "SEAT NO" in line:
		my_string=line
		break
#print my_string

list_of_elements= my_string.split(',')
naya_list=[]


var31=list_of_elements[len (list_of_elements)-1].strip()
var31='_'.join(list_of_elements[len (list_of_elements)-1].split())
var3=var31.replace(".","")


sql="CREATE TABLE IF NOT EXISTS student_INFO( %s VARCHAR(15) NOT NULL, PRIMARY KEY(%s));" %(var3,var3)
db.execute(sql)
db.commit()

for i in range(1, len (list_of_elements)-1):
	var=list_of_elements[i].strip()
	var='_'.join(list_of_elements[i].split())
	var2=var.replace(".","")
	print i,var2
	"""
	add try blocks. shit gets easy.
	"""


	if i != (len(list_of_elements)-1):
		sql="ALTER TABLE student_INFO ADD COLUMN %s VARCHAR(30);" %(var2)
		db.execute(sql)

#sql="CREATE TABLE IF NOT EXISTS student_INFO( %s VARCHAR(15) NOT NULL, PRIMARY KEY(%s));" %(ori[0],ori[0])
#cursor.execute(sql)

db.commit()
db.close()
f.close()
