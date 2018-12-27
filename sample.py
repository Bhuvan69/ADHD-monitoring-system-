#!/usr/bin/python


#Import the OpenCV and dlib libraries
import cv2
import dlib
import time
import picamera 
import numpy as np
#Initialize a face cascade using the frontal face haar cascade provided with
#the OpenCV library
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#The deisred output width and height
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600

def detectAndTrackLargestFace():
    #Open the first webcame device
    cap = cv2.VideoCapture(0)
    #print ("hello")
    #Create two opencv named windows
    #cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
    #cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)

    #Position the windows next to eachother
    #cv2.moveWindow("base-image",0,100)
    #cv2.moveWindow("result-image",400,100)

    #Start the window thread for the two windows we are using
    #cv2.startWindowThread()

    #Create the tracker we will use
    tracker = dlib.correlation_tracker()
    #print("hello")
    #The variable we use to keep track of the fact whether we are
    #currently using the dlib tracker
    trackingFace = 0
  
    #To keep track X, Y Value
    xValue = 0
    yValue = 0
	
    #Assigning Limits
    xnot = 1
    ynot = 1
    #xLimit2 = 250
    #yLimit2 = 250
    count = -1

    #The color of the rectangle we draw around the face
    rectangleColor = (0,165,255)
    #print("hello")
    try:
        while True:
            #print("hello")
            #Retrieve the latest image from the webcam
            #rc,fullSizeBaseImage = capture.read()
	    ret, img = cap.read()
            #Resize the image to 320x240
            #baseImage = cv2.resize( fullSizeBaseImage, (320, 240))


            #Check if a key was pressed and if it was Q, then destroy all
            #opencv windows and exit the application
            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('Q'):
                #cv2.destroyAllWindows()
                exit(0)



            #Result image is the image we will show the user, which is a
            #combination of the original image from the webcam and the
            #overlayed rectangle for the largest face
            #resultImage = baseImage.copy()





	
            #If we are not tracking a face, then try to detect one
            if not trackingFace:
		#count = count + 1
			
                	#For the face detection, we need to make use of a gray
                	#colored image so we will convert the baseImage to a
                	#gray-based image
                	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                	#Now use the haar cascade detector to find all faces
                	#in the image
                	faces = faceCascade.detectMultiScale(gray, 1.3, 5)

                	#In the console we can show that only now we are
                	#using the detector for a face
                	#print("Using the cascade detector to detect face")
			#count = count + 1

                	#For now, we are only interested in the 'largest'
                	#face, and we determine this based on the largest
                	#area of the found rectangle. First initialize the
                	#required variables to 0
                	maxArea = 0
                	x = 0
                	y = 0
                	w = 0
                	h = 0


                	#Loop over all faces and check if the area for this
                	#face is the largest so far
                	#We need to convert it to int here because of the
                	#requirement of the dlib tracker. If we omit the cast to
                	#int here, you will get cast errors since the detector
                	#returns numpy.int32 and the tracker requires an int
                	for (_x,_y,_w,_h) in faces:
                	    if  _w*_h > maxArea:
                	        x = int(_x)
                	        y = int(_y)
                	        w = int(_w)
                	        h = int(_h)
                	        maxArea = w*h

                	#If one or more faces are found, initialize the tracker
                	#on the largest face in the picture
                	if maxArea > 0 :

	                    #Initialize the tracker
			    tracker.start_track(img, dlib.rectangle(x-10, y-20, x+w+10, y+h+20))	
        	            #Set the indicator variable such that we know the
                	    #tracker is tracking a region in the image
                    	    trackingFace = 1
		            #xnot = 0
            	#Check if the tracker is actively tracking a region in the image
            if trackingFace:
                	#Update the tracker and request information about the
                	#quality of the tracking update
                	trackingQuality = tracker.update( img )



                	#If the tracking quality is good enough, determine the
                	#updated position of the tracked region and draw the
                	#rectangle
                	if trackingQuality >= 8.75:
                	    tracked_position =  tracker.get_position()

                	    t_x = int(tracked_position.left())
                	    t_y = int(tracked_position.top())
                	    t_w = int(tracked_position.width())
                	    t_h = int(tracked_position.height())
                	    cv2.rectangle(img, (t_x, t_y), (t_x + t_w , t_y + t_h), rectangleColor ,2)

                    	    #xValue = t_x + t_w
                   	    #yValue = t_y + t_h
                	else:
                    	#If the quality of the tracking update is not
                    	#sufficient (e.g. the tracked region moved out of the
                    	#screen) we stop the tracking of the face and in the
                    	#next loop we will find the largest face in the image
                    	#again
 	                   	trackingFace = 0
				xnot = 1




            #Since we want to show something larger on the screen than the
            #original 320x240, we resize the image again
            #
            #Note that it would also be possible to keep the large version
            #of the baseimage and make the result image a copy of this large
            #base image and use the scaling factor to draw the rectangle
            #at the right coordinates.
            largeResult = cv2.resize(img,
                                     (OUTPUT_SIZE_WIDTH,OUTPUT_SIZE_HEIGHT))

            #Finally, we want to show the images on the screen
            #cv2.imshow("base-image", baseImage)
            #cv2.imshow("result-image", largeResult)

            if xnot == ynot:
		count = count + 1
		#mylist = []
		#today = datetime.date.time.today()
		#mylist.append(today)
		#d = datetime.datetime.today()
                print count,",", time.strftime("%H:%M:%S"),",", time.strftime("%d/%m/%Y")
		xnot = 0
                #print("X Value = ", xValue, " and Y Value = ", yValue)
            #elif xValue > xLimit2 or yValue > yLimit2:
                     #print("movement not happenning")
                     #print("X Value = ", xValue, " and Y Value = ", yValue)

            #print("X Value = ", xValue, " and Y Value = ", yValue)

            #print(count)
    #To ensure we can also deal with the user pressing Ctrl-C in the console
    #we have to check for the KeyboardInterrupt exception and destroy
    #all opencv windows and exit the application
    except KeyboardInterrupt as e:
        #cv2.destroyAllWindows()
        exit(0)


if __name__ == '__main__':
    detectAndTrackLargestFace()

