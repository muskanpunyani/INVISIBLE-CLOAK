<*** note: Do use mobile camera for better performance***>



import cv2
import numpy as np
import time
#we are removing foreground frame in green screening we remove background frame

fourcc= cv2.VideoWriter_fourcc(*'XVID')   # for saving the video
out1 = cv2.VideoWriter('output1.avi', fourcc, 20.0, (1920, 1080))   # (output video name,fourcc,fps,frame size)
# fps(defined frame rate of the output video screen)
# frame size(width,height) should be same as the input video size
#fourcc : for recording(defining the codec)


# in order to check the cv2 version
#print(cv2.__version__)

# taking video.mp4 as input.
# Make your path according to your needs
capture_video = cv2.VideoCapture("input.mp4")


# give time to camera to warm up
time.sleep(1)
count = 0
background = 0

# capturing the background in range of 60
# you should have video that have some seconds
# dedicated to background frame so that it
# could easily save the background image
# i.e input video
for i in range(60):
    return_val, background = capture_video.read()  #read the input video
    if return_val == False:  # if no video is given it will return false
        continue

background = np.flip(background, axis=1)  # flipping of the frame
#flip(arr,axis=0 or 1) , axis=0 means flip array vertically
# axis=1 means flip array horizontally

# we are reading from video
while (capture_video.isOpened()):  #video is opened
    return_val, img = capture_video.read()   #read video
    if not return_val:
        break
    count = count + 1
    img = np.flip(img, axis=1)   #the images are captured till video is running

    # convert the image - BGR to HSV
    # as we focused on detection of red color

    # converting BGR to HSV for better
    # detection or you can convert it to gray

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #this is also in while loop
    #converting BGR TO HSV (evey image)

# -------------------------------------BLOCK----------------------------#
    # ranges should be carefully chosen
    # setting the lower and upper range for mask1
    lower_red = np.array([100, 40, 40])  #creating array using numpy,the only diff in this creation and original
    #is that using numpy we create nd array
    #the above array is 1-d
    upper_red = np.array([100, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # setting the lower and upper range for mask2
    lower_red = np.array([155, 40, 40])  #detecting red color
    #these are values of red color (h,s,v)
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    # ----------------------------------------------------------------------#

    # the above block of code could be replaced with
    # some other code depending upon the color of your cloth
    #just need to change h,s,v value
    mask1 = mask1 + mask2

    # Refining the mask corresponding to the detected red color
    #now we will replace the red portion with a mask image in each frame
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3),
                                                            np.uint8), iterations=2) #open the mask image
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)  #dilate the mask image
    mask2 = cv2.bitwise_not(mask1)      #create a inverted mask to segment out red color from frame

    # Generating the final output
    # create frame showing static background frame pixels only for the masked region
    res1 = cv2.bitwise_and(background, background, mask=mask1)

    # segment the red color part out of the frame using bitwise and with inverted frame
    res2 = cv2.bitwise_and(img, img, mask=mask2)

    #create the output
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    out1.write(final_output) #save the output

    cv2.imshow("INVISIBLE CLOAK", final_output)
    k = cv2.waitKey(10)
    if k == 27:    #it means if escape is pressed exit
        break
