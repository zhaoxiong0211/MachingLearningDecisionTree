#!usr/bin/python
#Filename:test.py

import string
# import plotting
import csv

def getSize(filename,tree,traininfo):
	for ele in traininfo:
		ele = ele.__str__()
	data, attrs = resetwinner(filename)
	allSize = len(data)
	return allSize

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
            
        return [title, realFile, rowLength]

def test(filename,tree,traininfo):
	for ele in traininfo:
		ele = ele.__str__()
	data, attrs = resetwinner(filename)
	handleques(data, traininfo)
#print data
	result = []
	count = 0
	allSize = getSize(filename,tree,traininfo)
	print allSize
	if 1:
		for line in data:
			winner = predict(line, tree, attrs)
			result.append(winner)
	csv = csvRead(filename)
	compareresult(filename, result, csv[1], csv[2], csv[0])

	# print "total = ",total,"\ncorrect = ", correct,"\n the accuray = ", float(correct)/float(total)
	# return acc

def compareresult(filename, result, fileraw, length, attr):
	resultfile = csv.writer(open("resultNew.csv", 'w'))
	# datafile = open(filename)
	# totalcount = 0
	# rightcount = 0
	resultfile.writerow(attr)
	for i in range(len(result)):
		fileraw[i][length-1] = str(result[i])
		resultfile.writerow(fileraw[i])
		# if totalcount == 0:
		# 	totalcount += 1
		# 	line.replace("\n","")
		# 	token = line.split(",")
		# 	result.writerow(token)
		# 	continue
		# line.replace("\n","")
		# token = line.split(",")
		# #print token
		# answer = token[len(token) - 1][0]
		# # if answer == '?':
		# # 	continue
		# # else:
		# # print " right answer is ",answer,"  we got",result[totalcount - 1]
		# # answer = string.atoi(answer)
		# token[len(token) - 1][0] = str(result[totalcount - 1])
		# result.writerow(token)
		# # if answer == result[totalcount - 1]:
		# # 	rightcount += 1
		# totalcount += 1
	# return totalcount - 1, rightcount

def compareresult1(filename, result, allSize):
	datafile = open(filename)
	totalcount = 0
	rightcount = 0
	temCount = -1
	acctem = []
	#for i in range(allSize):
		#print i
	for line in datafile:
		temCount = temCount + 1
		print temCount
		#if temCount <= i:
		if totalcount == 0:
			totalcount += 1
			continue
		line.replace("\n","")
		token = line.split(",")
		#print token
		answer = token[len(token) - 1][0]
		if answer == '?':
			continue
		else:
			# print " right answer is ",answer,"  we got",result[totalcount - 1]
			answer = string.atoi(answer)
		if answer == result[totalcount - 1]:
			rightcount += 1
		totalcount += 1
		acctem.append(str(float(rightcount) / (totalcount-1	)))
		
	return acctem

def predict(line, tree, attrs):
#	print line
	attribute = tree.keys()
	attribute = attribute[0]
	i = getattrindex(attrs, attribute)
	value = line[i] 
	value = string.atof(value)
	# print attribute," = ",value
	directory = tree[attribute].keys()
	cond = directory[0]
	if cond[0] == '<':
		condition = cond[2:]	 #to remove the '<='
		#	print condition
		condition = string.atof(condition)
		if value <= condition:
			if tree[attribute][cond] == 1 or tree[attribute][cond] == 0:
				# print" result = ",
				# print tree[attribute][cond]
				return tree[attribute][cond]
			else:
				return predict(line, tree[attribute][cond], attrs)
		else:
			cond = directory[1]
			if tree[attribute][cond] == 1 or tree[attribute][cond] == 0:
				# print "result = ",
				# print tree[attribute][cond]
				return tree[attribute][cond]
			else:
				return predict(line, tree[attribute][cond], attrs)
	else:
		condition = cond[1:]	 #to remove the '>'
		#	print condition
		condition = string.atof(condition)
		if value > condition:
			if tree[attribute][cond] == 1 or tree[attribute][cond] == 0:
				# print "result = ",
				# print tree[attribute][cond]
				return tree[attribute][cond]
			else:
				return predict(line, tree[attribute][cond], attrs)
		else:
			cond = directory[1]
			if tree[attribute][cond] == 1 or tree[attribute][cond] == 0:
				# print "result = ",
				# print tree[attribute][cond]
				return tree[attribute][cond]
			else:
				return predict(line, tree[attribute][cond], attrs)
		
	

def getattrindex(attr, at):
	for index in range(len(attr)):
#		print attr[index]
		if attr[index] == at or attr[index] == " "+at or " " + attr[index] == at:
			return index
	return -1

def handleques(data,traininfo):
	for line in data:
		for i in range(len(line) - 1):
			if line[i] == "?":
				line[i] = traininfo[i]
	return data

def resetwinner(filename):
	testfile = open(filename)
	count = 0
	for line in testfile:
#		print line
#		print count
		count += 1
	testfile.close()
	testfile = open(filename)
	data = []
#	data = [0 for i in range(count)]
	count = 0
	for line in testfile:
		line = line.replace("\n","")  #for windows, line = line.replace('\r\n',"")
		token = line.split(",")
		# token[len(token) - 1] = "?"
		data.append(token)
#		data[count] = token
		count += 1
	attr =  data.pop(0)
#	print data
	testfile.close()
#	print attr
	return data, attr

#info = ['0']*14
#tree = {'numinjured':{'>1.0':0.0,'<=1.0':1.0}}
#test("btrain2.csv",tree,info)
