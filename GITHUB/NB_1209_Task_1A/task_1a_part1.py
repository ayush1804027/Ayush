'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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
# Author List:		[ Pushkar Prashant ,Ayush Kumar ]
# Filename:			task_1a_part1.py
# Functions:		scan_image
# 					[ Comma separated list of functions in this file ]
# Global variables:	shapes
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################






##############################################################


def scan_image(img_file_path):

    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }
    
    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes
    shapes={}
    ##############	ADD YOUR CODE HERE	##############
    
    img = cv2.imread(os.path.join(img_file_path))
    img=cv2.blur(img,(4,4))
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    col = {"blue","green","red"}
    low_blue = np.array([110,50,50])
    high_blue = np.array([130,255,255])
    low_green = np.array([36,25,25])
    high_green = np.array([70,255,255])
    low_red = np.array([0,100,100])
    high_red = np.array([0,255,255])

    for i in col:
        if i=="blue":
            lower=low_blue
            high=high_blue
            color=i
        elif i=="green":
            lower=low_green
            high=high_green
            color=i
        elif i=="red":
            lower=low_red
            high=high_red
            color=i
        mask=cv2.inRange(hsv,lower,high)
            
        contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #CHAIN_APPROX_SIMPLE GIVE NO.OF VERTEX
        
        for cont in contours:
            Area=cv2.contourArea(cont)
            M=cv2.moments(cont)
            cX=int(M['m10']/M['m00'])
            cY=int(M['m01']/M['m00'])
            
            epsilon=cv2.arcLength(cont,True)
            approx=cv2.approxPolyDP(cont,0.01*epsilon,True)
            (x,y,w,h)=cv2.boundingRect(approx)
            rect_area = w*h
            extent=float(Area)/rect_area
            aspect_ratio=w/float(h)
            
            if len(approx)==3:
                shape="Triangle"
            elif len(approx)==4:
                rhom=h*(w)-h*(w/4)
                llgm=h*(w-Area/h)
                
                if Area<=1.1*rect_area and aspect_ratio>=0.95 and aspect_ratio<=1.05 and extent>0.96:
                    shape="Square"
                elif Area<rect_area*0.85 and extent<0.80:
                    shape="Rhombus"
                elif Area<=rect_area and extent>0.95:
                    shape="Rectangle"
                elif Area<=rect_area and extent<0.80 and aspect_ratio>1.8:
                    shape="Parallelogram"
                elif extent>0.78:
                    shape="Trapezium"
                else:
                    shape="Quadrilateral"
                    
            elif len(approx)==5:
                shape="Pentagon"
            elif len(approx)==6:
                shape="Hexagon"
            else:
                shape="Circle"
            shapes[shape]=[color,Area,cX,cY]    

         

	##################################################
    
    
    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in '+ curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'
    
    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')
    
    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()
    
    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')
        
        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2
        
        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')
            
            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the selected file.')
                exit()
            
            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')
                
                else:
                    print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
