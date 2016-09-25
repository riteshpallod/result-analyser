import re
import sys
"""
Updates:
Changed database system. Using sqlite3 instead of mysql.
Everything but adding columns (read sem1,2) is working.
"""

import sqlite3
cursor = sqlite3.connect('test.db')
print "Opened database successfully";
#tatus table will store seat no,marks,total marks and result of all the students
sql="CREATE TABLE IF NOT EXISTS tatus(SEAT_NO VARCHAR(15),got_of int,out_of int,result_comment VARCHAR(40),special_rc VARCHAR(40), PRIMARY KEY(SEAT_NO));"
cursor.execute(sql)
cursor.commit()
#function to check the type of subject
types=["PP", "TW", "PR", "OR"]
def in_types(mystring):
    if mystring=="PP":
        return (1)
    else:
        return (0)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#person class will store the student information like name,seat no,mother's name, prn no. and college name
class person:
    def add_attr(self,name,seat_num,mother,PRN,college):
        self.name=name.lstrip()
        self.seat_num=seat_num.lstrip()
        self.mother=mother.lstrip()
        self.PRN=PRN.lstrip()
        self.college=college.lstrip()
#function to display student information
    def display(self):
        print "Seat:", self.seat_num
        print "Name:", self.name
        print "Mom:", self.mother
        print "PRN:", self.PRN
        print "college:", self.college

regexp=re.compile(r'S[0-9]') #to extract seat no
list_of_objects=[] #to store the objects of class person in an array

def convert_into_nice_shit(seat_bro, array,flagm,types1=types):
    semester_name="sem"+str(flagm)
    #create table according to semester number having fields seat no
    try:
        sql="CREATE TABLE IF NOT EXISTS %s ( SEAT_NO VARCHAR(15) NOT NULL, PRIMARY KEY(SEAT_NO) );" %(semester_name)
        cursor.execute(sql)

    except:
        cursor.rollback()
    try:
        sql="INSERT INTO %s(SEAT_NO) VALUES ('%s')" %(semester_name,seat_bro)#insert into table semester_name value-seat no
        cursor.execute(sql)
        cursor.commit()
    except:
	 # Rollback in case there is any error
        cursor.rollback()
    pp_flag=0
    if flagm > 2:
        return
    stupidstatus=[]
    subject_string=""

    my=""
    objsathi=""
    subject_code=array[0] #subject code is at starting of the line
    K=0
    flag_OBJECTORIENTED=0
    for i in range(1,len(array)):
        if array[i] in types1: #check int?
            pp_flag=in_types(array[i]) #to check if the line is of type PP(theory exam)
            K=i #store the index in variable 'K'
            break
        if array[i].isdigit()==True:
	    #will come here directly if subject name gets attached with subject type(PP,TW,PR) and then we separate the subject name from type
            my=array[i-1]
            chara=my[-2:] #chara is my(pun intended) type
            objsathi=my[0:-2] #objsathi is my ka subject
            if chara in types1:
                pp_flag=in_types(chara)
            flag_OBJECTORIENTED=1
            K=i-1
            break
    for i in range(1,K):
        subject_string+=array[i]+" "
    if flag_OBJECTORIENTED==1:
        subject_type=chara
        subject_string+=" "+objsathi
    else:
        subject_type=array[K]
    max_marks=array[K+1]
    min_marks=array[K+2]

    pal=K+3
    rit=pal

    if pp_flag==1: #if paper type if PP then two marks will be allocated(th_1 and th_2)
        th_1=array[pal]
        th_2=array[pal+1]
        rit=pal+2

    oe_marks=array[rit] #overall marks
    A=0
    for i in range(rit+1,len(array)):
        if is_number(array[i])==True:
            A=i
            break
        stupidstatus.append(array[i])

    #this pos creates subject table for particular semester having subject code,type,max marks and min marks
    #there will be two such tables for two semesters
    subject_waala_table="subjectcodes_"+semester_name
    try:
        sql="CREATE TABLE IF NOT EXISTS %s ( code int(6) NOT NULL, type VARCHAR(3) NOT NULL, name VARCHAR(50), max_marks int(2), min_marks int(2), PRIMARY KEY (code,type));" %(subject_waala_table)
        cursor.execute(sql)
        cursor.commit()
    except:
	 # Rollback in case there is any error
        cursor.rollback()
	#now insert into the subject_code table
    try:
        sql="INSERT INTO %s (code,type,name,max_marks,min_marks)VALUES (%d, '%s', '%s', %d, %d);" %(subject_waala_table,int(subject_code),subject_type,subject_string,int(max_marks),int(min_marks))
        cursor.execute(sql)
        cursor.commit()
    except:
        # Rollback in case there is any error
        cursor.rollback()
    """
    this pos adds columns into table sem1(if they dont exist) or sem2 which will have seat_no and column having name(coe_oe):subject_code+subject_type.
    """
    coe_oe=subject_code+subject_type
    try:
        sql="ALTER TABLE %s ADD COLUMN '%s' int;" %(semester_name,coe_oe)
        cursor.execute(sql)
        cursor.commit()
    except:
    # Rollback in case there is any error
        #print ("roll back. Shit.")
        cursor.rollback()
    try:
        sql="UPDATE %s SET '%s'=%d WHERE SEAT_NO='%s';" %(semester_name,coe_oe,int(oe_marks),seat_bro)
        cursor.execute(sql)
        cursor.commit()
    except:
        # Rollback in case there is any error
        cursor.rollback()
    """
    print "subjectcode:", subject_code
    print "subject:", subject_string
    print "subject_type:", subject_type
    print "max_marks:", max_marks
    print "min_marks", min_marks
    if pp_flag==1:
        print "th_1:", th_1
        print "th_2", th_2
    print "oe_marks", oe_marks
    print "status:", stupidstatus
    """
    flagm+=1 #add 1 to flagm which stores the semester number. If flagm=2 then second semester is printed
    if (flagm==2):
        array1=array[A:len(array)+1]
        if array[0]==array1[0]:
            return #softskills will not print (twice)
        """
        for sige sem, check again
        """
        ##kuch nahi aage, print (s itself
        if array1[0].isdigit()==True:
            convert_into_nice_shit(seat_bro,array1,flagm)#now convert for second sem in same manner


#main
infile = open("0comp.txt", "r") #using file 0comp.txt which has data for computer department results
aapla_seat=""
regexp=re.compile(r'[S|B|T][0-9]')#change 'S' or add [S|B|T]
x=0
seat_num_for_status=""
for line in infile:
    flag_finish=0
    elements=line.split()
    lines=line.split(',')

    if len(elements) > 0:
        if regexp.search(lines[0]) is not None:
            flag_finish=1
            ##First line code here
            dummy=person() #create object of type person
            withoutcomma=lines[0].split()


            sea=withoutcomma[0] #first field is seat no
            seat_num_for_status=sea.strip()
            mom=withoutcomma[len(withoutcomma)-1] #last field of lines array is mother' name
            nae=""
            for i in range(1, len(withoutcomma)-1 ):
                nae=nae+" "+withoutcomma[i] #store name of candidate
    #        for range (len(lines)-1, 0, -1)
            college=lines[2]
            PRN=lines[1]
            aapla_seat=sea
            dummy.add_attr(nae,sea,mom,PRN,college) #store the extracted values in object of person class
            print "\n"
            dummy.display() #display details of person object using display() function
            print sea.strip()
            try:
                sql="INSERT INTO student_INFO (SEAT_NO,NAME_OF_THE_CANDIDATE,MOTHER,PERMANENT_REG_NO,COLLEGE) VALUES ('%s', '%s', '%s', '%s', '%s');" %(sea.strip(),nae.strip(),mom.strip(),PRN.strip(),college.strip())
                cursor.execute(sql)
                cursor.commit()
            except:
                # Rollback in case there is any error
                print ("Bhau, zala re rollback!")
                cursor.rollback()
            x=x+1
            list_of_objects.append(dummy) #append object into array of objects(list_of_objects)

        elif elements[0].isdigit(): #if first field is not seat_no then check if it is containing marks of the candidate
            flag_sem=0
            #Asuming that the sentence will have 2 sems
            """
            OK, so everything seems fine.
            Only, for BE results, the second semester has one-two extra subjects
            To tackle this, we must use a counter. We count the number of spaces
            If the spaces are beyond a certain count, we must consider the
            subject in secondsem.
            We wont face this problem in a scenario where first sem has more
            subjects
            """
            if len(line) > 90 and len(line.split())< 15:
                print ("in second sem only")
                convert_into_nice_shit(sea.strip(),elements,2) #2 means sem2
            else:
                convert_into_nice_shit(sea.strip(),elements,1)#1 means sem1
            flag_finish=2

        if flag_finish == 0 or flag_finish == 3:
            '''for second,third empty, near empty lines
                we don't write code.
                Asuming the subjects are filled, this is "grand", "result"
                check
            '''
            got=""
            out_of=""
            if "TOTAL" in line: #if TOTAL is in line then it will have grand total and result
                #print line.strip()
                grand_array = line.split()
                for i in range(0,len(grand_array)): #check if Grand Total '=' is there
                    if grand_array[i] == "=":
                        K=i
                        break
                for j in range(K+1, len(grand_array)): #then check if '/' is there
                    if "/" in grand_array[j]:
                        L=j
                        break

                total_score=""
                for h in range(K+1,L+1):
                    total_score+=grand_array[h]
                got, out_of = total_score.split('/') #split across '/' i.e. got is to left of / and out_of is to right of /

                """
                for grace marks, we need to convert the total, no, we leave that as it is.
                for later use:
                    import compiler
                    eq= "sin(x)*x**2"
                    ast= compiler.parse( eq )
                """

                print total_score
                #print "got: ", got
                #print "out_of: ", out_of
                if got.isdigit()==True: #if total is pure integer then store it as it is
                    got_of=int(got.strip())
                else: #otherwise if '--' is present then make it 000
                    got_of=000

                result_comment=""
                flagq=0
                dummy_stat= grand_array[L+1:]
                for ij in range(L+1, len(grand_array)):
                    if flagq==1:
                        result_comment=result_comment+" "+grand_array[ij]
                    if grand_array[ij]== ":": #make flagq=1 if Result ':' is found then we can put that value in result_comment
                        flagq=1
                #print result_comment.strip()
		#insert the above extracted values in 'tatus' table which will have final result of the candidate
                try:
                    sql="INSERT  INTO tatus(SEAT_NO,got_of,out_of,result_comment) VALUES ('%s',%d, %d,'%s')" %(aapla_seat,got_of,int(out_of),result_comment.strip())
                    print "done"
                    cursor.execute(sql)
                    cursor.commit()
                except:
                    print "Need to work on status."
                    cursor.rollback()

            special_result_comment=""
            #special_result_comment will store 'NULL' or 'RESULT RESERVED FOR BACKLOGS.'
            if "RESULT" in line: #this line will be present if RESULT RESERVED FOR BACKLOGS. is present
                special_result_comment= line
		#now update the table to store the special_result_comment as it does not store in the insert command
                try:
                    sql="UPDATE tatus SET special_rc='%s' WHERE SEAT_NO='%s';" %(special_result_comment,aapla_seat,)
                    cursor.execute(sql)
                    cursor.commit()
                except:
                    # Rollback in case there is any error
                    cursor.rollback()
                #print special_result_comment.strip()
            #print ("\n")
            """
            Dumping in the table.
            """
            if got.isdigit() == False:
                got = -1;


            flag_finish=3

#Done. if eof is reached then print the flag_finish and close the file

print (flag_finish)
infile.close()
