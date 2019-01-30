# Senior_capstone_project

This code is the property of Orthofix USA, and should not be copied or reproduced in any way without
prior written permission. The code is part of the Senior Capstone Project at University of Texas at 
Dallas, written for Orthofix USA. 

There are two parts to the code. The Python script which handles the test cases and controls the robot,
and the MATLAB script for image comparison. 


******************************************************************************************************
     	CREATING A TEST AND LEGEND FILE FOR ORTHOFIX
******************************************************************************************************



******************************************************************************************************
		LEGEND FILE
******************************************************************************************************
The legend file maps the buttons present on the StimOnTrack iOS app to an (x,y) cartesian coordinate,
and allows the user to write special commands such as Screenshots into the test case.
This file is unique for all devices. An iPhone legend will be different from an iPad legend. Each 
legend needs to be mapped out separately. There are two components to the legend file - the name of 
any button on the app, and it's corresponding (x,y) coordinate. The following is the syntax for 
different kinds of buttons: 

CASE 1: If the button is a single character (example mapping the QWERTY keypad), the syntax required is 

	"nameOfCharacter" xxx,yyy

	where x represents the 'x' coordinate, and y represents the 'y' coordinate. The double quotes
	are essential, as the code works by locating the string "nameOfCharacter" in the legend file. 
	There should also be a 'space' between the second quote and the first digit of the 'x'
	coordinate. The coordinates need to be triple digits. If the coordinate is less than 100 (Double
	digit), place zeros to make it triple digit.
	
	Example: 
	"a" 012,205

CASE 2: If the button is not a single character (example 'settings' on the app), the syntax required is
	
	nameOfString xxx,yyy    OR    "nameOfString" xxx,yyy
	
	The double quotes are not necessary here. There should be a 'space' between the final character
	of the name and the first digit of the 'x' coordinate, or the second quote and the first digit
	of the 'x' coordinate, depending on the syntax used. The coordinates need to be triple digits. 
	If the coordinate is less than 100 (Double digit), place zeros to make it triple digit.

	Example: 
	Settings 012,205
	"Calendar" 143,025

CASE 3: If the command to be executed is a 'screenshot' or 'optical character recognition', the syntax
	required is 

	*ss* 000,000     OR     *ocr* 000,000	  OR	*sn* 000,000	 OR	*ImageComp* 000,000

	This is the exact line that needs to be present in the legend to execute a screenshot or optical
	character recognition. The (0,0) coordinates allow the robot to move out of the way of the camera. 

	Example: 
	*ss* 000,000
	*ocr* 000,000
	*sn* 000,000
	*ImageComp* 000,000

CASE 4: If the command to be executed is a swipe motion or a double tap (typically used on the 'HOME' 
	button of an iPhone or iPad to close apps), the following commands can be used - 

	*swup* 002,002
	*swdn* 003,003
	*swlt* 004,004
	*swrt* 005,005
	*swout* 006,006
	*double* 007,007

	The first four are swipes in the up, down, left, and right directions respectively. After that
	is the swipe out command, used to close apps by swiping up to the end of the screen. The final
	is the double tap command. 

CASE 5: If the command is a reset command to move the robot back to the origin for recalibration, the 
	syntax is

	"reset" 000,000

The legend file only needs to be created once, and can be updated with buttons and commands as required. 
coordinates that are outside the workspace, such as (0,0) for reset or (2,2) for swipe up are special
coordinates which are used as markers by the Arduino code to understand the command that was sent. 
Simple if-else statements allow the program to determine the action that needs to be performed based
on the coordinates received.



******************************************************************************************************
	TEST FILE
******************************************************************************************************
The test file is used to convert test cases into a format readable by the python script. Using buttons
defined in the Legend file, test cases that are autonomous and non autonomous can be created. There are
several commands that can be placed in the test file for different actions. 

CASE 1: If the action is tapping any button on the iPhone/iPad, the syntax required is

	"nameOfCharacter" or nameOfString or "nameOfString"

	The way to write any button in the test file is to ensure it appears the same way in the
	Legend file. 

	Example: 
	"a" 012,201				This is in the legend file
	"a"					This is in the test file

	Settings 012,201			This is in the legend file
	Settings				This is in the test file

CASE 2: If the action is taking a Screenshot or performing Optical Character Recognition, the syntax
	required is
	
	*ss*	OR	*ocr*	OR	*sn*
	OR *ImageComp* REF_FILE_LOC

	This is the exact way a screenshot or OCR can be done.
 
	*ss* is used for screenshot. The code will take a screenshot of the entire screen, date and 
	time stamp it, and store it in a predefined location.

	*sn* is used for Optical Character Recognition of the serial number. This will read the 
	region of the serial number, and compare it to the serial number placed in the test case.
	(Look at CASE 6 for more information on this). The code will then print if the serial number
	entered is correct or not. In case it is INCORRECT, the code will exit. 

	*ocr* is used for Optical Character Recognition in any given region of the screen. After this
	command is encountered, the user is prompted to enter the (x,y) coordinates of the upper left
	corner, and then the (x,y) coordinates of the bottom right corner of the rectangle in which the 
	OCR needs to be performed. In case the region is not within the screen limit, an error is thrown.
	
	*ImageComp* works the same way as a screenshot (*ss*), but in addition to taking a screenshot, 
	it also compares it to a predetermined reference image. This is done at the end of the test case,
	and a difference image is produced via a MATLAB script. This difference image highlights the 
	places of difference as white specks on a black background (So, ideally you want a plain black
	background.) The MATLAB script is provided, and contains an in-depth explanation of the algorithm
	used. 

	Example:
	*ss*
	*ImageComp* C:\\Users\\UTD\\Desktop\\refImage1.tiff

CASE 3: If the action is a swipe or double tap or reset, the syntax required is

	*swup*
	*swdn*
	*swlt*
	*swrt*
	*swout*
	*double*
	"reset"

	The first four are swipes in the up, down, left, and right directions respectively. After that
	is the swipe out command, used to close apps by swiping up to the end of the screen. The next
	is the double tap command. The final is a reset command

CASE 4: If the action is printing a message to the screen for a user, the syntax required is

	printToScreen UserMessage

	The keyword printToScreen is required to display the message UserMessage on the screen. 

	Example:
	printToScreen This is a readme for creating legend and test files

	NOTE: The printToScreen command will print the line on the screen, and then will wait for 
	the return (Enter) key to be pressed before continuing.

CASE 5: If the action is logging a prewritten comment in a separate log file, the syntax required is

	Log PreWrittenMessage

	The keyword Log is required to store the message in a separate log file. Each test case 
	automatically creates a new log file in a location the user enters.

	Example:
	Log This is a readme for creating legend and test files

	NOTE: A log command will not do anything on the screen. It is not detected while the test
	is running. Once the test is complete or aborted, the log file can be checked to see how
	far the test ran. The logs are only written upto the point where the test ran successfully. 
	Anything after that is not written. If the test was COMPLETED successfully, the entire log
	is written.

CASE 6: If there is a Serial Number input in the test case, that Serial Number needs to be provided
	in the following format

	'SerialNumber'
	
	This can be placed anywhere in the file, though it is recommended to place it at the very beginning
	or end for clarity. The serial number needs to be enclosed in single quotes, and needs to be in 
	one line, and 10 characters long. This is also needed if there is an *sn* command in the test case
	(Look at CASE 2 for more information.)

	Example:
	'ABCD123456'


The legend and test file together provide a way to convert tests for FDA testing of the StimonTrack
app into cases executable by the robot, and to map all buttons in the app to a coordinate. 
