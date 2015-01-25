# -*- coding: utf-8 -*-
################################################################################
##Author:        Carlos Asmat
##Creation Date: 07/07/09
##Title:         Pololu Protocol Library
##Description:   Set of functions allowing the communication with
##               Pololu devices using the Pololu protocol.
##
##Copyright: Carlos Asmat, 2009
##License:
##      This program is free software: you can redistribute it and/or modify
##      it under the terms of the GNU General Public License as published by
##      the Free Software Foundation, either version 3 of the License, or
##      (at your option) any later version.
##
##      This program is distributed in the hope that it will be useful,
##      but WITHOUT ANY WARRANTY; without even the implied warranty of
##      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##      GNU General Public License for more details.
##
##      You should have received a copy of the GNU General Public License
##      along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##Description:
##      This is a small library with functions that allow to instantiate
##      and control Pololu motor controllers using the Pololu protocol.
##
################################################################################

#Defining values
start_byte = 0x80

def send_command(port, dev_id, command, num, data):
    """Sends a two-byte command using the Pololu protocol."""
    d = int(data)
    port.write(chr(start_byte)+chr(dev_id)+chr(command)+chr(num)+chr((d-(d&127))/128)+chr(d&127))

def send_command_single(port, dev_id, command, num, data):
    """Sends a one-byte command using the Pololu protocol."""
    port.write(chr(start_byte)+chr(dev_id)+chr(command)+chr(num)+chr(int(data)))

class Servo:
    """Servo motor object to be use with the Micro serial servo controller. It can be instantiated in order
    to control servos individually by setting position and speed."""
    def __init__(self, serialPort, servo_number = 0, min_rotation = 500, max_rotation = 5500):
        """Initialize a servo controller object by assigning a serial port,
        a device number (the number of the first servo), a max and min
        rotation values corresponding to the 0 deg ans 180 deg positions respectively."""
        self.port = serialPort
        self.servo_num = servo_number
        self.max_val = max_rotation % 5501
        self.min_val = min_rotation % 5501
        self.last_pos = 0

    __dev_id = 0x01

    def __compute_data(self, angle):
        angle = abs(angle) % 181 #keep the angle value in a safe range
        return self.min_val + angle * ((self.max_val - self.min_val)/180.0)

    def set_pos(self, pos = 90):
        data = self.__compute_data(pos)
        send_command(self.port, self.__dev_id, 0x04, self.servo_num, data)
        print("send_command(%s, %s, 0x04, %s, %s)" % (self.port, self.__dev_id, self.servo_num, data))
        self.last_pos = pos 

    def set_neutral(self, pos = 90):
        data = self.__compute_data(pos)
        send_command(self.port, self.__dev_id, 0x05, self.servo_num, data)
        self.last_pos = pos 

    def set_speed(self, speed = 127):
        send_command_single(self.port, self.__dev_id, 0x01, self.servo_num, speed)
    
    def set_parameters(self, on = False, dir_up = True, motion_range = 15):
        """Sets the parameters for a servo motor"""
        motion_range = abs(motion_range) % 32
        if on:
            on_byte = 0x40
        else:
            on_byte = 0x00

        if dir_up:
            dir_byte = 0x20
        else: 
            dir_byte = 0x00

        data = 0x00 | on_byte | dir_byte | motion_range
        send_command_single(self.port, self.__dev_id, 0x01, self.servo_num, data)
    
    def get_pos():
        return last_pos
