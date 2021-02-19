'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ NB_1209 ]
# Author List:		[ Ayush Kumar,Pushkar Prashant ]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv,length,approxpixel,blockval
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################



def length(x1,y1,x2,y2):
    l=((x1-x2)**2+(y1-y2)**2)**0.5
    return l

def approxpixel(wrap_image,i,j):
    pixel=255
    for a in range(i,i+8,1):
        for b in range(j,j+8,1):
            if wrap_image[a][b]==0:
                pixel=0
    for a in range(i-8,i,1):
        for b in range(j-8,j,1):
            if wrap_image[a][b]==0:
                pixel=0
    return pixel

def blockval(wrap_image,i,j,d):
    block=0
    
    W=approxpixel(wrap_image,i+23,j)#wrap_image[i+23][j]
    N=approxpixel(wrap_image,i,j+23)#N=wrap_image[i][j+23]
    E=approxpixel(wrap_image,i+23,j+47)#wrap_image[i+23][j+47]
    S=approxpixel(wrap_image,i+47,j+23)#wrap_image[i+47][j+23]
    
    if N<50 or i==4:
        block+=2
    if W<50 or j==4:
        block+=1
    if S<50 or i==427:
        block+=8
    if E<50 or j==427:
        block+=4    
    #print(N,W,S,E)
    return block


##############################################################


def applyPerspectiveTransform(input_img):
    warped_img = None
    
    img=input_img
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=cv2.bilateralFilter(gray,15,75,75)
    canny=cv2.Canny(gray,120,255,0)
    corners=cv2.goodFeaturesToTrack(canny,50,0.4,50)
    c1=[]
    c2=[]
    c3=[]
    for corner in corners:
        x,y=corner.ravel()
        sum1=int(x)+int(y)
        c1.append(sum1)
        c2.append(int(x))
        c3.append(int(y))
    for corner in corners:
        x,y=corner.ravel()
        sum1=int(x)+int(y)
        if sum1==min(c1) and sum1>0:
            x1=int(x)
            y1=int(y)
                
        elif sum1==max(c1) and sum1>0:
            x4=int(x)
            y4=int(y)
        elif int(x)==min(c2) or int(y)==max(c3):
            x2=int(x)
            y2=int(y)
        elif int(x)==max(c2) or int(y)==min(c3):
            x3=int(x)
            y3=int(y)    
    l12=length(x1,y1,x2,y2)
    l13=length(x1,y1,x3,y3)
    l34=length(x3,y3,x4,y4)
    l42=length(x4,y4,x2,y2)


    if round((l12-l13)/40.4)!=0:              #l12 !=l13
        if l12>l13 and l13<380:        
            x3=x3+round((l12-l13)/40)*38
            x3=int(x3)
    if round((l12-l42)/40.4)!=0:              #l12 !=l42
        if l12<l42:        
            y2=y2+round((404-l12)/41)*41
            y2=int(y2)
    if round((l34-l13)/40.4)!=0:               #l34 !=l13
        if l34<l13:        
            y3=y3-round((404-l34)/41)*38
            y3=int(y3)   
    if round((l34-l42)/40.4)!=0:                #l34 !=l42
        if l34>l42:        
            x2=x2-round((l34-l42)/40)*38
            x2=int(x2)
    pts1=np.float32([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
    pts2=np.float32([[6,6],[6,475],[475,6],[475,475]])

    M=cv2.getPerspectiveTransform(pts1,pts2)
    warped_img=cv2.warpPerspective(img,M,(482,482))
    
    return warped_img 
def detectMaze(warped_img):
    maze_array = []
    
    warped_img = cv2.cvtColor(warped_img,cv2.COLOR_BGR2GRAY)
    (thresh,warped_img)=cv2.threshold(warped_img,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    count=0
    cellsize=47
    for i in range (4,429,47):                 #431
        col=[]
        for j in range(4,429,47):
            cv2.circle(warped_img,(i,j),1,(0,0,255),-1)        
            block=blockval(warped_img,i,j,cellsize)
            col.append(block)
        maze_array.append(col)
    
    return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

	# path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()
	
	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):
			
			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
			
			# read the image file
			input_img = cv2.imread(img_file_path)

			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)

				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')
					
					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)

					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				
				else:

					print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()
			
			else:

				print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')

