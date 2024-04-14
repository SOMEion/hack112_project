from cmu_112_graphics import *
import random
import numpy as np
from PIL import Image, ImageDraw
import time
import os
import pyaudio
import sys
import numpy as np
import aubio
import statistics
import math
#############################################################
# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

if len(sys.argv) > 1:
    # record 5 seconds
    output_filename = sys.argv[1]
    record_duration = 5 # exit 1
    outputsink = aubio.sink(sys.argv[1], samplerate)
    total_frames = 0
else:
    # run forever
    outputsink = None
    record_duration = None

# setup pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

# magVals = [0]
# magChunk = []
#global pitchChunk
pitchChunk = [0,0]

########################################################################
# SCREENS: splash/ play/ end
# def splash_onScreenStart(app):

def almostEqual(a,b):
    if abs(a-b)<=10:
        return True
    return False

def appStarted(app):
    app.play=False
    app.timer=0
    app.timerDelay=1
    app.image0=loadAnimatedGif0('bird_closed.gif')
    app.image1=loadAnimatedGif1('bird_open.gif')
    app.image2=loadAnimatedGif2('bug_slow.gif')
    app.image3=loadAnimatedGif3('bug_fast.gif')
    app.count0=0
    app.count1=0
    app.count2=0
    app.count3=0
    app.cloud1=app.loadImage('cloud1.png')
    app.cloud2=app.loadImage('cloud2.png')
    app.cloud3=app.loadImage('cloud3.png')
    app.cloud4=app.loadImage('cloud4.png')
    app.images=app.loadImage('sky.png')
    app.pa=app.loadImage('play.png')
    app.tweater1=app.loadImage('tweater1.png')
    app.cy=(Bird.rail)*app.height/14-app.height/28
    app.cloudImage=[app.cloud1,app.cloud2,app.cloud3,app.cloud4]
    app.timerC=0
    app.cloud=True
    app.Introx=app.width/2
    app.pausex=app.width/2
    app.open=False
#####################Loading image################
def loadAnimatedGif0(path):
    image0 = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            image0.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return image0

    
def loadAnimatedGif1(path):
    image1 = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            image1.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return image1

def loadAnimatedGif2(path):
    image2 = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            image2.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return image2

def loadAnimatedGif3(path):
    image3 = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            image3.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return image3 
    
    
    
class Food:
    onScreenList = [ ]
    upCommingList=[]
    def __init__(self, parameter, row, timeDelay):
        self.parameter = parameter #the location of the food item on screen 
        self.row = row #the number of row that the food is in 
        self.timeDelay = timeDelay #amount of time delay before an item is added to the on-screen list

    @classmethod   
    def timerFired(cls, app):
        if app.play == True and Food.upCommingList != [ ]:#if the upcomming list is not empty
            delay = Food.upCommingList[0].timeDelay #get the needed amount of time delay 
            app.timer += 1
            
            if app.timer == delay:#if the delay is reached
                app.timer = 0#refresh the timer
                Food.onScreenList.append(Food.upCommingList.pop(0))#add the first food of the upcomming list to the on screen list
    #make list of corn?

class Cloud:
    onScreenList=[]
    upCommingList=[]
    
    def __init__(self,parameter,cloudType,timeDelay):
        self.parameter= parameter
        self.timeDelay=timeDelay
        self.cloudType=cloudType
    

    @classmethod   
    def timerFired(cls, app):
        if Cloud.upCommingList != [ ]:#if the upcomming list is not empty
            delay = Cloud.upCommingList[0].timeDelay #get the needed amount of time delay 
            app.timerC += 1
            if app.timerC == delay:#if the delay is reached
                app.timerC = 0#refresh the timer
                Cloud.onScreenList.append(Cloud.upCommingList.pop(0))#add the first food of the upcomming list to the on screen list
    #make list of corn?
    
class Bird:
  rail = 14
  def __init__(self):
    self.cy = 250
    self.mouthOpen = False
    self.targetRrail=False
  def __repr__(self):
    return f'bird on rail {self.currentRail}, mouth open is {self.mouthOpen}'

def moveRrail(app,bird):
    if bird.targetRrail==False:
        return False
    else:
        target=(bird.targetRrail)*app.height/14-app.height/28
        
        if almostEqual(app.cy,target):
            
            bird.targetRrail=False
    
        elif app.cy<target:
            
            app.cy+=17
            Bird.rail=int(((app.cy)/(app.height/14))+1)
        elif app.cy>target:
            
            app.cy-=17
            Bird.rail=int(((app.cy)/(app.height/14))+1)
            
                  
        
bird=Bird()

############player interface#############


############
# splash screen
############


def redrawAll(app,canvas):
    
    drawLine(app,canvas)
    drawBackgroud(app,canvas)
    drawCloud(app,canvas)
    drawTweater(app,canvas)
    drawPause(app,canvas)
    drawBird(app,canvas)
    drawFood(app,canvas)
    #drawblack(app,canvas)

def splitScreen(app):
    if app.play==True:
        app.Introx-=15
        app.pausex+=15
        
def mousePressed(app,event):
    cx=app.width/2
    cy=4*app.height/5
    
    if cx-50<event.x<cx+50 and cy-60<event.y<cy+60:
        app.play=True
        L=Gen(app)
        Food.upCommingList=L
        Food.onScreenList.append(Food.upCommingList.pop(0))
        

def keyPressed(app,event):
    
        
    
    if event.key=="w":
        if Bird.rail>1: 
            Bird.rail-=1
            bird.targetRrail=False
            app.cy=(Bird.rail)*app.height/14-app.height/28
            
    elif event.key=="s":
        if Bird.rail<14: 
            Bird.rail+=1
            bird.targetRrail=False
            app.cy=(Bird.rail)*app.height/14-app.height/28


def timerFired(app):
    splitScreen(app)
    eat(app)
    Cloud.timerFired(app)
    for cloud in Cloud.onScreenList:
            cloud.parameter[0]-=1
            if cloud.parameter[0]<-200:
                Cloud.onScreenList.remove(cloud)
    if app.cloud==True:
        L=CloudListGen(app)
        app.cloud=False 
        Cloud.upCommingList=L
        Cloud.onScreenList.append(Cloud.upCommingList.pop(0))
        
    if app.play==True:
        moveRrail(app,bird)
        for food in Food.onScreenList:
            food.parameter[0]-=4
            food.parameter[2]-=4
            if food.parameter[2]<-200:
                Food.onScreenList.remove(food)

        Food.timerFired(app)
        

        app.count0= (1 + app.count0) % len(app.image0)
        app.count1= (1 + app.count1) % len(app.image1)
        app.count2= (1 + app.count2) % len(app.image2)
        app.count3= (1 + app.count3) % len(app.image3)
        global pitchChunk
        
        if pitchChunk[-1] != 0:
           
        
            cy = pitchChunk[-1]
            if cy<180:
                bird.targetRrail=14
            elif cy>430:
                bird.targetRrail=1
            else:
                bird.targetRrail=int(14-(((cy-180)/(app.height/14))+1))
            
            
            if len(pitchChunk)>10:
                pitchChunk = pitchChunk[-9:]

        try:
            
            audiobuffer = stream.read(buffer_size,exception_on_overflow = False)
            signal = np.fromstring(audiobuffer, dtype=np.float32)

            pitch = pitch_o(signal)[0]

            #only touch here
            magnitude = statistics.mean(abs(signal))*100
            # magChunk.append(magnitude)
            
            # if len(magChunk) == 20:
            #     magVals.append(int(statistics.mean(magChunk)))
            #     magChunk = []
            #     #print(magVals[-1],pitchVal)

            
            # minP = 40
            # maxP = 80
            
            # if magnitude>4:
            #     if pitchVal<minP:
            #         pitchVal = max(minP,pitchVal)
            #     if pitchVal>maxP:
            #         pitchVal = min(maxP,pitchVal)
            #     pitchVal = round(((pitchVal-minP)/(maxP-minP))*6)
            #     if pitchChunk[-1]!=pitchVal:
            #         pitchChunk.append(pitchVal)
            #

            #print(magnitude)
            pitchVal = pitch
            if magnitude<=0.7:
                app.open=False
            if magnitude>0.7:
                app.open=True

                if 0<=pitchVal<100:
                    if pitchVal>50:
                        pitchVal-=50
                    pitchVal*=25
                    pitchVal = min(pitchVal,450)
                    pitchVal = max(30,int(pitchVal))
                    distance = max(1,abs(pitchChunk[-1]-pitchVal)//10)
                    if pitchVal!=0:
                        if pitchChunk[-1]>pitchVal:
                            pitchChunk.extend(list(range(pitchVal,pitchChunk[-1],distance)))
                        else:
                            pitchChunk.extend(list(range(pitchVal,pitchChunk[-1],-distance)))
        
                print(pitchChunk[-1],Bird.rail)
                
            
            # if len(pitchChunk) == 5:
            #     pitchVals.append(int(statistics.mean(pitchChunk)))
            #     pitchChunk = []
            #     print(pitchVals[-1])
            
            #print("{} / {}".format(pitch,confidence))

            if outputsink:
                outputsink(signal, len(signal))

            if record_duration:
                total_frames += len(signal)
                if record_duration * samplerate < total_frames:
                    return
        except KeyboardInterrupt:
            print("*** Ctrl+C pressed, exiting")
            return

def distance(l1,l2,c1,c2):

    return math.sqrt((l1-c1)**2+(l2-c2)**2)

  
def eat(app):
    
    birdx=app.width/7-90
    birdy=app.cy
    if Food.onScreenList!=[]:
        for each in Food.onScreenList:
            x0,y0,x1,y1=each.parameter

             
            if abs(birdx-x0)<50:
                if abs(birdy-y1)<50:
                    if app.open==True:
                        Food.onScreenList.remove(each)
                    
                
                
def drawTweater(app,canvas):
    cx=app.Introx
    cy=2*app.height/5
    canvas.create_image(cx,cy,image=ImageTk.PhotoImage(app.tweater1))
    

def drawPause(app,canvas):
    cx=app.pausex
    cy=4*app.height/5
    canvas.create_image(cx,cy,image=ImageTk.PhotoImage(app.pa))

def drawblack(app,canvas):
    cx=app.width/2
    cy=4*app.height/5
    canvas.create_rectangle(cx-50,cy-60,cx+50,cy+60,fill="black")

    
def drawBackgroud(app,canvas):
    cx=app.width/2
    cy=app.height/2
    canvas.create_image(400,250,image=ImageTk.PhotoImage(app.images))          
def drawBird(app,canvas):
    rail=Bird.rail
    cx=app.width/7
    cy=app.cy#-app.height/14 so that it is in the center
    
    r=30
    photoImage0 = app.image0[app.count0]
    photoImage1 = app.image1[app.count1]
    if app.open==False and app.play==True:
        canvas.create_image(cx, cy, image=photoImage0)
        

    elif app.open==True and app.play==True:
        cy=app.cy
        canvas.create_image(cx, cy, image=photoImage1)
        

def drawCloud(app,canvas):
    if Cloud.onScreenList!=[]:
        for each in Cloud.onScreenList:
            cx,cy=each.parameter
            image=app.cloudImage[each.cloudType]
            canvas.create_image(cx,cy,image=ImageTk.PhotoImage(image))
            
            
        
    
def drawFood(app,canvas):
    if Food.onScreenList!=[]:
        for each in Food.onScreenList:
            x0,y0,x1,y1=each.parameter
            cx=((x1-x0)/2+x1)
            cy=((y1-y0)/2+y1)
            photoImage2 = app.image2[app.count2]
            photoImage3 = app.image3[app.count3]
            k=random.randint(0,1)
            if k==0:
                canvas.create_image(cx,cy-20,image=photoImage2)
                
            elif k==1:
                canvas.create_image(cx,cy-20,image=photoImage3)
                                                    

    
def drawLine(app,canvas):
    for i in range(7):
        canvas.create_rectangle(0,app.height*(i/7),app.width,app.height*((i+1)/7),
                                fill="white",outline="black")

def upCGen(app):

    row=random.randint(0,6)
    timeDelay=random.randint(20,40)
    parameter=[app.width,(row-1)*(app.height/7),app.width+77,
               (row-1)*(app.height/7)+88]
    
    return Food(parameter,row,timeDelay)



def Gen(app):
    L=[]
    for i in range(25):
        stuff=upCGen(app)
        L.append(stuff)
        
    return L

def CloudGen(app):
    cloudType=random.randint(0,3)
    cx=app.width+200
    cy=random.randint(50,400)
    parameter=[cx,cy]
    timerDelay=random.randint(300,400)
    return Cloud(parameter,cloudType,timerDelay)
def CloudListGen(app):
    L=[]
    for i in range(75):
        cloud=CloudGen(app)
        L.append(cloud)
    return L
    
runApp(width=800,height=500)
print("*** done recording")
stream.stop_stream()
stream.close()
p.terminate()

############
# end screen
############


    

