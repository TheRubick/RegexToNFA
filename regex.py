#0 for concat, 1 for oring, 2 for repeat, 3 for single character
#((0|1)*+(01))
#((C)*+(01))
#(D+(01))
#(D+E)
#Z
import re
#table = {'Z':{"operation":1,'oprd1':'D', 'oprd2':'E' },
       # 'D':{'operation':2,'oprd1':'C', 'oprd2':-1 },
      # 'C':{'operation':1,'oprd1':'0', 'oprd2':'1' },
      #  'E':{'operation':0,'oprd1':'0', 'oprd2':'1' }}

def checkParantheses(counterCheck,counter,regex):
    if(counter == len(regex)):
        return counterCheck
    if(regex[counter] == "("):
        counterCheck += 1
    if(regex[counter] == ")"):
        counterCheck -= 1
    if(counterCheck < 0): # if there is a preceding ) then return
        return -1
    return checkParantheses(counterCheck,counter+1,regex)

#check any invalid character in the input or invalid sequences of characters
def isValidInput(regex):
    SpecialChars = []
    for i in regex:
        if(
            ((ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 65 and ord(i) <= 90))
            or (ord(i) >= 48 and ord(i) <= 57)
        ):
            SpecialChars.append(i)
        elif(i not in ['+','|','*','(',')']): # if the regex has character other than the valid ones
            print("invalid character !!",i)
            return None
        #print(ord(i))
    if(
        re.findall("\*{2,}",regex) or re.findall("\|{2,}",regex) # ** , ||
        or re.findall("\+{2,}",regex) or re.findall("\|\*+",regex) # ++ , |*
        or re.findall("\(\*",regex) or re.findall("\(\|",regex) # (* , (|
        or re.findall("\(\+",regex) or re.findall("\|\)",regex) # (+ , |)
        or re.findall("\+\)",regex) or re.findall("\+\*",regex) # +) , +*
        or re.findall("^\*",regex) or re.findall("^\+",regex) # start with * or +
        or re.findall("^\|",regex) or re.findall("\|$",regex) # start with | or end with |
        or re.findall("\+$",regex) # end with +
        ): 
            print("invalid sequence")
            return None
    if(checkParantheses(0,0,regex) == 0):
        return SpecialChars
    else:
        print("invalid parantheses sequence")
        return None

def makeRegexDic(regex):
    dicRegex = {'operation':None,'oprd1':None, 'oprd2':-1}
    if('|' in regex or '+' in regex): #regex is oring
        regex = regex.replace('+','|')
        dicRegex['operation'] = 1
        dicRegex['oprd1'] = regex.split('|')[0]        
        dicRegex['oprd2'] = regex.split('|')[1]
    elif('*' in regex): #in case of repeation "*"
        dicRegex['operation'] = 2
        dicRegex['oprd1'] = regex.split('*')[0][:-1]
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
    dicRegex['oprd1'] = dicRegex['oprd1'][:-1] if "$" in dicRegex['oprd1'] else dicRegex['oprd1']
    if(dicRegex['oprd2'] != -1):
        dicRegex['oprd2'] = dicRegex['oprd2'][:-1] if "$" in dicRegex['oprd2'] else dicRegex['oprd2'] 
    return dicRegex


def buildTable(counter,globalCounter,regex):
    table1 = {}
    dic = {}
    regexNodes = []
    regexSplit = ""
    while(counter < len(regex)):
        #print(counter,' ',len(regex))
        if(regex[counter] == ")"):
            if(len(regexNodes) > 1):
                finalRegex = "".join(regexNodes[0]) + regexSplit + "".join(regexNodes[1])
                #print(finalRegex)
                dic = makeRegexDic(finalRegex)
                table1['Node'+str(globalCounter)] = dic
            #print("global = ",globalCounter)
                globalCounter += 1
            if(regexNodes[0][:2] != "No"):
                globalCounter += 1
            return counter,'Node'+str(globalCounter-1),globalCounter,table1
        elif(regex[counter] == "("):
            counter,newNodeName,globalCounter,tableTemp = buildTable(counter+1,globalCounter,regex)
            tableTemp2 = table1
            table1 = {**tableTemp2 , **tableTemp}
            if(len(regexNodes)):
                #print("".join(regexNodes)+regexSplit+newNodeName)
                dic = makeRegexDic("".join(regexNodes)+regexSplit+newNodeName)
                table1['Node'+str(globalCounter)] = dic
                regexNodes = ['Node'+str(globalCounter)+"$"]
                globalCounter += 1
                regexSplit = ""
            else:
                regexNodes.append(newNodeName+"$")
        elif(regex[counter] == "*"):
            dic = makeRegexDic("".join(regexNodes)+"*")
            table1['Node'+str(globalCounter)] = dic
            #print(regexNodes)
            print('Node'+str(globalCounter-1)+"$")
            regexNodes = []
            regexNodes.append('Node'+str(globalCounter)+"$")
            globalCounter += 1
        elif(regex[counter] == "+" or regex[counter] == "|"):
            regexSplit = "+"
        elif(len(regexNodes)):
            #print("".join(regexNodes)+regexSplit+regex[counter])
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
        #print(finalRegex)
        dic = makeRegexDic(finalRegex)
        table1['Node'+str(globalCounter)+"$"] = dic
        globalCounter += 1
    #print("returning",regexNodes)
    return counter,regexNodes[0],globalCounter,table1


'''
x,y,z,table = buildTable(0,0,"(a|b)*1(f|g)")
print("printing table",table)

regex = "(1+0)*1"
regex = "(a|b)*abb"
regex = "0+*(1((0+1)*)00)"
regex = "(a|b)*1(a|b)*4(cdef)"
specialChars = isValidInput("**")
print(specialChars)

#regex = "(1)*"
print(checkParantheses(0,0,regex))
ret1,ret2,flag,table1 = buildTable(0,0,regex)
#print(flag)
print("printing the table")
print(len(table1))

#print(makeRegexDic("1$|Node1$"))
'''