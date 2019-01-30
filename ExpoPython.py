# Code written by: Anurag Madan, Angela Moncy, Jennifer Burns
# For : Orthofix
# The following is a Python script written for Orthofix by UTDesign team 543 Team 'TAPP' during the Fall 2017 and Spring 2018 Senior Design courses. 
# This script interfaces with both Arduino and MATLAB to control the entire robot. The test case is converted to numeric coordinates, and these coordinates
# are then sent to Arduino, which moves the stylus accordingly. This script also handles Optical Character Recognition, Image comparison, and file handling.
# Special commands, including screenshots, OCR, Image Comparison, are all performed in this script. The comments in the code provide a detailed explanation
# of what this script does. 
# PLEASE NOTE: There are a lot of places where hard-coded file paths exist. These will need to be changed according to the computer this script is run on. 


import time
import serial										# This is used to connect to the Arduino COM port. 	
import array
import datetime
from PIL import Image
import pytesseract									# This is used to perform Optical Character Recognition.
import Image
import matlab.engine									# This is used to connect to MATLAB to run an image comparison script
from desktopmagic.screengrab_win32 import (getDisplaysAsImages)				# This is used to take screenshots

w= 1680
h= 1050

#THIS IS THE USER INPUT REQUIRED TO RUN A TEST CASE

# This is where we take in basic user input. This is the minimum input required to run a given test on a given device, and will be required at the start of
each test case. The test case can be run repeatedly without having to fill this information out again. 
com = raw_input("Enter Arduino COM port.")						# This requires the user to enter the COM port which the Arduino is
											# connected to. 
loc = raw_input("Enter file location for test case: ")					# This requires the user to enter the name of the test file. Only the
											# name is required, as the rest of the path is currently hard coded.
legendloc = raw_input("Enter file location for legend: ")				# This requires the user to enter the name of the legend file. Only 
											# the name is required, as the rest of the path is currently hard coded.
numberOfTests = raw_input("Enter the number of times this test case needs to run: ")	# This requires the user to enter the number of times the test needs
											# to run
deviceType = raw_input("Is the Device an iPhone6 or an iPad? ")				# This requires the user to enter the type of device.
eng=matlab.engine.start_matlab()							# This connects to MATLAB to run an image comparison script.



#Here, we define any helper functions we needed


#This function gets the area of just the screen
def get_area():
	if deviceType == 'iPhone6':							#crops the area of the serial number.
	        area=(640,525,890,570)
		cropped_img = img.crop(area)
	else:
        	area=(447,300,677,350)
		cropped_img = img.crop(area)


#This function sends the end effector to coordinates (0,0)
def send_to_zeros():
	ser.write('x')						# sends coordinates (0,0). This process is repeated for all special
								# commands.
	ser.write('000')
	ser.write('!')
	ser.write('y')
	ser.write('000')
	ser.write('!')
        ser.write('*')						# When Arduino receives '*', it executes all coordinates upto that point
								# This process is repeated for all special commands. 


#This function takes a screenshot from the camera

def screenshot():
	
	q=ser.readline()
	print q		
	print "Screenshot being taken..."
	date_string1 = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	for displayNumber, im in enumerate(getDisplaysAsImages(), 1):
		im.save('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string1+'_%d.tiff' % (displayNumber,), format='tiff')
											# takes screenshot of both desktop screens. 

#This function solves any errors we found for the serial number. more cases may be added as needed. 

def errors(filename):
	file = open(filename, "r")
	for line in file:
		print line
		for i in line:					# The following are issues in OCR we encountered. Because the serial number
								# is hexadecimal, we could eliminate a lot of misreadings. There may be more
								# mistakes, but in our testing, we haven't found them. 
			if i == 'O':
                						# 'O' => '0'
	       			snRead += str('0')
            		elif i == ']':
                						# ignore
                		break
            		elif i == '\n':
                						# ignore
                		break
	            	elif i == 'I':
                						# 'I' => '1'
        	        	snRead += str('1')
                	elif i == 'S':
                						# 'S' => '5'
                		snRead += str('5')
                        elif i == 'M':
                						# 'M' => '14'
                		snRead += str('14')
                        elif i == 'l':
                						# 'l' => '1'
                		snRead += str('1')
	                elif i == "'":
                						# ignore
        	        	break
            		else:
	             		snRead += str(i)

			file.close()
	return snRead



#Here we define any functions for setting up the test cases. 


#This function reads the test case

def read_test_case(loc):
	store = ["" for x in range(40)]							# This array stores all the commands in a test case as elements. 
											# Used for a lot of reasons. The size will need to be modified to a 
											# higher number when required. 
	sscount=0									# This counts the number of times image comparison command is encountered
											# in a test case. 
	with open('C:\Users\utd\Desktop\Expo\\'+loc) as myfile:				# opens the test case for read. The hard coded path will need to be 
											# changed. 
		line=myfile.readline().replace('\n','')
		cnt=1
		while line and line[0]!="'":
			store[cnt-1]=line						# stores all test case commands in 'store' array. 
			line=myfile.readline().replace('\n','')
			cnt=cnt+1
	return store, cnt


#This function gets the serial number from the test case

def get_serial_number(loc):
	myfile=open('C:\Users\utd\Desktop\Expo\\'+loc)					# opens the test case to locate the required serial number. The hard
											# coded path will need to be changed. 
	var=myfile.read().replace('\n','')
	j=var.find("'")									# the serial number is placed in between "'". Locates the first '. 
	for i in range(j+1,j+11):
	    serialNo=serialNo+var[i]							# Stores the 10 character long serial number in variable 'serialNo'.
	return serialNo



#This function reads the legend file

def read_legend(legendloc):
	legfile=open('C:\Users\utd\Desktop\Expo\\'+legendloc)				# Opens the required legend file. The hard coded path will need to be
											# changed. 
	leg=legfile.read()								# Stores the legend in 'leg' array. 
	return leg


#This function gets the x coordinates for all test case commands.

def get_xcoord(store, leg, count):
	x=[]
	X=[]
	for i in range(0,count):
		if store[i] in leg and store[i].find('Log')==-1 and store[i].find('printToscreen')==-1:		# checks whether the stylus needs to move
			x=leg[leg.find(store[i])+len(store[i])+1:leg.find(store[i])+len(store[i])+4]		# Stores the x coordinates taken from the 
														# legend into a variable 'x'
			X.insert(0,x)										# Collects all 'x' coordinates. 
		else:
			x='-01'											# stores a negative coordinate as the x coordinate
														# if the stylus does not need to move.
			X.insert(0,x)
	X.reverse()
	return X



#This function gets the y coordinates for all test case commands.

def get_ycoord(store, leg, count):
	y=[]
	Y=[]
	for i in range(0,count):
		if store[i] in leg and store[i].find('Log')==-1 and store[i].find('printToscreen')==-1:
			y=leg[leg.find(store[i])+len(store[i])+5:leg.find(store[i])+len(store[i])+8]
			Y.insert(0,y)
		else:
			y='-01'
			Y.insert(0,y)
	Y.reverse()
	return Y



#This function gets any special commands that need to be performed.
#More cases may be added as needed

def get_special_commands(store, count)
	j=1
	
	command=array.array('i',(0 for i in range(0,11)))				# This array stores the locations of all special commands. 

    	for i in range(0,count):
		if store[i]=='*ocr*' or store[i].find('*ImageComp*')!=-1 or store[i].find('*ss*')!=-1 or store[i]=='*sn*' or store[i].find('printToScreen')!=-1 or store[i].find('Log')!=-1:
			command[j]=i							# This puts a pointer on all special commands in a test case. These 
											# pointers are used as start and end points in sending the coordinates
											# to Arduino. To add more functionality, just extend the if case to include
											# new functions. 
			j=j+1		
	return command, j








#Here we define functions for various tasks we needed to do. 


#this function performs optical character recognition

def optical_character_recognition():
	
	o=ser.readline()
	print o
        date_string1 = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        for displayNumber, im in enumerate(getDisplaysAsImages(), 1):
	im.save('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string1+'_%d.tiff' % (displayNumber,), format='tiff')
											# saves a screenshot of the 2 desktop screens. 
	upperx = input("Enter the top left x coordinate: ")		# gets the upper left x,y and bottom right x,y coordinates for 
											# getting the region for OCR. 
        uppery = input("Enter the top left y coordinate: ")
        lowerx = input("Enter the bottom right x coordinate: ")
        lowery = input("Enter the bottom right y coordinate: ")
        img = Image.open('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string1+"_2.tiff")

	area=(upperx,uppery,lowerx,lowery)
        cropped_img = img.crop(area)					# crops the area for OCR. 
        date_string2 = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	cropped_img.save('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string2+"_3.tiff")

	text=pytesseract.image_to_string(Image.open('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string2+"_3.tiff")).encode('ascii','ignore')
											# calls a function to perform OCR on the given cropped image. 
	date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	filename='C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string+'_4.txt'
	file=open(filename,'w')
        file.write(text)						# writes the performed OCR in a text file. 
	file.close()

	print 'txtFile = ', filename
        Read = ''
        file = open(filename, "r")
        for line in file:
        	print 'OCR Read = ',line				# prints what OCR read. 
        print "OCR done"		


#This function ensures the serial number entered is correct

def serial_number_check():
	r=ser.readline()						# Arduino sends back 'moved' after it is done. readline() reads that. 
	print r
	print "Optical Character Recognition in progress..."
	date_string1 = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")		# gets the current date and time for naming. 
	for displayNumber, im in enumerate(getDisplaysAsImages(), 1):
	im.save('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string1+'_%d.tiff' % (displayNumber,), format='tiff')
											# saves a screenshot of both desktop screens. 
	img = Image.open('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string1+"_2.tiff")
											# opens image of second screen, which is recording the
											# app. 
        
	cropped_img=get_area()
	

	date_string2 = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	cropped_img.save('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string2+"_3.tiff")
											# stores the cropped image. The hard coded path will
											# need to be changed. 
	text=pytesseract.image_to_string(Image.open('C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string2+"_3.tiff")).encode('ascii','ignore')
											# calls a function to perform OCR on the given 
											# cropped image. 
	date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	filename='C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\'+date_string+'_4.txt'
	file=open(filename,'w')
	file.write(text)								# stores the text in a file. 
	file.close()


	    # Open and read the file
	print 'txtFile = ', filename
	snRead = errors(filename)
			

	print 'snRead = ', snRead
	print 'snStr  = ', serialNo

    #
    # Compare serial number read with serial number string, they should be identical!
	if snRead == serialNo:				# validates that the serial number typed is correct. 
    		print 'Serial Number entered is correct.'
	else:
        	print 'Serial Number entered is incorrect. '
		print 'End'
		time.sleep(3)
		commentfile.write('OCR not matching. Test failed.')	
		quit()



#This function performs image comparison 

def image_comparison(command, k):
	screenshot()

       	time.sleep(5)
        img = Image.open("C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\"+date_string1+"_2.tiff")
										# opens the second screen, which is recording the app. 
	cropped_img=get_area()
        date_string2 = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        cropped_img.save("C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\"+date_string2+"_3.tiff")
										# saves the cropped image. 
		
	actss[sscount]="C:\\Users\\utd\\Desktop\\Expo\\Screenshots\\"+date_string2+"_3.tiff" 	# stores the location of the image taken.
										# The hard coded location will need to be 
										# changed.
	refss[sscount]=store[command[k]].replace('*ImageComp* ','')	# gets the location of the reference image. The way the test file
										# is created, this command gets the location correctly. 
	sscount=sscount+1						# counts the number of times image comparison is called. 

	return actss, refss, sscount




for rerun in range(0,int(numberOfTests)):						# Runs the loop for the number of times a test case needs to run


	store, cnt=read_test_case(loc)

	

	refss = ["" for x in range(40)]							# Stores the locations of the reference images for image 
											# comparisons in a test case. 
	actss = ["" for x in range(40)]							# Stores the locations of the actual screenshots for image 
											# comparisons in a test case. 
	
	date_stringcomment = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	
	commentfile=open('C:\Users\utd\Desktop\Expo\Log files\\autotester_'+date_stringcomment + '.txt','w')	# Location of the log files for a test case. 
														# This will need to be modified for different
														# computers. 
	serialNo=get_serial_number(loc)

	#print serialNo
	leg=read_legend(legendloc);

	#print leg
	count=cnt-1									# the number of lines in the test case. 

	
	
	X=get_xcoord(store, leg, count)
	Y=get_ycoord(store, leg, count)
	
	command, j=get_special_command(store, count)						
	
	ser=serial.Serial(com,9600)							# opens a serial communication to Arduino.
	time.sleep(3)

	for k in range(1,j):								# j is the number of special commands encountered in a test case.
		for i in range(command[k-1],command[k]):				# command is the location of those special commands. we run the loop
											# from one special command to the next. 
			if X[i]!='-01':							# removing negative coordinates. 
				ser.write ('x')						# sending 'x' or 'y' tells Arduino what coordinate it is about to 
											# receive. 
				ser.write (X[i])					# sends the actual coordinate.
				ser.write('!')						# sending '!' marks the end of the coordinate. 
		for i in range(command[k-1],command[k]):
			if Y[i]!='-01':
				ser.write('y')
				ser.write(Y[i])
				ser.write('!')	
	
		if store[command[k]]=='*sn*':						# if the special command is a serial number OCR.
	        	send_to_zeros()
        		serial_number_checck(serialno)
			time.sleep(5)

		if store[command[k]].find('*ss*')!=-1:			
			send_to_zeros()
			screenshot()
	        	time.sleep(5)


		if store[command[k]].find('*ImageComp*')!=-1:				# if special command encountered is image comparison.
        		send_to_zeros()
			actss, refss, sscount = image_comparison(command,k)

        	if store[command[k]]=='*ocr*':						# if the special command encountered is OCR on any given region.

			send_to_zeros()
        		optical_character_recognition()

		if store[command[k]].find('printToScreen')!=-1:				# if the special command encountered is print to screen. 
			ser.write('*')
			q=ser.readline()
			print store[command[k]]						# prints what the line in the test case says. 
			raw_input('press enter to continue...')				# waits for 'enter'

		if store[command[k]].find('Log')!=-1:					# if the special command encountered is to log something. 
			commentfile.write(store[command[k]])				# writes the line in the test case in a separate log file. 
			commentfile.write('\n')
		

	for i in range(command[k]+1,count):						# This loop finishes all the remaining actions in the test case
											# after all the special commands have been completed. So the actions
											# from the last special command to the end of the test case. 
		if X[i]!='-01':
			ser.write ('x')
			ser.write(X[i])
			ser.write('!')
	for i in range(command[k]+1,count):
		if Y[i]!='-01':
			ser.write('y')
			ser.write(Y[i])
			ser.write('!')

	commentfile.close()
	ser.write('+')									# This tells Arduino to reset. 
    	z=ser.readline()
    	print z
        print "Test case complete"
	time.sleep(3)
	ser.close()
	print "image comp being done if any..."
	for i in range(0,sscount):							# This does image comparisons for one round of the test case. 
		dummy=open('C:\Users\utd\Desktop\Expo\MATLAB image comp\dummyss.txt','w')
											# writes the locations of the actual and reference images in a 
											# dummy text file. The hard coded locations will need to be 
											# changed. 
		dummy.write(actss[i])
	    	dummy.write('\n')
		dummy.write(refss[i])
		dummy.write('\n')
		dummy.write(date_stringcomment)
		print "written"
		dummy.close()
		eng.ImageComp_V4(nargout=0)						# calls the image comparison MATLAB script. 
	    	time.sleep(10)
	

	






