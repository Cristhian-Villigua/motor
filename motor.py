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

def step_forward(steps, delay):
    for _ in range(steps):
        for step in sequence:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(delay)

def step_backward(steps, delay):
    for _ in range(steps):
        for step in reversed(sequence):
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(delay)

try:
    while True:
        step_forward(200, 0.005)
        time.sleep(1)
        step_backward(200, 0.005)
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()