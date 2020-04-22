from collections import namedtuple
import pandas as pd
from tika import parser
import os
from os import path
import click
from flask.cli import with_appcontext
import sys


deptList=["ANTH","APPM","ARAB","ARTF","ARTH","ARTS","ARSC","ASIA","ASTR","ATOC","CWC","CAM","CEES","CHE","CHIN","GRE","CLAS","DNC","EBIO","ECO","ENGL","ENVS","ETHN","EDU","FARR",
"FREN","GEO","GEOL", "GRM","GSLL","HEBR","HIND","HIST","HON","HUM","INDO","IPHY","IAFS","ITAL","JPNS","JWST","KREN","LAW","LGTC",
"LGBT","LING","MATH","MCD","MUS","NRS","PACS","PHIL","PHYS","PSCI","PORT","PSYC","RLST","RUSS","SCAN","SOCY","SPAN","SLHS",
"THTR","WRT","ASEN","AREN","ATLS","CHE","CVEN","CSCI","ECEN","EHO","EME","EVEN","GEE","HUE","MCE","TLEN","APRD","COM","CMD",
"INFO","JRNL","MDST","CMCI","IAWP","MUS","MUEL","EMU","PMU","TMUS","AIRR","MILR","NAVR","PRLC","ACCT","BAD","BCO","BPOL","BSL","CESR","ESBM",
"FNCE","INBU","MGM","MKT","MBAX","MBA","MSBX","OPIM","ORM","REAL","ARC","ENVD","EDU","LEAD","LAW"]

compList=["REC","LEC","SEM","LAB","PRA","MLS","FLD","THE"]

classInfo = namedtuple("classInfo",["classDept","classCourseNum","classSectionNum","classSessionNum","classClassNum","classCredits","classTitle","classComponent","classBuilding","classRoom"])

abbrevList = ["WLAW","EDUC","HLMS","CLRE","MUEN","FLMG","DUAN","MATH","ENVD","ECCR","MCOL","KOBL","CASE","CHEY","KTCH","WVN","STAD","MUS","MCKY","CEDU","ARMR","VAC","ECNT","LIBR","HUMN","GUGG","ECON","ITLL","ECCE","ATLS","EKLC","KCEN","LESS","ECEE","ECST","DLC","ECES","CLUB","CHEM","HALE","IBS","OBSV","BESC","AERO","SEEC","RAMY","THTR","CARL","GOLD","PORT","MKNA","SLHS","BIOT","FRND"]

def init_app(app):
    app.cli.add_command(pdf_to_text_command)


@click.command('pdfToText')
@with_appcontext
def pdf_to_text_command():
    pdfToText()
    click.echo('pdf converted')


def pdfToText(outfile="classData.txt",filepath="spring2020class_schedule.pdf"):
    with open(outfile,'w') as output:
        with open('temp.txt','w+') as tempFile:
            pdfData = parser.from_file(filepath)
            pdfText = pdfData['content']
            tempFile.write(pdfText)

            for line in tempFile:
                if line.strip():
                    output.write(line)


        os.unlink('temp.txt')

    return True


def grabClassInfo(currLine,dataList):
    attrList = [""]*15
    temp = currLine.split(" ")
    tempString=""
    x=6
    y=temp[6]
    attrList[0], attrList[1], attrList[2], attrList[3], attrList[4], attrList[5] = temp[0].strip(), temp[1].strip(), temp[2].strip(), temp[3].strip(), \
                                                                                   int(temp[4]), temp[5].strip()

    for i in temp[x:]:
        if i in compList:
            break
        else:
            x += 1
            tempString = " ".join((tempString, i))

    attrList[6] = tempString.strip()
    tempString = ""
    attrList[7] = temp[x].strip()
    x += 1

    if temp[x + 1] == "AM":
        attrList[8] = "".join((temp[x], temp[x + 1]))
        attrList[9] = "".join((temp[x + 3], temp[x + 4]))
        x += 5

    elif temp[x] == "-" and ":" in temp[x + 1]:
        attrList[9] = "".join((temp[x + 1], temp[x + 2]))
        x += 3

    else:
        x += 1

    attrList[10] = temp[x].strip()

    x += 1
    tempString = ""


    # right now have problem here because in instances with no prof will go out of index
    for x,substring in enumerate(temp[x:len(temp)]):
        if ',' not in substring:
            tempString = " ".join((tempString, substring))

        else:
            attrList[11] = tempString
            attrList[12] = " ".join((substring,temp[x+1]))


    newTuple = classInfo._make(attrList)
    newOD = newTuple._asdict()
    newDict = dict(newOD)
    dataList = dataList.append(newDict)
    return dataList


def grabClassInfo2(line,data_list):
    attrList = [""]*10
    temp = line.split(" ")

    attrList[0] = temp[0]
    attrList[1] = temp[1]
    attrList[2] = temp[2]
    attrList[3] = temp[3]
    attrList[4] = temp[4]
    attrList[5] = temp[5]

    temp_string = ""
    temp_x = 6

    while temp[temp_x] not in compList:
        temp_string = " ".join((temp_string,temp[temp_x]))
        temp_x+=1

    attrList[6] = temp_string
    attrList[7] = temp[temp_x]

    while temp[temp_x] not in abbrevList:
        temp_x+=1

    attrList[8] = temp[temp_x]
    attrList[9] = temp[temp_x+1]
    newTuple = classInfo._make(attrList)
    newOD = newTuple._asdict()
    newDict = dict(newOD)
    data_list = data_list.append(newDict)
    return data_list




def text_to_dataframe(infile="classData.txt"):

    dataList = []

    with open(infile,"r") as input:
        while True:
            line = input.readline()
            if not line:
                break
            try:
                grabClassInfo2(line,dataList)
            except:
                pass

        classesFrame = pd.DataFrame(dataList)
        return classesFrame

