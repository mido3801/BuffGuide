from collections import namedtuple

classInfo = namedtuple('classInfo',['dept','deptNum','sectionNum','sessionNum','classNum','credits','courseTitle','classComp','startTime','endTime','days','roomNum','profName','maxEnr','campus'])

abbrevList=['MW','F','TTH','MWF']
lineList = []
classDict={}
classToggle= False
count=0

def grabClassInfo(lineList,classDict):
#dept,coursenmbr,(sectionNum sess# classNBR), (hrs name of class),
# classCompnent, time, days, room, prof, (numStudents campus)
    print(lineList)
    newTuple = classInfo._make(lineList)
    newDict = newTuple._asdict()
    print(newDict)

with open('test.txt','r') as file:
    while True:
        line = file.readline()
        if not line:
            break

        line=line.rstrip('\n')
        line=line.rstrip()

        print(line)

        if line.find('Page')!=-1:
            grabClassInfo(lineList,classDict)
            classToggle=False
            count = 0

        if 'ANTH' in line and not classToggle:
            classToggle=True
            lineList = []
            lineList.append(line)
            count=1
        elif 'ANTH' in line and classToggle:
            grabClassInfo(lineList,classDict)
            lineList=[]
            lineList.append(line)
            count=1
        elif classToggle:

            count+=1

            if count==3:
                temp = line.split(' ')
                for x in temp:
                    lineList.append(x)
            elif count == 4:
                if len(line)>3:
                    type=1
                    temp = line.split(' ',1)
                    for x in temp:
                        lineList.append(x)
                else:
                    type=2
                    lineList.append(line)

                #lineList.append(line[0])
                #lineList.append(line[2:])
            elif count ==5:
                if len(line)>3:
                    temp=line.split(" ",1)
                    if temp[1][0].isdigit():
                        type=3
                if type == 3:
                    lineList.append(temp[0])
                    lineList.append(temp[1][:8])
                    lineList.append(temp[1][11:])
                else:
                    lineList.append(line)
            elif count==6:
                if type==1:
                    lineList.append(line[:8])
                    lineList.append(line[11:])
                elif type == 3:
                    temp = line.split(' ',1)
                    for x in temp:
                        lineList.append(x)
                else:
                    lineList.append(line)

            elif count ==7:
                if type==1 or type==3:
                    if ',' in line:
                        lineList.append(line)
                    elif len(line)>3:
                        temp = line.split(' ',1)
                        for x in temp:
                            lineList.append(x)
                        count=8

                    else:
                        lineList.append(line)
                else:
                    if not line[0].isdigit():
                        temp = line.split(' ',1)
                        for x in temp:
                            lineList.append(x)
                    else:
                        lineList.append(line[:8])
                        lineList.append(line[11:])
            elif count == 8:
                if type==1:
                    lineList.append(line)
                else:
                    temp = line.split(' ',1)
                    for x in temp:
                        lineList.append(x)
                    if type==3:
                        count = 0

            elif count == 9:
                if not line[0].isdigit():
                    lineList.append(line)
                else:
                    temp=line.split(' ',1)
                    for x in temp:
                        lineList.append(x)
                    count=0
            elif count == 10:
                temp=line.split(' ',1)
                for x in temp:
                    lineList.append(x)
                count=0

            else:
                lineList.append(line)
