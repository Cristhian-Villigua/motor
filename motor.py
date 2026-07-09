import RPi.GPIO as GPIO
import time

IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21

GPIO.setmode(GPIO.BCM)

for pin in (IN1, IN2, IN3, IN4):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

sequence = [
    [1,0,1,0],
    [0,1,1,0],
    [0,1,0,1],
    [1,0,0,1]
]

def step_backward(delay):
    for step in reversed(sequence):
        GPIO.output(IN1, step[0])
        GPIO.output(IN2, step[1])
        GPIO.output(IN3, step[2])
        GPIO.output(IN4, step[3])
        time.sleep(delay)

try:
    while True:
        step_backward(0.005)  # gira en sentido antihorario continuamente

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()