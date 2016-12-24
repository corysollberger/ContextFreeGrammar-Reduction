#Homework 8 | COS451 | Cory Sollberger

from random import randint
import string

#Read the desired information from a file
def readFile(fileName):
    f = open(fileName, 'r') #opens file to read the 5 elements of the NDFA
    inpLines = []
    for line in f:
        inpLines.append(line.rstrip('\n'))

    count = 0
    R.clear()
    for x in inpLines:
        if count == 0:
            A.clear()
            for a in inpLines[count]:
                A.append(a)
        elif count == 1:
            V.clear() 
            for a in inpLines[count]:
                V.append(a)
        elif count == 2:
            S.clear() 
            for a in inpLines[count]:
                S.append(a)
        elif count >= 3:
            s = ""
            v = ""
            tempTuple = ()
            for a in inpLines[count]:
                if(a=='.'):
                    v = s
                    tempTuple += (v,)
                    s = ""
                elif(a=='|'):
                    tempTuple += (s,)
                    s = ""
                else:
                    s = s+ a
            R.append(tempTuple)
        count = count + 1

#Takes 3 inputs, Filename, Maximum Length, and Number of Derivations
#Produces Derivations using the CFG pulled from the file
def getDerivation(f, M, D):
    #readFile(f)
    #removeEps()
    print ("Randomizing Derivation...\nM = " + str(M) + "  D = " + str(D))
    for x in range(0,D):
        print ("Run " + str(x))
        temp = S[0]
        count = 0
        print ("Start: " + str(temp))
        while(count<M):
            for a in V: #Check for variables to derive
                if(a in temp):
                    val = temp.index(a)
                    middle = ""
                    for b in R: #Randomly select a derivation for a variable V
                        if (b[0] == a):
                            value = randint(0,len(b)-1)
                            if (value == 0):
                                value = value + 1
                            if (b[value] == 'e'): #Handles Eps
                                pass
                            else:
                                middle = middle + b[value]
                    first = temp[:val]
                    second = temp[val+1:]
                    temp = first + middle + second #Used to concatenate the new string
                    break
            count+=1
        print ("Derivation: " + str(temp) + "\n")

#Get the rules that have epsilon transitions
def getEps():
    l = []
    for x in R:
        for a in x:
            if (a=='e'):
                l.append(x)
    return l

#Remove epsilons and update rules
def removeEps():
    l = getEps()
    rtrn = []
    count = 0
    for x in l:
        lst = list(x)
        lst.pop(len(lst)-1)
        s = ""
        for c in x[1]:
            if (c != x[0]):
                s+=c
        lst.append(s)
        l[count] = lst
        #print (l[count])
        count += 1
    e = saveRules(l)
    modifyStart(e)
    return l
#Update the Rules
def saveRules(l):
    tmp = []
    count = 0
    for x in R:
        for a in l:
            if(x[0]==a[0]):
                tmp.append(a[0])
                R[count] = tuple(a)
                #print ("hello")
        count += 1
    return tmp

def modifyStart(l):
    temp = []
    for a in R[0]:
        temp.append(a)
        for b in l:
            if (b in a):
                d = a
                d = d.replace(b, "")
                temp.append(d)
    R[0] = tuple(temp)                

def eliminateUnitP():
    unitP = []
    #Find the unit productions
    for x in R:
        for a in range(1, (len(x)-1)):
            if (x[a] in V):
                if (x[a] not in unitP):
                    unitP.append(x[a])
    temp = []
    #Find the rules pointed from unit productions
    for x in R:
        if x[0] in unitP:
            temp.append(x)
    for x in R:
        if (x in temp):
            R.remove(x)
    tempL = []
    #Build new rules without unit productions
    for x in R: #Individual Rules
        true = False
        tempTuple = ()
        for a in x: #Elements of the rules
            if (a in unitP): #Element contains a unitProduction
                true = True
                rplc = x[0]
                for v in temp:
                    if (a in v):
                        for f in range(1, (len(x)-1)):
                            tm = v[f].replace(a, rplc)
                            tempTuple = tempTuple + (tm,)
            else:
                tempTuple = tempTuple + (a, )
                        
        if (true == False):
            tempL.append(x)
        else:
            tempL.append(tempTuple)
    return tempL

#Eliminate useless variables
#Marks variables as reachable, also marks variables as deriving to terminals
#Eliminates all productions not reachable or deriving to non-terminals
def uselessVars():
    l = [] #Holds all variables that derive to terminals
    for x in R: #Check all variables to see if they derive to terminals
        for y in x: #check if individual variable derives to a terminal
                if (y in A):
                    if (x not in l):
                        l.append(x[0])
    #Build new rule set removing all rules that contain variables that don't derive to terminals
    #add terminals to list
    for a in A:
        l.append(a)
    #add start symbol
    l.append(S[0])
    for x in R: #Rules
        for y in range(1,len(x)): #Element of rules
            dTrm = x[0] #Var that derives to term
            add = True
            for c in x[y]:
                if (c in l): #if element derives to terminal
                    pass
                else:
                    add = False
            if (add == True and dTrm not in l):
                l.append(dTrm)
    newR = []
    for x in R: #Rules
        tempTuple = ()
        for y in x: #elements of rules
            add = True
            for c in y:#chars of elements
                if c in l:
                    pass
                else:
                    add = False
            if (add == True):
                tempTuple = tempTuple + (y,)
        if (tempTuple):
            newR.append(tempTuple)
    return newR
                    
def updateVars():
    l = []
    for x in R:
        l.append(x[0])
    return l

#Find all variables of length > 2, create tuple (current, new symbol, points to)
def reduceVars(alp):
    newVars = []
    for x in R: #Rules
        for y in x: #elements of rules
            s = ""
            var = []
            count = 0 #If more than 2 variables are counted, create new rule
            for c in y:
                if (c in V):
                    #print (c)
                    count +=1
                    var.append(c)
            if (count>2):
                s += var[0] + var[1]
                if (s not in newVars and alp):
                    r = alp.pop()
                    tTuple = (r,s)
                    newVars.append(tTuple)
                    R.append(tTuple)
    newR = []
    for x in R:
        tempTuple = ()
        for y in x:
            add = True
            for z in newVars:
                if(z[1] in y):
                    if(z[0] not in x and len(x) > 2):
                        p = y.replace(z[1],z[0])
                        tempTuple = tempTuple + (p,)
                        add = False
            if(add == True):
                tempTuple = tempTuple + (y,)
        newR.append(tempTuple)
    return newR
                    
#Creates variables that point to terminals          
def toTerminal(alp):
    l = []
    for x in A:
        tempTuple = ()
        r = alp.pop()
        tempTuple = (x,r)#(x -> r)
        l.append(tempTuple)
    newR = []
    for x in R:
        tempTuple = ()
        for y in x:
            s = "" #build each element
            for c in y:
                if(c in A):
                    for z in l:
                        if(c == z[0]):
                            s+=z[1]
                else:
                    s+=c
            tempTuple = tempTuple + (s,)
        newR.append(tempTuple)
    for n in l:
        tTuple = (n[1],n[0])
        newR.append(tTuple)
    return newR
            
        
            
A = []
V = []
S = []
R = []
readFile("test.txt")
print (A)
print (V)
print (S)
print ("List of Rules with eps...\n")
print (R)
print ("List of Rules without eps...\n")
removeEps()
print (R)
R = eliminateUnitP()
print ("The new rule set after removing unit productions\n")
print (R)
R = uselessVars()
print ("The new rule set after removing useless productions\n")
print(R)
#print(V)
V = updateVars()
#print(V)
#print(V)
#Find available variable letters
alp = list(set(string.ascii_uppercase) - set(V))
#alp.remove(S[0])
#print (alp)
#reduceVars(alp)
print ("The new rule set after creating terminal variables\n")
R = toTerminal(alp)
print(R)
V = updateVars()
#print(alp)
print ("The new rule set after reducing variables\n")
R = reduceVars(alp)
print(R)
V = updateVars()
getDerivation("test.txt", 25, 10)




