lineList = []
classDict={}
classToggle= False
count=0

def grabClassInfo(lineList,classDict):
#dept,coursenmbr,(sectionNum sess# classNBR), (hrs name of class),
# classCompnent, time, days, room, prof, (numStudents campus)


with open('test.txt','r') as file:
    while True:
        line = file.readline()
        if not line:
            break

        line=line.rstrip('\n')
        line=line.rstrip()

        if 'ANTH' in line and not classToggle:
            classToggle=True
            lineList.append(line)
            count=1
        elif 'ANTH' in line and classToggle:
            grabClassInfo(lineList,classDict)
            lineList=[line]
            count=1
        elif classToggle:
            count+=1

            if count==3:
                temp = line.split(' ')
                for x in temp:
                    lineList.append(x)
            elif count == 4:
                lineList.append(line[0])
                lineList.append(line[2:])
            elif count==6:
                lineList.append(line[:8])
                lineList.append(line[11:])
            elif count==9:
                if line[]


            lineList.append(line)

        elif line.find('Page')!=-1:
            classToggle=False
            count = 0
