#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.motor import MediumMotor, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import os
import sys
import time

# state constants
ON = True
OFF = False


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)

def turn(degrees, speed, motor):
    motor.on_for_degrees(SpeedPercent(10), degrees)

def resetToStartTurn(degrees, speed, motor):
    motor.on_for_degrees(SpeedPercent(10), -(degrees))

def driveUntilStop(tank_drive, speed):
    tank_drive.on(SpeedPercent(speed), SpeedPercent(speed))



def main(): #This main is just a test for the interface functions right now
    '''The main function of our program'''
#drive motors
tank_drive = MoveTank(OUTPUT_D, OUTPUT_B)
#turning motor
m = MediumMotor(OUTPUT_C)

#command to run
decision = 1
#speed percent
speed = 0
#degrees to turn
degrees = 0

while True:

    print(decision)
    print(speed)
    print(degrees)
    if decision == 1:
        degrees = -30
        turn(degrees, speed, m)
        #resetToStartTurn(degrees, speed, m)
        decision = 3
        time.sleep(2)

    if decision == 2:


        degrees = 30
        turn(degrees, speed, m)
        resetToStartTurn(degrees, speed, m)
        decision = 3
        time.sleep(2)


    if decision == 3:
        #speed += 5
        #if speed >= 25:
         #   decision = 4
        speed = 10
        driveUntilStop(tank_drive, speed)
        decision = 1
        time.sleep(2)

    if decision == 4:
        speed = 0
        driveUntilStop(tank_drive, speed)
        m.stop










if __name__ == '__main__':
    main()
