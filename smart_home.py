import RPi.GPIO as GPIO
import LCD1602 as LCD
import time
import urllib.request
from keypadfunc import keypad as KP
from RFIDTest import ser_read as rfid
import DHT11
import PCF8591 as ADC
from flask import Flask
from flask import send_file
from picamera import PiCamera
from datetime import datetime
LCD.init(0x27,1)
ADC.setup(0x48)

#----------------------------------------------
#THINGSPEAK SETUP AND VARIABLES


API_KEY = "1K4YATUCW5H3V1NG"
CH_ID = 2099336
Field_No1 = 1
Field_No2 = 2
numberofreadings = 3
elementnumber = 2
values1=[]
values2=[]

#----------------------------------------------
#SETUPS:
GPIO.setmode(GPIO.BCM)

#initialize camera
camera = PiCamera()  
camera.resolution = (640,480)
#Setting the pin numbers 
        #blPin=18
grPin=13
rdPin=6
PbPin=12
ECHO=16
buzzPin=5
motion=4
TRIG=17
#Setting up the TRIG for the ultrasonic snesor
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
#Setting up the buzzer
GPIO.setup(buzzPin, GPIO.OUT)
Buzz = GPIO.PWM(buzzPin, 0.5)
Buzz.start(50)
#Setting the LED's as outputs
GPIO.setup(grPin, GPIO.OUT)
#GPIO.setup(blPin, GPIO.OUT)
GPIO.setup(rdPin, GPIO.OUT)
GPIO.output(grPin, GPIO.LOW)
#GPIO.output(blPin, GPIO.LOW)
GPIO.output(rdPin, GPIO.LOW)
#Setting the Push Button as an input
GPIO.setup(PbPin, GPIO.IN)
#Setting the Motion Sensor as an input
GPIO.setup(motion, GPIO.IN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motion, GPIO.IN, pull_up_down=GPIO.PUD_UP)



app = Flask(__name__)
#----------------------------------------------
#GLOBAL VARIABLES

flag=0
checkaccess=0
mistake =0

SPO2QUALITY=0
Humidtycheck=0
#----------------------------------------------
#FUNCTIONS:

#function that converts adc units into a temperature value
def readTemp():
        ADC1_units= ADC.read(1)
        temp = ADC1_units*(15/255)+15
        return temp

#funciton that writes adc unites to the LED   
def changeLED():
        ADC1_units= ADC.read(2)
        ADC.write(ADC1_units)

#function that converts adc units read from channel 2 into an SPO2 value
def checkAirquality():
        ADC1_units= ADC.read(2)
        SPO2= ADC1_units*(19.6/100)+50
        return SPO2

#this function plays a harmonic sound using various frequencies through the buzzer
def welcome():
  print("Welcome Home!\n")
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(329.63)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(329.63)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(311.13)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(329.63)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(311.13)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(329.63)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(246.94)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(293.66)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(261.63)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(220)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(130.81)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(164.81)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(220)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(246.94)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(164.81)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(261.63)
  
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.LOW)
  Buzz.ChangeFrequency(246.94)
  time.sleep(0.35)
  GPIO.output(grPin, GPIO.HIGH)
  Buzz.ChangeFrequency(220)
  time.sleep(1)
  Buzz.ChangeFrequency(1)

#function that plays an alarm sound through the buzzer
def alarmSound():

  GPIO.output(rdPin, GPIO.LOW)
  Buzz.ChangeFrequency(1500)
  time.sleep(1)
  GPIO.output(rdPin, GPIO.HIGH)
  Buzz.ChangeFrequency(2500)
  time.sleep(1)
  GPIO.output(rdPin, GPIO.LOW)
  Buzz.ChangeFrequency(1500)
  time.sleep(1)
  GPIO.output(rdPin, GPIO.LOW)
  Buzz.ChangeFrequency(2500)
  time.sleep(1)
  GPIO.output(rdPin, GPIO.HIGH)
  Buzz.ChangeFrequency(1500)
  
  time.sleep(1)
  Buzz.ChangeFrequency(1)
  
#function that makes a doorbell sound through the buzzer
def doorBell(delay,freq1,freq2):
  Buzz.ChangeFrequency(freq1)
  time.sleep(delay)
  Buzz.ChangeFrequency(freq2)
  time.sleep(delay)
  Buzz.ChangeFrequency(1)

#action function that is called once a falling edge is detected from the motion sensor with a bouncetime of 2000
def action(self):
  global flag
  if(flag==1):
     print("Movement outside the house was detected... Call the police!")
     GPIO.output(rdPin, GPIO.HIGH)
     flag=0
     if(__name__=='__main__'):
        app.run(host='0.0.0.0', port=5080)

#Adding the interrupt        
GPIO.add_event_detect(motion, GPIO.FALLING, callback=action, bouncetime=2000)

#funciton that returns the distance from the ultrasound sensor  
def distance():
    GPIO.output(TRIG, GPIO.LOW) 
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0:
        a = 0                                          
    time1 = time.time()                        
    while GPIO.input(ECHO) == 1:
        a = 0                                                  
    time2 = time.time()                        
    duration = time2 - time1
    return duration*1000000/58


#funciton that reads temperature and humidity value using the DHT11 sensor, uploads them to thingspeak and reads htem to detect certain air qualities and humidity values
def checktemp():
        global SPO2QUALITY
        global Humidtycheck
        result = DHT11.readDht11(27)
        
        if result:
                
            humidity, temperature = result
            spo2percent=checkAirquality()
            LCD.clear()
            LCD.write(0,0, 'SPO2:{}%'.format(checkAirquality()))
            LCD.write(0,1, 'T:{}C, H:{}% '.format(temperature, humidity))

            #to write the humidity, temperature and oxygen quality into thingspeak:
            x=urllib.request.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}".format(API_KEY, spo2percent, humidity, temperature))

            #to read the humidity, temperature and oxygen quality from thingspeak:
            Y=urllib.request.urlopen("https://api.thingspeak.com/channels/{}/fields/{}.csv?results={}".format(CH_ID, Field_No1, numberofreadings))
            data1=Y.read().decode('ascii')
            data1=",".join(data1.split("\n"))
            #append the values into an array/list:
            for i in range(5, numberofreadings*3+3, 3):
                values1.append(data1.split(",")[i])
            arrlen1= len(values1)
            #save the last value in the list/array into a variable
            Yelement1 = float(values1[arrlen1-1])
            print("SPO2:{}%".format(Yelement1))
            #check and compare the last instance of air quality value measured
            if(Yelement1 <80): #Poor air quality
             SPO2QUALITY=1
             if(Yelement1 <70): #Life threatening air quality
              SPO2QUALITY=2
            
            Z=urllib.request.urlopen("https://api.thingspeak.com/channels/{}/fields/{}.csv?results={}".format(CH_ID, Field_No2, numberofreadings))
            data2=Z.read().decode('ascii')
            data2=",".join(data2.split("\n"))
            for j in range(5, numberofreadings*3+3, 3):
                values2.append(data2.split(",")[j])
            #save last instance of humidity value
            arrlen2= len(values2)
            Zelement1 = float(values2[arrlen2-1])
            ##Zelement2 = float(values2[arrlen2-1])
            print("Humidity:{}%".format(Zelement1))
            ##print(Zelement2)
            #if humidity value is higher than 65% then its too hot
            if(Zelement1 >65):
                    Humidtycheck=1
        
#function that returns special characters from the keypad
def shift():
  numnp, nump = KP()
  GPIO.output(grPin,GPIO.HIGH)
  time.sleep(0.3)
  GPIO.output(grPin,GPIO.LOW)
  
  if(GPIO.input(PbPin)==1):
    return nump
  else:
    return numnp

#function that flashes an LED on and OFF
def flash(inp):
  for i in range(3):
    GPIO.output(inp, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(inp, GPIO.LOW)
    time.sleep(0.5)

  GPIO.output(inp,GPIO.HIGH)
#----------------------------------------------
#FLASK

#index route for flask server
@app.route('/')
def index():
  return '**Welcome to your personalised Home Security and Automation System**'

#static route to display the indoor climate on the flask server webpage
@app.route('/View/IndoorClimate')
def indoor_climate():
  result = DHT11.readDht11(27)
  if result:
    humidity, temperature = result
    LCD.clear()
    LCD.write(0,0, 'Humidity:{}%'.format(humidity))
    LCD.write(0,1, 'Temperature: {}C'.format(temperature))
    buf = "Humidity:{}%,  Temperature: {}C".format(humidity, temperature)
    return buf

#static route to display the Oxygen Quality on the flask server webpage
@app.route('/View/SPO2')
def checkSPO2():
  SPO2 = checkAirquality()
  LCD.clear()
  LCD.write(0,0, 'Air Quality:')
  LCD.write(0,1, 'SPO2: {}%'.format(SPO2))
  buf = "Air Quality: SPO2 = {}%".format(SPO2)
  return buf
  
  
#static route to display the AC temperature on the flask server webpage
@app.route('/AC/CheckTemp')
def check_temp():
  temp = readTemp()
  LCD.clear()
  LCD.write(0,0, 'Current Temp:')
  LCD.write(0,1, '%2.1f Celsius'%temp)
  buf = "Current Temperature %2.1f Celsius"%temp
  return buf

#Dyanmic route to change the AC temperature from the flask server webpage
@app.route('/AC/ChangeTemp/<temp>')
def change_airconditioning(temp):
  LCD.clear()
  LCD.write(0,0, 'Set Temperature:')
  LCD.write(0,1, '{}C'.format(temp))
  buf = "Setting Airconditioning Temperature to: {}C".format(temp)
  return buf

#Dynamic route to change the LED color from the flask server webpage
@app.route('/Lightswitch/<color>')
def light_switch(color):
  if(color=="Green"):
    GPIO.output(grPin,GPIO.HIGH)
    GPIO.output(rdPin,GPIO.LOW)

    LCD.clear()
    LCD.write(0,0, 'Turning On:')
    LCD.write(0,1, 'Green Lights')
    
    buf = "Turning on Green Lights"

  elif(color=="Red"):
    GPIO.output(rdPin,GPIO.HIGH)
    GPIO.output(grPin,GPIO.LOW)

    LCD.clear()
    LCD.write(0,0, 'Turning On:')
    LCD.write(0,1, 'Red Lights')
    
    buf = "Turning on Red Lights"

  else:
    buf = "Light color does not exist!"
          
  return buf

#Dynamic route to take an image or video from a request on the flask server webpage
@app.route('/DoorCam/<captureType>')
def door_cam(captureType):
  if(captureType.lower()=="picture"):

    photo_path = "/home/pi/Desktop/pic.jpg"
    t=datetime.now().isoformat()
    camera.annotate_text = "Door Cam: Pic taken at time %s" %(t)
    time.sleep(2)
    camera.capture(photo_path)
    response=send_file(photo_path, mimetype = "image/jpeg")
    return response

  elif(captureType.lower()=="video"):

    video_path = '/home/pi/Desktop/video.h264'
    camera.annotate_text = "Door Cam: Video recorded at time %s" %(t)
    camera.start_recording(video_path)
    time.sleep(8)
    camera.stop_recording
    response=send_file(video_path, mimetype = "=video/h.264")
    return response

  else:
    
    buf = "Security breach... Cam activated at %s" %(time.ctime())
    return buf

#Dynamic route to take an image or video from a request on the flask server webpage
@app.route('/BabyCam/<captureType>')
def babydoor_cam(captureType):
  if(captureType.lower()=="picture"):

    photo_path = "/home/pi/Desktop/pic.jpg"
    t=datetime.now().isoformat()
    camera.annotate_text = "Baby Cam: Pic taken at time %s" %(t)
    time.sleep(2)
    camera.capture(photo_path)
    response=send_file(photo_path, mimetype = "image/jpeg")
    return response

  elif(captureType.lower()=="video"):

    video_path = '/home/pi/Desktop/video.h264'
    camera.annotate_text = "Baby Cam: Video take record at time %s" %(t)
    camera.start_recording(video_path)
    time.sleep(10)
    camera.stop_recording
    response=send_file(video_path, mimetype = "=video/h.264")
    return response


    
    buf = "Baby's door sensor was tripped! %s" %(time.ctime())
    return buf



#----------------------------------------------
#MAIN



while(True):
  flag=0
  
  
  GPIO.output(buzzPin, GPIO.HIGH)
  GPIO.output(rdPin, GPIO.LOW)
  GPIO.output(grPin, GPIO.LOW)
  
  #MODE ACCESS CHECK
  while(True):
    #KEYPAD MODE
    LCD.clear()
    LCD.write(0,0, 'Choose access:')
    LCD.write(0,1, 'mode: K|R|G')
    accessmode = input("Welcome! Choose access mode: (Keypad[K] / RFID card[R]/ Guest[G])")
    if(accessmode.upper() == "KEYPAD" or accessmode.upper() == "K"):
      
      print("Enter your password:")
      while(True):
        LCD.clear()
        LCD.write(0,0, 'Keypad mode...')
        LCD.write(0,1, 'Enter pin:')
        
        keyp1 = shift()
        LCD.write(0,1, 'Enter pin:*')
        time.sleep(0.7)
        keyp2 = shift()
        LCD.write(0,1, 'Enter pin:**')
        time.sleep(0.7)
        keyp3 = shift()
        LCD.write(0,1, 'Enter pin:***')
        time.sleep(0.7)
        keyp4 = shift()
        LCD.write(0,1, 'Enter pin:****')
        time.sleep(0.7)
        
        #check if the values entered from the keypad match the correct password
        print(str(keyp1) + str(keyp2) + str(keyp3) + str(keyp4))
        if(((str(keyp1) + str(keyp2) + str(keyp3) + str(keyp4))==("1234"))):
          
          LCD.clear()
          LCD.write(0,0, 'Welcome Home!')
          LCD.write(0,1, '   :)   ')
          welcome()
           
          #this variable will allow the user to exit the authentication mode
          checkaccess=1
          break
        #if the number of mistakes are 3 then launch the flask and check door camera for security reasons
        elif(mistake==2):

          alarmSound()
          
          if(__name__=='__main__'):
            app.run(host='0.0.0.0', port=5080)
        #if its wrong pin entered then increment the number of total mistakes and give another attempt to the user         
        else:
          mistake = mistake +1
          print("Incorrect PIN... ("+ str(mistake)+"/3)")
          LCD.clear()
          LCD.write(0,0, 'Incorrect Pin!')
          LCD.write(0,1, 'Try Again ({}/3)'.format(mistake))
          time.sleep(2)
          
    #RFID MODE
    elif(accessmode.upper() == "RFID" or accessmode.upper() == "R" ):
      LCD.clear()
      LCD.write(0,0, 'RFID mode...')
      LCD.write(0,1, 'Swipe card:')
      print("Hold  the pushbutton to scan a RFID card")
      
      while(True):
        rfidInput = ""
        while (GPIO.input(PbPin)==0):
          time.sleep(0)
        time.sleep(1)
        rfidInput=rfid()
        if(rfidInput == "5400653CCF" or rfidInput == "5200129DAB" or rfidInput == "5300C81249"):
          checkaccess=1
          welcome()
          break
        else:
          print("Wrong keycard")
    #GUEST MODE    
    elif(accessmode.upper() == "GUEST" or accessmode.upper() == "G" ):
      LCD.clear()
      LCD.write(0,0, 'Guest mode...')
      LCD.write(0,1, 'Ring the doorbell:')
      print("Ring the doorbell... (Push button)")
      
      checked=0
      waitflag=0
      while(True):
        if(GPIO.input(PbPin)==1):
          checkaccess=1
          if(waitflag==0):
            waitflag=1
            print("Kindly wait for someone to open the door")
          doorBell(1, 2500, 1500)
        
        Buzz.ChangeFrequency(1)
        time.sleep(0.25)
        checked = checked+waitflag
        if(checked == 10):
          break
      LCD.clear()
      LCD.write(0,0, 'Welcome Home!')
      LCD.write(0,1, '   :)   ') 
        
    #checks for permission after the authentication process is complete
    if(checkaccess==1):
      break


    
    else:
      print("Incorrect access mode.. Try again!")

  #guests can't access the smart home automation system so they will be welcomed and exit this loop 
  if(accessmode.upper() == "G"):
    print("Welcome guest!")
    break
  
  
  print("Choose an option from the smart home interface: ")
  LCD.clear()
  LCD.write(0,0, 'Choose option:')
  LCD.write(0,1, '1|2|3|4|5|6')
  while(True):
    GPIO.output(rdPin, GPIO.LOW)
    #GPIO.output(blPin, GPIO.LOW)
    GPIO.output(grPin, GPIO.LOW)
    userinput=input("1. Check indoor climate\n2. Change AC temperature\n3. Modify indoor light intensity\n4. Activate Baby Room Sensor\n5. Leave the house\n6. Access Remote Control Through Flask\n")
    if(userinput == "1"):
      print("Checking indoor climate... use the Pushbutton to exit...")      
      while(GPIO.input(PbPin)==0):
              SPO2QUALITY=0
              Humidtycheck=0
              checktemp()
              if(SPO2QUALITY ==1):
                print("Poor air quality detected... Air Ventilation system activated!")
                ##break
              if(SPO2QUALITY ==2):
                print("Life threatening air quality detected... Calling paramdics!")
              if(Humidtycheck==1):
                print("High air humidity detected... Switching on Air Conditioning!")
              
    elif(userinput =="2"):
      print("Adjust the temperature... use the Pushbutton to exit...")
      while(GPIO.input(PbPin)==0):
        temperature=readTemp()
        LCD.clear()
        LCD.write(0,0, 'Temperature:')
        LCD.write(0,1, '%2.1f Celsius'%temperature)
        time.sleep(1)
    elif(userinput=="3"):
      print("Adjust the light intensity... use the Pushbutton to exit...")
      while(GPIO.input(PbPin)==0):
        LED=changeLED()
        LCD.clear()
        LCD.write(0,0, 'Changing LED')
        LCD.write(0,1, 'Intensity...')
        time.sleep(1)
        
                
    elif(userinput=="4"):
      LCD.clear()
      LCD.write(0,0, 'Baby Monitor:')
      LCD.write(0,1, 'Activated')
      print("Baby room sensor was activated! Press push button to disable the sensor")
      while(GPIO.input(PbPin)==0): ##Checking if baby is in the bed (door sensor)
                dist = distance()
                if(distance()<40):
                        print("Baby room sensor was tripped!")
                        Buzz.ChangeFrequency(500)
                        time.sleep(0.25)
                        Buzz.ChangeFrequency(750)
                        time.sleep(0.25)
                        Buzz.ChangeFrequency(1000)
                        time.sleep(0.25)
                        Buzz.ChangeFrequency(1250)
                        time.sleep(0.25)
                        Buzz.ChangeFrequency(1)
                        if(__name__=='__main__'):
                          app.run(host='0.0.0.0', port=5080)
    elif(userinput=="5"):
        LCD.clear()
        LCD.write(0,0, 'Safety mode..')
        LCD.write(0,1, 'Sensors activated!')
        flag=1
        print("Leaving the house.... Safety Mode has been activated! Press push button to exit Safety Mode")
        while(GPIO.input(PbPin)==0):
                a=0
        flag=0
        #print(dist)

    elif(userinput=="6"):
     LCD.clear()
     LCD.write(0,0, 'Remote mode:')
     LCD.write(0,1, '(Flask)')
            
     print("/DoorCam            -> Check Door Camera")

     print("/BabyCam            -> Check Baby Camera")
     print("/View/IndoorClimate -> Checks Indoor Climate")

     print("/View/SPO2          -> Check Oxygen Saturation")
     print("/AC/Checktemp       -> Check Temperature")

     print("/AC/ChangeTemp      -> Change AC Temperature")

     if(__name__=='__main__'):
                  app.run(host='0.0.0.0', port=5080)
                
print("\nPlease have a seat while super supreme pizza is being served for iftar")

                
#----------------------------------------------





  
