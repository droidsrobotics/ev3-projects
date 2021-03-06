#!/usr/bin/python
# -*- coding: utf-8 -*- import python packages



#install --> (sudo) apt-get install python-pip --> (sudo) pip install pillow termcolor python-ev3dev
#running --> run (sudo) python pythonfilename.py imagefilename.png (jpg will work along with others types) -->
#            you will be given a dialogue --> just type "" and return/enter to continue --> when presented with a color dialogue swap pen to that color
#errors --> try using (r,g,b = ...) instead of (r,g,b,a = ...) ***EVERYWHERE BELOW**

from PIL import Image, ImageFilter
from termcolor import colored
import ev3dev.ev3 as ev3
import time
from ev3dev import *
import os
import sys

# paper resolution
#horiz_deg = -1800; #degress max move
#horiz_width = 5; #inches
#horiz_res = horiz_deg/horiz_width; # degrees per inch
#vertical_deg = 850; #degress max move
#vertical_width = 6.5; #inches
#vertical_res = vertical_deg/vertical_width; # degrees per inch
#vert_move = 7;
#horiz_move = vert_move*horiz_res/vertical_res;
#res = horiz_deg/horiz_move/1.1;

# paper resolution
horiz_deg = 1950; #degress max move
horiz_width = 6; #inches
horiz_res = horiz_deg/horiz_width-10; # degrees per inch
vertical_deg = -17000; #degress max move
vertical_width = 6.5; #inches
vertical_res = vertical_deg/vertical_width; # degrees per inch
vert_move = 15;
horiz_move = vert_move*horiz_res/vertical_res;
res = 140;
bottom = 1700

horiz_move = 15;



#function to ensure the motor has stopped before moving on
xxx = 0
def waitformotor(motor):
    #run more than once to ensure that motor is stopped and that it was not a false reading
    while motor.state != []:
        xxx = 0

#define motors and use brake mode
paper = ev3.MediumMotor('outA')
pen = ev3.MediumMotor('outB')
LR = ev3.MediumMotor('outC')
pen2= ev3.MediumMotor('outD')
pen.stop_action = u"brake"
LR.stop_action = u"brake"
paper.stop_action = u"brake"
LR.ramp_up_sp=100
LR.ramp_down_sp=200
LR.reset()
pen.reset()
pen2.reset()
#LR.run_to_abs_pos(position_sp=-50, duty_cycle_sp=75)
waitformotor(LR)
waitformotor(LR)
LR.reset()
paper.reset()
#move paper until color sensor recieves >50 reading



#make a function to make a dot on the page
#def makedot():
#    pen.run_to_abs_pos(position_sp=bottom, speed_sp=1000, ramp_down_sp=500)
#    pen.run_t(time_sp=1230, speed_sp=1000)
#    waitformotor(pen)
#    waitformotor(pen) #double check if motor is stopped before raising pen
#    pen.run_to_abs_pos(position_sp=bottom-1000, speed_sp=1000, ramp_down_sp=500)
#    pen.run_timed(time_sp=1200, speed_sp=-1000)
#    waitformotor(pen)
#    waitformotor(pen)


ts = ev3.TouchSensor()
while ts.value() != 1:
	print ts.value()
	print "Please activate!"

def makedot():
#    pen.run_to_abs_pos(position_sp=bottom, speed_sp=1100, ramp_down_sp=500)
    pen.run_timed(time_sp=300, speed_sp=-1000)
    waitformotor(pen)
    waitformotor(pen) #double check if motor is stopped before raising pen
#    pen.run_to_abs_pos(position_sp=0, speed_sp=1000, ramp_down_sp=500)
    pen.run_timed(time_sp=300, speed_sp=1000)
    waitformotor(pen)
    waitformotor(pen)

def makedot2():
#    pen.run_to_abs_pos(position_sp=bottom, speed_sp=1100, ramp_down_sp=500)
    pen2.run_timed(time_sp=300, speed_sp=-1000)
    waitformotor(pen2)
    waitformotor(pen2) #double check if motor is stopped before raising pen
#    pen.run_to_abs_pos(position_sp=0, speed_sp=1000, ramp_down_sp=500)
    pen2.run_timed(time_sp=300, speed_sp=1000)
    waitformotor(pen2)
    waitformotor(pen2)

#def makedot2():
#    pen2.run_to_abs_pos(position_sp=bottom, speed_sp=1000, ramp_down_sp=500)
#    pen.run_t(time_sp=1230, speed_sp=1000)
#    waitformotor(pen2)
#    waitformotor(pen2) #double check if motor is stopped before raising pen
#    pen2.run_to_abs_pos(position_sp=bottom-1000, speed_sp=1000, ramp_down_sp=500)
#    pen.run_timed(time_sp=1200, speed_sp=-1000)
#    waitformotor(pen2)
#    waitformotor(pen2)

#copy image to print.jpg
filename = sys.argv[1]
#cmd = "cp '"+filename+"' print.jpg"
print filename
#os.system("convert "+filename+" -resize 80 /home/sanjay/print.jpg") #alternate automatic resizer for image note -- changes color of pixels (do not know why)

#execute copy
#os.system(cmd)
os.system("convert "+filename+" -rotate 90 print.png") #alternate automatic resizer for image note -- changes color of pixels (do not know why)


w = 0
h = 0
l = 0
img2 = Image.open('print.png') #open image
img=img2.convert("RGBA")
width, height = img.size # get image size

#define variables
array = []
w = width-1 #define starting width counter
print width," x ", height
r_array=[]
g_array = []
b_array = []
bl_array = []

#different colors: (in rgba -- remove last number in set to convert to rgb)
#red = (255,0,0,0) eg. in rgb -- (255,0,0)
#green = (0,255,0,0)
#blue = (0,0,255,0)
#black = (0,0,0,0)
#white = (255,255,255,0)
print img.getpixel((w,h))

while h != height:
        while w != -1:
                array.append(img.getpixel((w, h))) #get rgba black or white of each pixel and write to full array
                r,g,b,a = img.getpixel((w, h)) #get rgba of each pixel
                #check if red, green, or blue is greatest in rgb values --- check if black or white also --> then append array differently for each switch case
                if r > g and r > b :
                    r_array.append(0)
                    g_array.append(255)
                    b_array.append(255)
                    bl_array.append(255)
                elif g > r and g > b :
                    g_array.append(0)
                    r_array.append(255)
                    b_array.append(255)
                    bl_array.append(255)
                elif b > r and b > g :
                    b_array.append(0)
                    g_array.append(255)
                    r_array.append(255)
                    bl_array.append(255)
                elif b < 50 and r < 50 and g < 50 :
                    b_array.append(255)
                    g_array.append(255)
                    r_array.append(255)
                    bl_array.append(0)
                else:
                    b_array.append(255)
                    g_array.append(255)
                    r_array.append(255)
                    bl_array.append(255)
                w = w-5 #move to next pixel -- use -1 to flip image -> make images not backward when printed 
        w = width-1 #reset width counter
        h = h+5 #move to next row






#x = input('Type text to preview picture(s) (in quotes) >>') #wait until dialogue is answered then show preview


height = height/5
width = width/5

xd = 0
yd = 0
xda = 0
while yd < height:
        while xd < width:
                r,g,b,a = array[xda] #get rgba of each pixel save in array
                #check if red, green, or blue is greatest --- check if black or white also
#               if r > g and r > b: #is pixel black?
#                                        print colored("█","red"),
                if b > g and b > r: #is pixel black?
                                        print colored("█","blue"), 
#                                       nnn=0
#                elif g > b and g > r: #is pixel black?
#                                        print colored("█","green"), #print block if black pixel
#                                       nnn=0
                elif r < 50 and b < 50 and g < 50:
                        print " ", #if terminal background is not black print block here instead
                else:
                        print  "█", #if terminal background is not black print a space here instead
                xd = xd + 1 #increase counters
                xda = xda + 1
        print(" ")
        #reset and increase counters
        yd = yd + 1
        xd = 0





#x = input('BLACK/BLUE>>') #wait for dialogue to be answered then start printing
all_pixels = bl_array 
all_pixels2 = b_array
xd = 0
yd = 0
xda = 0 
while yd != height:
    while xd != width:
        if all_pixels[xda] == 0: #is pixel black?
            print "█", #print block if black pixel
            LR.run_to_abs_pos(position_sp=horiz_move*xd, speed_sp=400, ramp_down_sp=500)
            waitformotor(LR)
            # lower and raise pen
#            pen.run_timed(time_sp=250, duty_cycle_sp=-75)
            makedot()
            # move pen left	
        elif all_pixels2[xda] == 0:
            print "█", #print block if red pixel
            LR.run_to_abs_pos(position_sp=(horiz_move*xd)+319, speed_sp=400, ramp_down_sp=500)
#            LR.run_to_abs_pos(position_sp=(horiz_move*xd)+230, speed_sp=400, ramp_down_sp=500)
            waitformotor(LR)
            # lower and raise pen
#            pen.run_timed(time_sp=250, duty_cycle_sp=-75)
            makedot2()
	else:
            print " ",
            #move pen left
        xd = xd + 1
        xda = xda + 1

    print(" ")
    yd = yd + 1
    xd = 0
    # move paper forward
    paper.run_to_abs_pos(position_sp=vert_move*(yd), speed_sp=250,ramp_down_sp=500)
    # reset pen location
    waitformotor(paper)
    waitformotor(paper)

#reset paper location
paper.run_to_abs_pos(position_sp=0, speed_sp=1000)

LR.run_to_abs_pos(position_sp=0, speed_sp=1000)
pen.run_to_abs_pos(position_sp=0, speed_sp=1000)
pen2.run_to_abs_pos(position_sp=0, speed_sp=1000)
waitformotor(paper)
waitformotor(LR)
waitformotor(pen)
waitformotor(pen2)

