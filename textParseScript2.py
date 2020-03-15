import re
from collections import namedtuple
import pandas as pd
from sqlalchemy import create_engine


deptList=["ANTH","APPM","ARAB","ARTF","ARTH","ARTS","ARSC","ASIA","ASTR","ATOC","CWC","CAM","CEES","CHE","CHIN","GRE","CLAS","DNC","EBIO","ECO","ENGL","ENVS","ETHN","FARR",
"FREN","GEO","GEOL", "GRM","GSLL","HEBR","HIND","HIST","HON","HUM","INDO","IPHY","IAFS","ITAL","JPNS","JWST","KREN","LGTC",
"LGBT","LING","MATH","MCD","MUS","NRS","PACS","PHIL","PHYS","PSCI","PORT","PSYC","RLST","RUSS","SCAN","SOCY","SPAN","SLHS",
"THTR","WRT","ASEN","AREN","ATLS","CHE","CVEN","CSCI","ECEN","EHO","EME","EVEN","GEE","HUE","MCE","TLEN","APRD","COM","CMD",
"INFO","JRNL","MDST","CMCI","IAWP","MUS","MUEL","EMU","PMU","TMUS","AIRR","MILR","NAVR","PRLC","ACCT","BAD","BCO","BPOL","BSL","CESR","ESBM",
"FNCE","INBU","MGM","MKT","MBAX","MBA","MSBX","OPIM","ORM","REAL","ARC","ENVD","EDU","LEAD","LAW"]

compList=["REC","LEC","SEM","LAB","PRA","MLS","FLD","THE"]

classInfo = namedtuple("classInfo",["dept","deptNum","sectionNum","sessionNum","classNum","credits","courseTitle","classComp","startTime","endTime","days","roomNum","profName","maxEnr","campus"])
classDictList=[]

def grabClassInfo(textLine):
    attrList= [""]*15
    temp = textLine.split(" ")
    tempString=""
    x=6
    y=temp[6]

    attrList[0],attrList[1],attrList[2],attrList[3],attrList[4],attrList[5]=temp[0],temp[1],temp[2],temp[3],temp[4],temp[5]

    for i in temp[x:]:
        if i in compList:
            break
        else:
            x+=1
            tempString=" ".join((tempString,i))

    attrList[6]=tempString.lstrip()
    tempString=""
    attrList[7] = temp[x]
    x+=1

    if temp[x+1]=="AM":
        attrList[8]="".join((temp[x],temp[x+1]))
        attrList[9]="".join((temp[x+3],temp[x+4]))
        x+=5

    elif temp[x]=="-" and ":" in temp[x+1]:
        attrList[9]="".join((temp[x+1],temp[x+2]))
        x+=3

    else:
        x+=1

    attrList[10]=temp[x]

    x+=1
    tempString=""

    while "," not in temp[x]:
        tempString=" ".join((tempString,temp[x]))
        x+=1

    attrList[11]=tempString.lstrip()
    tempString=""

    while not temp[x][0].isdigit():
        tempString=" ".join((tempString,temp[x]))
        x+=1

    attrList[12],attrList[13] = tempString,temp[x]
    tempString=""

    for i in range(x+1,len(temp)):
        tempString= " ".join((tempString,temp[i]))

    attrList[14]=tempString.strip()

    newTuple = classInfo._make(attrList)
    newOD=newTuple._asdict()
    newDict = dict(newOD)
    classDictList.append(newDict)

with open("test3trimmed.txt","r") as infile:

    while True:
        line = infile.readline()
        if not line:
            break

        try:
            if line[:4] in deptList and line[6].isdigit():
                grabClassInfo(line)

        except:
            pass

    classFrame = pd.DataFrame(classDictList)

    engine=create_engine('sqlite://',echo=False)
    classFrame.to_sql('classes',con=engine)
    testResult = engine.execute("SELECT courseTitle FROM classes")

    for row in testResult:
        print("CourseTitle:",row['courseTitle'])
