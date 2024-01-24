# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       april                                                        #
# 	Created:      1/21/2024, 11:20:37 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Define the states
IDLE = 0
DRIVING = 1
LIFTING = 2

# Robot configuration code
left_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)

## Reverse is forward
## True should reverse the direction of the motor
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
UltraS = Sonar(brain.three_wire_port.e)

## Set the velocities for the motor
left_motor.set_velocity(50, RPM)
right_motor.set_velocity(50, RPM)

## Create motor group to get around the blocking code
wheelG = MotorGroup(left_motor, right_motor)

# Define the current state
current_state = IDLE

# set the position of the arm
# Be careful the first time you run the program because the position of the arm will be set as the home position
startposition = 0
arm_motor.set_position(startposition, DEGREES)

# Event handeler for the button press
def handleButton():
    global current_state
    ## Return the arm to the start position to run again
    if(arm_motor.position != 0 and current_state == IDLE):
        arm_motor.spin_to_position(startposition, DEGREES, 30, RPM)

    if(current_state == IDLE):
        print('IDLE -> DRIVING')
        current_state = DRIVING
        wheelG.spin(FORWARD)
    
    elif(current_state == DRIVING):
        print('DRIVING -> IDLE \n')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

 

buttonD = Bumper(brain.three_wire_port.g)

buttonD.pressed(handleButton)

def MoveArm():
    global current_state
    ## Get current distance
    distance = UltraS.distance(MM)
    brain.screen.print_at("Distance(MM): ", distance, x = 50, y = 50)

    if(distance < 300):

        ## Stop the motors
        left_motor.stop()
        right_motor.stop()

        ## Have to change the state back to IDLE otherwise it thinks it is still DRIVING and it will keep moving the arm
        current_state = IDLE
        arm_motor.spin_to_position(500, DEGREES, 30, RPM)

        ## Wait then continue
        wait(500, MSEC)

        ## Move forward to catch the handle of the bucket
        wheelG.spin_for(FORWARD, 3, TURNS, 30, RPM)

        ## 0 is the start position
        arm_motor.spin_to_position(375, DEGREES, 30, RPM)
        brain.screen.print_at("Torque: ", arm_motor.torque(), x = 50, y = 75)

## Run at least once to get rid of the zero
distance = UltraS.distance(MM)

while True:
    ## The entire time the robot is in the DRIVING state call MoveArm 
    if(current_state == DRIVING):
        MoveArm()