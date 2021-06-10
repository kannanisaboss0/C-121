#--------------------------------------------------------------------------VideoModifier.py--------------------------------------------------------------------------#

import numpy as np
import cv2 as cv2
import time as tm 

'''
Importing modules:
- numpy (np)
- cv2 (cv2)
- time (tm)
'''

#Defining a function to ask the user to determine the rate
def AskRate():
    print("Instantaneous appearence can be achieved by setting the value greater than 3")
    print("A recommendable value would be 0.25 or 0.5.")

    rate_param=float(input("Please enter the appearence rate of the active foreground layer(in HSV value/second):"))

    return rate_param

#Defining a function to specefically warn the user about setting the HSV value and to input their ressurective operations
def ShowAppearenceSettings():    
    rate_param=AskRate()

    #Warning the user of setting a value above the recommended limit
    #Case-1
    if(rate_param>3):
       warn_rate_param=input("By setting the rate above 3, the effect of constructive transition will be majorly oppressed. Continue?(:-Yes or No)")

       #Verifying the user's option on continuing with the confuration
       #Case-1
       if(warn_rate_param=="No" or warn_rate_param=="no"):
           ShowAppearenceSettings()

    value_param=0

    return rate_param,value_param 
        
      


four_cc=cv2.VideoWriter.fourcc(*"XVID")
file=cv2.VideoWriter("file.avi",four_cc,81.0,(820,450))

#Introductory  messages and user inputs
print("Welcome to VideoMofifier.py. We provide special effects for enhancing video quality.")

tm.sleep(2.3)

effects_list=["Unusable_Element","Transperancy","Appearence","Partial Invisibility"]

effects_count=0

for effect in effects_list[1:]:
    effects_count+=1
    print("{}:{}".format(effects_count,effect))

effect_input=int(input("Please enter the index of the corresponding effect desired to view:"))

effect_choice=effects_list[effect_input]

print("Effect '{}' chosen".format(effect_choice))
if(effect_input==1):
    print("Transperancy:-Decreases the opacity of the output.")
elif(effect_input==2):
    print("Appearence:-Makes the active foreground appear at a fixed rate.") 
elif(effect_input==3):
    print("Partial Visibility:-Practically renders the active foreground out of the ouput, with only a selected portion to be displayed.")          
Video=cv2.VideoCapture(0)

tm.sleep(2.3)

bg=0

rate=None
value=None

if(effect_input==2):
    rate,value=ShowAppearenceSettings()

for loop in range(60):
    ret,bg=Video.read()

bg=np.flip(bg,axis=1)  

while(Video.isOpened()):
     
    ret,img=Video.read()

    img=np.flip(img,axis=1)

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower_red=None
    upper_red=None

    #Executing the method depending on the user input provided above
    #Case-1
    if(effect_input==2):
            value+=rate

            lower_red = np.array([0,0,0])       
            upper_red = np.array([int(value),int(value),int(value)])

    #Case-2
    elif(effect_input==3):
        lower_red = np.array([0,0,200])       
        upper_red = np.array([360,360,360])

    #Case-3    
    else:
        lower_red = np.array([0,20,100])       
        upper_red = np.array([360,360,360])

    mask_1=cv2.inRange(hsv,lower_red,upper_red)

    mask_1=mask_1
    
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3), np.uint8))
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3), np.uint8))
    
    mask_2=cv2.bitwise_not(mask_1)

    res_1=0
    res_2=0

    #Executing the method depending on the user input provided above
    #Case-1
    if(effect_input==1):
        res_1=cv2.bitwise_and(img,img)
        res_2=cv2.bitwise_and(bg,bg)

    #Case-2
    else:
        res_1=cv2.bitwise_and(img,img,mask=mask_1)
        res_2=cv2.bitwise_and(bg,bg,mask=mask_2)
  
    output=cv2.addWeighted(res_1,1,res_2,1,0)
    
    file.write(output)

    cv2.imshow("Cloak",output)
    cv2.waitKey(1)

Video.release()
cv2.destroyAllWindows()

#Prinintg the ending message
print("Thank you for using VideoModifier.py")

#--------------------------------------------------------------------------VideoModifier.py--------------------------------------------------------------------------#