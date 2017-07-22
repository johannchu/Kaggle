#-*- coding: utf-8 -*-
import sys, codecs, math

class SplitNode:
	'The object representing each split node'
	def __init__(self, data, usedSet, attributeToSplit, obtainedWithAttributeIndex, nodeName):
		# if we have a node obtained by splitting its parent with attribute on index i,
		# the we save "i" in 'obtainedWithAttributeIndex'. The node would then have
		# data containing one identical information across all entries; that piece of
		# information would then be the 'nodeName'.
		self.data = data
		self.usedSet = usedSet
		self.attributeToSplit = attributeToSplit
		self.obtainedWithAttributeIndex = obtainedWithAttributeIndex
		self.nodeName = nodeName

def GetSplitWithAttribute(listOfData, attributeIndex):
	someDict = {}
	for item in listOfData:
		components = item.strip().split('\t')
		if components[attributeIndex] not in someDict:
			temp = []
			temp.append(item.strip())
			someDict[components[attributeIndex]] = temp
		else: someDict[components[attributeIndex]].append(item.strip())
	return someDict

def GetClassDataNumbersForEachKey(someDict, classIndex):
	# storage will have the key as same as someDict, with another dictionary as value.
	# The value dictionary will have the class as key, 
	# while the occurrence of data associated with that class as corresponding value
	storage = {}
	for uniqueKey in someDict.keys():
		classToNumberOfData = GetClassDataNumbersFromList(someDict[uniqueKey], classIndex)
		storage[uniqueKey] = classToNumberOfData
	return storage

def GetClassDataNumbersFromList(dataList, classIndex):
	# print "Type of dataList: " + str(type(dataList))
	classToNumberOfData = {}
	for item in dataList:
		components = item.split('\t')
		if components[classIndex] not in classToNumberOfData:
			classToNumberOfData[components[classIndex]] = 1
		else: classToNumberOfData[components[classIndex]] += 1
	return classToNumberOfData

# dataDict could be something like: {[CERTIFIED:3],[DENIED:5],[WITHDRAWN:2],...}
def GetImpurityOfNode(dataDict, totalNumberOfData):
	sumOfSquare = 0.0
	for uniqueKey in dataDict.keys():
		sumOfSquare += math.pow(dataDict[uniqueKey] * 1.0 / totalNumberOfData, 2)
	return 1-sumOfSquare

fileName = sys.argv[1]
storage = []
inputFile = codecs.open(fileName,'r','utf-8')
print "Start reading file..."
for line in inputFile:
	storage.append(line.strip())
inputFile.close()

print "Number of data: " + str(len(storage))

rootClassDistribution = GetClassDataNumbersFromList(storage,1)
rootImpurity = GetImpurityOfNode(rootClassDistribution, len(storage))

# 假設我們今天要試2到6當attribute
for index in range(2,6):
	print "Calculating impurity for child nodes under attribute " + str(index)
	identifierToData = GetSplitWithAttribute(storage,index)
	classNumberUnderIdentifier = GetClassDataNumbersForEachKey(identifierToData, 1)
	totalImpurityOfChildNodes = 0
	for uniqueKey in classNumberUnderIdentifier.keys():
		classToNumber = classNumberUnderIdentifier[uniqueKey]
		totalNumberOfData = 0
		for uniqueClass in classToNumber.keys():
			totalNumberOfData += classToNumber[uniqueClass]
		impurity = GetImpurityOfNode(classToNumber, totalNumberOfData)
		totalImpurityOfChildNodes += impurity * totalNumberOfData / len(storage)
	gain = rootImpurity - totalImpurityOfChildNodes
	print "Gain for attribute index " + str(index) + ": " + str(gain)