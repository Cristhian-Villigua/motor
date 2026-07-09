from machine import Pin
from time import sleep_ms

# ==========================
# Pines del L298N
# ==========================
BELT_IN_PINS = [5, 6, 13, 19]

IN1 = Pin(BELT_IN_PINS[0], Pin.OUT)
IN2 = Pin(BELT_IN_PINS[1], Pin.OUT)
IN3 = Pin(BELT_IN_PINS[2], Pin.OUT)
IN4 = Pin(BELT_IN_PINS[3], Pin.OUT)

# ==========================
# Secuencia Full Step
# ==========================
SECUENCIA = (
    (1, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 1),
)

paso = 0

while True:
    IN1.value(SECUENCIA[paso][0])
    IN2.value(SECUENCIA[paso][1])
    IN3.value(SECUENCIA[paso][2])
    IN4.value(SECUENCIA[paso][3])

    paso = (paso + 1) % 4
    sleep_ms(3)