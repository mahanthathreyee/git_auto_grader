import sys
import os
import re
import glob
import shutil


def fileReader(filePath):
    flag = True
    studentDict = {}
    with open(filePath, 'r') as f:
        for line in f:
            if (line != '\n'):
                if (flag):
                    flag = False
                    continue

                wordList = re.split("\s|,", line)
                fullName = ''
                for idx in range(1, len(wordList)-1):
                    if (wordList[idx].isnumeric()):
                        break

                    if (wordList[idx] != ' '):
                        fullName += wordList[idx].lower()
                fullName = fullName.replace(".", "")
                fullName = fullName.replace("-", "")
                fullName = fullName.replace("'", "")
                studentDict[fullName] = 1
    return studentDict


def groupDivider(directoryPath, studentDict, numGroups):
    numSubmissions = len(glob.glob(directoryPath+'/*.zip'))
    dirList = os.listdir(directoryPath)
    studentsPerGroup = int(numSubmissions / numGroups)

    numStudentsInGroup = 0
    currGroup = 0
    restart = False

    for student in studentDict:
        # print(student)
        match = glob.glob(directoryPath + "/"+student+"*")
        # print(match)
        if (len(match) != 0):
            if (numStudentsInGroup < studentsPerGroup):
                numStudentsInGroup += 1
            else:
                currGroup += 1
                if (currGroup == numGroups):
                    currGroup = 0
                    restart = True

                if (restart):
                    numStudentsInGroup = studentsPerGroup - 1

                else:
                    numStudentsInGroup = 1

            loc = "/G" + str(currGroup)+"/"
            # print(loc)
            path = directoryPath + loc
            shutil.copy(match[-1], path)

    return


def initFunction():
    print("Welcome to Group Divider!")
    numGroups = 7  # int(input("Please enter the number of Groups"))

    directoryPath = ''
    filePath = ''
    if len(sys.argv) >= 2:
        directoryPath = sys.argv[2]
        filePath = sys.argv[1]
    else:
        print('Please Include a file path')
        sys.exit()

    if (directoryPath[-1] != '/'):
        directoryPath += '/'

    for i in range(numGroups):
        directory = "G"+str(i)
        # print(directoryPath)
        path = directoryPath + directory
        # print(path)
        if (not os.path.exists(path)):
            try:
                os.mkdir(path)

            except PermissionError:
                print("Please Enable permissions")
                print("Alternatively, Please create " + str(numGroups) +
                      " folders with names 'G0','G1'... so on in the submissions directory")

    studentDict = fileReader(filePath)
    groupDivider(directoryPath, studentDict, numGroups)

    numsub = 0
    totalSub = 0
    for i in range(numGroups):
        directory = "G"+str(i)
        # print(directoryPath)
        path = directoryPath + directory
        numsub = len(glob.glob(path+'/*'))
        print("The number of submissions in group " +
              str(i) + " is " + str(numsub))
        totalSub += numsub

    print("The total number of submissions are " + str(totalSub))

    return studentDict, numGroups, directoryPath


'''
if __name__ == "__main__":
  initFunction()'''
