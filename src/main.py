#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()

def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

from vex import *

brain = Brain()
overide = False
brain.screen.draw_image_from_file("7187g.png", 0, 0)
startcheck = False
# Controler setup
c1 = Controller(PRIMARY) # Controller 1 setup (Primary is the argument)
c2 = Controller(PARTNER) # Controller 2 Does not have prioity

# Define motors by this order:  Port, Gear Ratio, Reversed y/n 
MR = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False) # Middle right
FR = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False) # Front right
BR = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False) # Back right
ML = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False) # Middle left
FL = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False) # Front left
BL = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False) # Back left

IN = Motor(Ports.PORT1, False) # Front intake
CL = Motor(Ports.PORT1, False) # Claw 
FBR = Motor(Ports.PORT1, False) # Four Bar Right Side
FBL = Motor(Ports.PORT1, False) # Four bar Left Side

leftvoltagecurve = 0 # This is here to adjust the speed of each side
rightvoltagecurve = 0 
# Creates the function to call drivetrain movement
def movement(leftspeed, rightspeed):
    #Left side
    FL.spin(REVERSE, leftspeed + leftvoltagecurve, VOLT)
    ML.spin(REVERSE, leftspeed + leftvoltagecurve, VOLT)
    BL.spin(REVERSE, leftspeed + leftvoltagecurve, VOLT)


    #Right side
    FR.spin(REVERSE, rightspeed + rightvoltagecurve, VOLT)
    MR.spin(REVERSE, rightspeed + rightvoltagecurve, VOLT)
    BR.spin(REVERSE, rightspeed + rightvoltagecurve, VOLT)
    
# Stop simpliy stops all drivetrain movement

def stopp():
    FR.stop()
    MR.stop()
    BR.stop()
    FL.stop()
    ML.stop()
    BL.stop()
#This is for coding dont acutally change it, this is to keep the same program instead of splitting
side = "Left"
#Left/Right
def autostuff():
    pass

# States the overide conditions on the controller
def overidecontrol():
    global overide
    if c2.buttonX.pressing():
        overide = True
        c1.screen.clear_row(3)
        c2.screen.clear_row(3)
        c1.screen.set_cursor(3, 1)
        c2.screen.set_cursor(3, 1)
        c1.screen.print("C2 control")
        c2.screen.print("C2 control")
    if c1.buttonX.pressing():
        overide = False
        c1.screen.clear_row(3)
        c2.screen.clear_row(3)
        c1.screen.set_cursor(3, 1)
        c2.screen.set_cursor(3, 1)
        c2.screen.print("C1 in control")
        c1.screen.print("C1 in control")
def controls():
    if c1.buttonL1.pressing():
        IN.spin(FORWARD, 5.5 , VOLT)
    elif c1.buttonL2.pressing():
        IN.spin(REVERSE, 5.5, VOLT)
    elif c1.buttonR1.pressing():
        FBR.spin(FORWARD , 13 , VOLT)
    elif c1.buttonR2.pressing():
        FBL.spin(REVERSE , 13 , VOLT)
    # Contoller two inputs
    if c2.buttonL1.pressing():
        IN.spin(FORWARD, 5.5 , VOLT)
    elif c2.buttonL2.pressing():
        IN.spin(REVERSE, 5.5, VOLT)
    elif c2.buttonR1.pressing():
        FBR.spin(FORWARD , 13 , VOLT)
    elif c2.buttonR2.pressing():
        FBL.spin(REVERSE , 13 , VOLT)
def autonomous():
    startcheck = True
    autostuff()
#BTW this is the stuff that happens during driver control
def user_control():
    # Makes sure velocityis maxed (We use voltage to curve instead of velocity percentage)
    MR.set_velocity(100, PERCENT)
    ML.set_velocity(100, PERCENT)
    FL.set_velocity(100, PERCENT)
    FR.set_velocity(100, PERCENT)
    BR.set_velocity(100, PERCENT)
    BL.set_velocity(100, PERCENT)
    startcheck = False 
    brain.screen.clear_screen()
    brain.screen.draw_image_from_file("7187g.png", 0, 0)
    while True:
        # Gives C1 Control unless a overide is set
        if overide == True:
            Lat = c2.axis1.position() / 100 * 12
            horizontal= c2.axis3.position() / 100 *12 
            Leftside = Lat + horizontal
            Rightside = Lat - horizontal
            movement(Leftside,Rightside)
        else:
            Lat = c1.axis1.position() / 100 * 12
            horizontal= c1.axis3.position() / 100 *12 
            Leftside = Lat + horizontal
            Rightside = Lat - horizontal
            movement(Leftside,Rightside)
        overidecontrol()

        wait(20, MSEC)

        


comp = Competition(user_control, autonomous)


