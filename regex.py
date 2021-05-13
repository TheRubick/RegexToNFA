#0 for concat, 1 for oring, 2 for repeat, 3 for single character
#((0|1)*+(01))
#((C)*+(01))
#(D+(01))
#(D+E)
#Z
import re
table = {'Z':{"operation":1,'oprd1':'D', 'oprd2':'E' },
        'D':{'operation':2,'oprd1':'C', 'oprd2':-1 },
        'C':{'operation':1,'oprd1':'0', 'oprd2':'1' },
        'E':{'operation':0,'oprd1':'0', 'oprd2':'1' }}

#check any invalid character in the input or invalid sequences of characters
def isValidInput(regex):
    for i in regex:
        '''
        n-make sure en el mawdo3 kolo mortbet bel validation msh b2ny abdel el invalid char
        n3ml check 3la 7etet el numbers hal hya valid wala la2
        @TODO yryt nkml ba2yt el validation cases zay maslan el *A,**,*|*,() order and position,etc..
        '''
        if(
            ((ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 65 and ord(i) <= 90)) or
            i in ['+','|','*','(',')']
        ):
            print(i)
        else:
            print("invalid character !!",i)
            return False
        print(ord(i))
    if(re.findall("\*{2,}",regex) or re.findall("\|{2,}",regex) 
        or re.findall("\|\*+",regex)):
            print("invalid sequence")
            return False
    return True

def checkParantheses(counterCheck,counter,regex):
    if(counter == len(regex)):
        return counterCheck
    if(regex[counter] == "("):
        counterCheck += 1
    if(regex[counter] == ")"):
        counterCheck -= 1
    if(counterCheck < 0):
        return -1
    return checkParantheses(counterCheck,counter+1,regex)

def makeRegexDic(regex):
    dicRegex = {'operation':None,'oprd1':None, 'oprd2':-1}
    if('|' in regex or '+' in regex): #regex is oring
        regex = regex.replace('+','|')
        dicRegex['operation'] = 1
        dicRegex['oprd1'] = regex.split('|')[0][:-1] if "$" in regex.split('|')[0] else regex.split('|')[0]        
        dicRegex['oprd2'] = regex.split('|')[1]
    elif('*' in regex): #in case of repeation "*"
        dicRegex['operation'] = 2
        dicRegex['oprd1'] = regex.split('*')[0]
    elif(regex.count("$") == 2): #in case of concatenate
        regex = regex[:-1]
        dicRegex['operation'] = 0
        dicRegex['oprd1'] = regex.split('$')[0]
        dicRegex['oprd2'] = regex.split('$')[1]
    elif(regex.count("$") == 1 and regex[len(regex)-1] != "$"):
        dicRegex['operation'] = 0
        dicRegex['oprd1'] = regex.split('$')[0]
        dicRegex['oprd2'] = regex.split('$')[1]
    elif(len(regex) == 2):
        dicRegex['operation'] = 0
        dicRegex['oprd1'] = regex[0]
        dicRegex['oprd2'] = regex[1]
    elif(len(regex) == 1):
        dicRegex['operation'] = 3
        dicRegex['oprd1'] = regex
    else: return {} #it means that the regex is empty
    return dicRegex

table1 = {}
def buildTable(counter,globalCounter,regex):
    dic = {}
    regexNodes = []
    regexSplit = ""
    while(counter < len(regex)):
        print(counter,' ',len(regex))
        if(regex[counter] == ")"):
            #dic = makeRegexDic(regexSplit)
            #print(dic)
            #print("finished")
            #table1['Node'+str(globalCounter)+"$"] = dic
            if(len(regexNodes) > 1):
                finalRegex = "".join(regexNodes[0]) + regexSplit + "".join(regexNodes[1])
                print(finalRegex)
                dic = makeRegexDic(finalRegex)
                table1['Node'+str(globalCounter)] = dic
                globalCounter += 1
            print("global = ",globalCounter)
            return counter,'Node'+str(globalCounter-1),globalCounter
        elif(regex[counter] == "("):
            counter,newNodeName,globalCounter = buildTable(counter+1,globalCounter,regex)
            if(len(regexNodes)):
                print("".join(regexNodes)+regexSplit+newNodeName)
                dic = makeRegexDic("".join(regexNodes)+regexSplit+newNodeName)
                table1['Node'+str(globalCounter)] = dic
                regexNodes = ['Node'+str(globalCounter)+"$"]
                globalCounter += 1
                regexSplit = ""
            else:
                regexNodes.append(newNodeName+"$")
        elif(regex[counter] == "*"):
            if(len(regexNodes) > 0):
                dic = makeRegexDic("".join(regexNodes)+"*")
                #print(dic)
                #print("finished")
                table1['Node'+str(globalCounter)] = dic
                #print(table1)
                print(regexNodes)
                print('Node'+str(globalCounter-1)+"$")
                regexNodes.remove('Node'+str(globalCounter-1)+"$")
                regexNodes.append('Node'+str(globalCounter)+"$")
                globalCounter += 1
            else:
                return len(regex),"None",-5
        elif(regex[counter] == "+" or regex[counter] == "|"):
            if(len(regexNodes) > 0):
                regexSplit = "+"
            else:
                return len(regex),"None",-5
        elif(len(regexNodes)):
            print("".join(regexNodes)+regexSplit+regex[counter])
            dic = makeRegexDic("".join(regexNodes)+regexSplit+regex[counter])
            table1['Node'+str(globalCounter)] = dic
            regexNodes = ['Node'+str(globalCounter)+"$"]
            globalCounter += 1
            regexSplit = ""
        else:
            regexNodes.append(regex[counter]+"$")

        counter += 1
    if(len(regexNodes) > 1):
        finalRegex = "".join(regexNodes) + regexSplit
        print(finalRegex)
        dic = makeRegexDic(finalRegex)
        table1['Node'+str(globalCounter)+"$"] = dic
        globalCounter += 1
    print("returning",regexNodes)
    return counter,regexNodes[0],globalCounter

regex = "(1+0)*1"
regex = "(a|b)*abb"
regex = "(1(1+0)00)|1"
isValidInput(regex)

regex = "(1(1+0)00)|1"
print(checkParantheses(0,0,regex))
ret1,ret2,flag = buildTable(0,0,regex)
print(flag)
print("printing the table")
print(table1)
#print(makeRegexDic("1$Node$"))
#def buildTable()