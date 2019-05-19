import time
start = time.time()
import random
import cv2

sqrState=1; #first run- the square is not on screen,  rand1 and rand2 need to be sent in
rand1=random.randint(0, 520)
rand2=random.randint(0, 1080)
rand_r = random.randint(0, 255)
rand_g = random.randint(0, 255)
rand_b = random.randint(0, 255)
filter_reference.write(0x30, sqrState)
print(filter_reference.read(0x30))
score = 0
i=0
n=2
font = cv2.FONT_HERSHEY_SIMPLEX
scoreCheck = True
dontdo = True
itera = True
swap = True
colourChange = False
GameLength = 60
timeTaken=0
startTime=time.time()

while time.gmtime(timeTaken) < time.gmtime(GameLength):
#for i in range(60000):
    if(n<12):
        if(i>0 and i%500==0):
            n=n+1
    if(sqrState==1):
        if(rand1>260):
            rand1=rand1+n
        else:
            rand1=rand1-n
        if(rand2>540):
            rand2=rand2-n
            dontdo = False
            itera = True
        elif(dontdo and iter):
            rand2=rand2+n
            itera = False
            dontdo = True
        if(rand1>720 or rand2>1280 or rand1<-200 or rand2 < -200):
            sqrState=0
            scoreCheck=False
            colourChange = True
        if(sqrState==1):
            filter_reference.write(0x38, rand1)
            filter_reference.write(0x40, rand2)
    if(sqrState == 0):
        rand1=random.randint(0, 520)
        rand2=random.randint(0, 1080)
        print(rand1, ",", rand2)
        filter_reference.write(0x38, rand1)
        filter_reference.write(0x40, rand2) #send in new numbers
        sqrState = 1
        if(scoreCheck==True):
            score=score+1
            colourChange = True
        scoreCheck=True
    
    in_frame = hdmi_in.readframe()
    out_frame = hdmi_out.newframe()
    filter_reference.write(0x10, in_frame.physical_address)   # Get Pointers to memory
    filter_reference.write(0x18, out_frame.physical_address)
    filter_reference.write(0x20, 1280)   # Make sure that the input HDMI signal is set to 1280x720
    filter_reference.write(0x28, 720)

    filter_reference.write(0x00, 0x01)             # ap_start triggering
    while (filter_reference.read(0) & 0x4) == 0:   # ap_done checking
        pass
    sqrState = filter_reference.read(0x48)
    cv2.putText(out_frame,f"score = {score}",(10,100), font, 1,(255,0,0),2,cv2.LINE_AA)
    cv2.circle(out_frame, (int(rand2), int(rand1)), int(10),(0, 255, 255), 2)
    if(colourChange):
        rand_r = random.randint(0, 255)
        rand_g = random.randint(0, 255)
        rand_b = random.randint(0, 255)
    cv2.rectangle(out_frame,(rand2,rand1),(rand2+200,rand1+200),(255,255,255),-1)
    cv2.rectangle(out_frame,(rand2+30,rand1+50),(rand2+40,rand1+60),(0,0,0),-1)
    cv2.rectangle(out_frame,(rand2+110,rand1+50),(rand2+120,rand1+60),(0,0,0),-1)
    # cv2.ellipse(out_frame, (rand2+30,rand1+130), axes, angle, startAngle, endAngle, color[, thickness[, lineType[, shift]]])
    if(swap):
        cv2.circle(out_frame, (rand2+70,rand1+100), 10, (255,0,0), -1)
        swap = False
    else:
        cv2.circle(out_frame, (rand2+70,rand1+100), 15, (255,0,0), -1)
        swap = True
    remaining = int((GameLength - timeTaken)) 
    cv2.putText(out_frame,f"TIME REMAINING = {remaining}",(500,100), font, 1,(255,0,0),2,cv2.LINE_AA)
    colourChange = False
    hdmi_out.writeframe(out_frame)
    i=i+1
    timeTaken=time.time()-startTime
  
cv2.putText(out_frame,'GAME OVER',(540,260), font, 1,(255,0,0),2,cv2.LINE_AA)
