from __future__ import print_function
import os
import sys

#We use the Xpdf utility pdftotext;
filname=str(sys.argv[1]).strip()
os.system("pdftotext -layout %s" %(filname))
filnam=filname.split(".")
filnam=filnam[0]
filnam=filnam+".txt"
#opening the text file we just generated;
infile= open(filnam,"r")

#seperate txt into 3 depts, we use only comp, for now;
efile= open("0elex.txt", "w")
cfile= open("0comp.txt", "w")
itfile= open("0it.txt", "w")

x1=["SAVITRIBAI PHULE", "BRANCH", "CENTRE", "................................................................","SUB.TYPE", "MOTHER","MAX. MARKS","CARRY OVER"]

x=1
flagc="e"

infile.seek(0)
for line in infile:
    flagprint=0
    if "BRANCH" in line:
        if "(COMPUTER)" in line:
            flagc="c"
        elif "(INFORMATIOM TECHNOLOGY)" in line:
            flagc="it"
    for i in range(0,8):
        if x1[i] in line :#or "BRANCH" not in line:
            flagprint=1
    if flagprint==0:
        if flagc=="e":
            print(line.strip(),file=efile)
        elif flagc=="c":
            print(line.strip(),file=cfile)
        elif flagc=="it":
            print(line.strip(),file=itfile)

cfile.close()
efile.close()
itfile.close()
infile.close()
