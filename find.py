#!/usr/bin/python

import sys, getopt
import os
import os.path
import shutil
import re

projectPath = ''
fileName = ''

copyDrawable = 0
removeDrawable = 0
updateResources = 0
replaceWithDummyDrawable = 0

newResourceCompactPath = ''

resMap = {'ldpi':'drawable-ldpi','mdpi':'drawable-mdpi','hdpi':'drawable-hdpi','xhdpi':'drawable-xhdpi','xxhdpi':'drawable-xxhdpi','xxxhdpi':'drawable-xxxhdpi'}

def main(argv):
	
	global projectPath
	global fileName
	global copyDrawable
	global replaceWithDummyDrawable
	global removeDrawable
	global newResourceCompactPath
	global updateResources

	try:
	
		opts, args =getopt.getopt(argv,"hp:f:u:crd",["projectPath=","fileName=","update="])
	except getopt.GetoptError:
		print 'run script properly'
		sys.exit(2)
	
	for opt,arg in opts:
		if opt  == '-h':
			print 'Following options are available: '
			print '-f,--fileName 	To print the all the directories of file: python find.py -p <PROJECT_PATH> -f <FILE_NAME>'
			print '-c   		To prepare a copy of the file according to resource folder for eg. hdpi,xhdpi,etc: python find.py -p <PROJECT_PATH> -f <FILE_NAME> -c'
			print '-u 		To update existing resource or copy new one: find.py -p <PROJECT_PATH> -f <FILE_NAME> -u <NEW_RESOURCE_PATH> '
			print '-r 		To remove existing resource : find.py -p <PROJECT_PATH> -f <FILE_NAME> -r'
			print '-d 		If you want to make sure that a resource is being loaded from correct dpi then this option will replace those resource with dummy image which shows what dpi resource is being used : find.py -p <PROJECT_PATH> -f <FILE_NAME> -d'
			sys.exit()
		elif opt in ("-p","--projectPath"):
			projectPath = arg
		elif opt in ("-f","--fileName"):
			fileName = arg
		elif opt in ('-u',"--update"):
			newResourceCompactPath = arg
			updateResources = 1
		elif opt in '-c':
			copyDrawable = 1
		elif opt in '-r':
			removeDrawable = 1
		elif opt in '-d':
			replaceWithDummyDrawable = 1

def printDrawableFolders():

	global projectPath
	global fileName

	resPath = projectPath+'src/main/res/'
	print 'path '+resPath
	print fileName+' present as following drawable folders:'
	

	f=os.getcwd()+'/copied_drawables'
	for root, dirs, files in os.walk(resPath):
		for eachDir in dirs:
			if os.path.isfile(resPath+eachDir+"/"+fileName):
				print eachDir
				if copyDrawable == 1:
					copyDrawableFnc(f,eachDir)
				if removeDrawable == 1:
					os.remove(resPath+eachDir+"/"+fileName)
				if replaceWithDummyDrawable == 1:
					replaceWithDummy(eachDir)

		break

def replaceWithDummy(eachDir):
	dummyDrawables = os.getcwd()+'/sample_images'
	dummyFile = eachDir[9:]+'.png'

	shutil.copy(dummyDrawables+'/'+dummyFile,projectPath+'src/main/res/'+eachDir+'/'+fileName)

def ensureDir(f):
	if not os.path.exists(f):
		os.makedirs(f)

def copyDrawableFnc(dirPath,eachDir):
	global fileName

	ensureDir(dirPath)

	filePath = dirPath+ '/'+eachDir
	if os.path.exists(filePath):
		shutil.rmtree(filePath)
	os.makedirs(filePath)
	shutil.copy(projectPath+'src/main/res/'+eachDir+'/'+fileName,filePath)

def updateDrawablesCompact():
	
	global newResourceCompactPath
	
	for root, dirs, files in os.walk(newResourceCompactPath):
		for eachFile in files:
			m = re.search('(.+?)@(.+?).png',eachFile)
			if m:
				fileName = m.group(1)
				dpi = m.group(2)
				dest = projectPath+'src/main/res/'+resMap[dpi]
				
				ensureDir(dest)
				shutil.copy(newResourceCompactPath+'/'+eachFile,dest)
				print 'File: '+fileName+'    DPI: '+dpi+'   dest '+dest+'    src: '+newResourceCompactPath+eachFile

def newDrawables():
	
	global newResourceCompactPath


	for root,dirs,files in os.walk(newResourceCompactPath):
		for eachDirs in dirs:
			print eachDirs+" directory  "+root 

				
	
if __name__ == "__main__":
	main(sys.argv[1:])
	printDrawableFolders()
	newDrawables()
	if updateResources == 1:
		updateDrawablesCompact()

