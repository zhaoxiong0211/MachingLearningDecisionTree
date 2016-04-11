import csv
import operator
import struct, string, math, copy
import test, newprune
import sys
# import plotting
import output

def csvRead(fileName):
    # with open(fileName, 'eb') as csvfile:
    rowNumber = 0
    realFile0 = []
    with open(fileName, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            realFile0.append(row)
            rowNumber = rowNumber + 1
            rowLength = len(row)

        realFile = [[0 for n in range(rowLength)] for m in range(rowNumber)]

        count = -1
        for item in realFile0:
            count = count + 1
            for col in range(rowLength):
                realFile[count][col] = item[col]
        title = realFile.pop(0)
            
        return [title, realFile]

def decisionTree(fileName, Train, Validate, Predict, testFile, NeedPrune):
    csv = csvRead(fileName)
    columnCsv = []
    modeList = []
    traininfo = []
    # print len(csv[1][0])
    for num in range(len(csv[1][0])):
        # columnCsv.append(columnCreate(csv[1], num))
        columnCsv = columnCreate(csv[1], num)
        categoryOrnumeric(columnCsv, csv, num, modeList, traininfo)
    myTree = createTree(csv[1], csv[0],modeList)
    # f = open("tree.txt", "w")
    # drawTree(myTree,0,f)
    if NeedPrune == False:
        if Validate:
            test.test(testFile,myTree, traininfo)
        if Predict:
            output.test(testFile,myTree,traininfo)
    # print myTree
    # output.test('btest.csv',myTree,traininfo)
    return myTree,csv[1],traininfo

        
def categoryOrnumeric(currentColumn,csv,num,modeList,traininfo):
    temDict = {}
    count = -1
    blankPos = []
    columnSum = 0
    # print currentColumn
    for item in currentColumn:
        count = count + 1
        if item != '?':
            if item not in temDict:
                temDict[item] = 1
                columnSum = columnSum + float(item)
                csv[1][count][num] = float(item)
            else:
                temDict[item] = temDict[item] + 1
                csv[1][count][num] = float(item)
        else:
            blankPos.append(count)

    if len(temDict) > 100:  #500
        mode = 1 # numeric
    else:
        mode = 2 # categorical

    if mode == 1:
        noneBlankLength = (count+1) - len(blankPos)
        replace = columnSum / noneBlankLength
        for pos in blankPos:
            csv[1][pos][num] = replace
    else:
        maxKey = maxValuefromDict(temDict)
        replace = float(maxKey)
        for pos in blankPos:
            csv[1][pos][num] = replace
    modeList.append(mode)
    traininfo.append(replace)
        
def columnCreate(dataset, num):
    col = []
    for item in dataset:
        col.append(item[num])
    return col

def maxValuefromDict(rawDict):
    counter = 0
    for word in rawDict.keys():
        if rawDict[word] > counter:
            counter = rawDict[word]
            result = word
    return result

def calcShannonEnt(dataSet):
    #calculate the shannon value
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:  #create the dictionary for all of the data
            currentLabel = featVec[-1]
            if currentLabel not in labelCounts.keys():
                    labelCounts[currentLabel] = 0
            labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
            prob = float(labelCounts[key])/numEntries
            shannonEnt -= prob*math.log(prob,2) #get the log value
    return shannonEnt


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    retDataSet2 = []
    for featVec in dataSet:
        if featVec[axis] <= value:      #abstract the fature
            reducedFeatVec = featVec[:]
            #reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
        else:
            reducedFeatVec = featVec[:]
            #reducedFeatVec.extend(featVec[axis+1:])
            retDataSet2.append(reducedFeatVec)    
    return [retDataSet,retDataSet2]
        


def chooseBestFeatureToSplit(dataSet,modeList):
        numFeatures = len(dataSet[0])-1
        baseEntropy = calcShannonEnt(dataSet)
#print baseEntropy
        bestInfoGain = 0.0; bestFeature = -1; threshold = 0.0
        for i in range(numFeatures):
                if modeList[i] == 2:
                        featList = [example[i] for example in dataSet]
                        uniqueVals = set(featList)
                        InfoGain = 0.0
                        newEntropy = 0.0
                        uniqueVals = sorted(list(uniqueVals))
#print modeList                
                        '''if modeList[i] == 1:
                                delta = float(uniqueVals[-1] - uniqueVals[0])
                                # print delta
                                uniqueVals = [(uniqueVals[0] + delta/50*(j+1)) for j in range(48)]
                        valuer = 0.0'''
                        for value in uniqueVals:
                                newEntropy = 0.0
                                subDataSet = splitDataSet(dataSet, i , value)
                                for two in subDataSet:
                                        prob = len(two)/float(len(dataSet))
                                        newEntropy +=prob * calcShannonEnt(two)
                                infoGainTest = baseEntropy - newEntropy
                                if(infoGainTest > InfoGain):
                                        InfoGain = infoGainTest
                                        valuer = value

                else:
                        InfoGain = 0.0
                        newEntropy = 0.0
                        sorteddataSet = sorted(dataSet, key = lambda data : data[i])
                        featList = [example[i] for example in sorteddataSet]
                        #print featList
                        uniqueValue = list(set(featList))
                        uniqueValue.append(10000)
                        index = []
                        counting = 0
                        for d in range(len(featList)):
                                if featList[d] == uniqueValue[counting]:
                                        index.append(d)
                                        counting += 1
                        for valueindex in range(len(index)-2):
                                value = featList[index[valueindex+1]]
                                newEntropy = 0.0
                                subDataSet = [sorteddataSet[:index[valueindex+1]],sorteddataSet[index[valueindex+1]:]]
                                for two in subDataSet:
                                        prob = len(two)/float(len(dataSet))
                                        #print prob
                                        newEntropy +=prob * calcShannonEnt(two)
                                infoGainTest = baseEntropy - newEntropy
                                if(infoGainTest > InfoGain):
                                        InfoGain = infoGainTest
                                        valuer = value

                if(InfoGain > bestInfoGain):
                        bestInfoGain = InfoGain
                        bestFeature = i
                        threshold = valuer

                                
#        print bestInfoGain
#        print bestFeature
#        print threshold
        return [bestFeature, threshold, bestInfoGain]

def createTree(dataSet, labels,modeList):
        classList = [example[-1] for example in dataSet]
        fileHandle = open ( 'Output.txt', 'a' )
        if classList.count(classList[0]) == len(classList):    #
                return classList[0]
        if len(dataSet[0]) == 1:
                return majorityCnt(classList)       #
        features = chooseBestFeatureToSplit(dataSet,modeList)
        bestFeat = features[0]
        bestinfogain = features[2]
        bestFeatLabel = labels[bestFeat]
        if bestFeat == -1:
            return majorityCnt(classList)
        else:
            threshold = features[1]
            myTree = {bestFeatLabel:{}}
            #del(labels[bestFeat])
            #del(modeList[bestFeat])
            value = '<=' + str(threshold)
            value2 = '>' + str(threshold)
            subdataSet = splitDataSet(dataSet, bestFeat, threshold)

            fileHandle.write ( '\n' )
            fileHandle.write ( bestFeatLabel ) 
            fileHandle.close()

#            if bestinfogain >= 0.005:
#if 1:
            if len(dataSet) > 1: 
                subLabels = labels[:]
                submodeList = modeList[:]
                myTree[bestFeatLabel][value] = createTree(subdataSet[0], subLabels, submodeList)

                subLabels = labels[:]
                submodeList = modeList[:]
                myTree[bestFeatLabel][value2] = createTree(subdataSet[1], subLabels, submodeList)
            else:
                return majorityCnt(classList)
        return myTree

def drawTree(myTree, drawTreeCount,f):

    if myTree == 1.0 or myTree == 0.0:
        lines = '-'* drawTreeCount
        print lines, myTree
        leaf = lines + str(myTree)
        f.write(leaf)
        f.write('\n')
    else:
        attribute = myTree.keys()
        attribute = attribute[0]
        directory = myTree[attribute].keys()
        cond = directory[0]
        cond2 = directory[1]
        count_next = copy.deepcopy(drawTreeCount + 1)
        lines = '-'* drawTreeCount
        if myTree[attribute][cond] == 1 or myTree[attribute][cond] == 0:
            print lines, myTree[attribute][cond]
            leaf = lines + str(myTree[attribute][cond])
            f.write(leaf)
            f.write('\n')
        else:
            nodeInformation = attribute + ' ' + cond
            print lines, nodeInformation
            leaf = lines + nodeInformation
            f.write(leaf)
            f.write('\n')

            temTree = myTree[attribute][cond]
            drawTree(temTree, count_next, f)

            nodeInformation2 = attribute + ' ' + cond2
            print lines, nodeInformation2
            leaf = lines + nodeInformation2
            f.write(leaf)
            f.write('\n')

            temTree2 = myTree[attribute][cond2]
            drawTree(temTree2, count_next, f)

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0;
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)  #
    return sortedClassCount[0][0]

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: python *.py <-p for use pruning, -np for not using pruning>'
    else:
        if sys.argv[1] == '-p':
            NeedPrune = True
        elif sys.argv[1] == '-np':
            NeedPrune = False
        if sys.argv[4] == '-train':
            Train = True
            Validate = False
            Predict = False
        elif sys.argv[4] == '-validate':
            Train = False
            Validate = True
            Predict = False
        elif sys.argv[4] == '-predict':
            Train = False
            Validate = False
            Predict = True
        if sys.argv[1] != '-p' and sys.argv[1] != '-np':
            print 'Usage: python *.py <-p for use pruning, -np for not using pruning>'
        else:
            trainFile = sys.argv[2]
            testFile = sys.argv[3]
            Dtree, trainset, traininfo = decisionTree(trainFile, Train, Validate, Predict,testFile, NeedPrune)
            if NeedPrune:
                print "####################################################################################"
                optimaltree = newprune.Prune('btrain.csv', Dtree, Train, Validate, Predict,testFile, NeedPrune)
                # test.test('bvalidate.csv',optimaltree,traininfo)
                

