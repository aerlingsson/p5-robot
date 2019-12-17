from ev3dev2 import *
from ev3dev2.motor import LargeMotor, MediumMotor, MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
import math
# https://education.lego.com/en-us/products/lego-mindstorms-education-ev3-large-servo-motor-by-lego-education/45502


class Car:
    def __init__(self):
        self.current_pos = 4  # 0-3 = Left, 4 = center, 5-8 = Right

        try:
            self.turner = MediumMotor(OUTPUT_C)
            self.driver = MoveTank(OUTPUT_B, OUTPUT_D)
        except DeviceNotFound:
            print("No connected motors")

    def take_action(self, cmd):
        try:
            position, speed = cmd.split("_")
            position, speed = int(position), int(speed)

            self.turn(position)
            self.drive(speed)

        except ValueError:
            print("Wrong input format")

    # Turn specific amount of degrees
    def turn(self, pos):
        if pos == self.current_pos or pos < 0 or pos > 8:
            return

        degrees = 15
        speed = 20
        turns = abs(pos - self.current_pos)

        if pos - self.current_pos > 0:  # If turning right, then minus degrees
            degrees = -1 * degrees

        for _ in range(turns):
            self.turner.on_for_degrees(speed, degrees, block=False)

        self.current_pos = pos

    def drive(self, speed):
        try:
            self.driver.on(speed, speed)
        except AssertionError:
            print("If this is printed you can kill me")



