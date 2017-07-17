#!/usr/bin/env python

import os
import RPi.GPIO as gpio
import time

LED_PIN = 12

FAN_MAX_TEMP = 70.0
FAN_MIN_TEMP = 45.0

FAN_MAX_POWER = 100.0
FAN_MIN_POWER = 30.0

def get_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    res = res.replace('temp=','').replace("'C\n",'')
    return float(res)

def calculate_linear_function_variables(y1, y2, x1, x2):
    b = (y2 - y1) / (-x1 + x2) 
    a = -x1 * ((y2 -y1) / (-x1 + x2)) + y1

    return a, b

def calculate_fan_power(a, b, current_cpu_temp):
    if current_cpu_temp >= FAN_MIN_TEMP:
        return a + b * current_cpu_temp
    else:
        return 0

def main():
    a, b = calculate_linear_function_variables(FAN_MIN_POWER, FAN_MAX_POWER, \
        FAN_MIN_TEMP, FAN_MAX_TEMP)
    increment = calculate_increment(FAN_MAX_POWER, FAN_MIN_POWER, \
        FAN_MAX_TEMP, FAN_MIN_TEMP)

    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(LED_PIN, gpio.OUT)
    fan_pwd = gpio.PWM(LED_PIN, 50)

    while(True):
        cpu_temp = get_cpu_temperature()
        fan_power = calculate_fan_power(a, b, cpu_temp)
        if fan_power != 0:
            fan_pwd.start(fan_power)
        else:
            fan_pwd.stop()
        
        time.sleep(15)

if __name__ == '__main__':
    main()
