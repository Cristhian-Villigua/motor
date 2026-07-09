"""
Prueba simple del motor: gira continuamente en sentido horario.
Detener con Ctrl+C.
"""

import time

try:
    import RPi.GPIO as GPIO
    IS_RPI = True
except (ImportError, RuntimeError):
    IS_RPI = False
    print("⚠️ RPi.GPIO no disponible (modo simulado)")

    class GPIO:
        BCM = "BCM"
        OUT = "OUT"
        LOW = 0
        HIGH = 1

        @staticmethod
        def setmode(mode):
            pass

        @staticmethod
        def setup(pin, mode):
            pass

        @staticmethod
        def output(pin, val):
            pass

        @staticmethod
        def cleanup():
            pass


# ==========================
# Pines del L298N
# ==========================
BELT_IN_PINS = [5, 6, 13, 19]

# ==========================
# Secuencia Full Step
# ==========================
STEP_SEQUENCE = [
    (1, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 1),
]

STEP_DELAY = 0.003  # 3 ms


def setup_pins(pins):
    GPIO.setmode(GPIO.BCM)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


def set_step(pins, step):
    for pin, value in zip(pins, step):
        GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)


def motor_clockwise():
    print("▶ Motor girando continuamente... (Ctrl+C para detener)")

    paso = 0

    try:
        while True:
            set_step(BELT_IN_PINS, STEP_SEQUENCE[paso])
            paso = (paso + 1) % 4
            time.sleep(STEP_DELAY)

    except KeyboardInterrupt:
        print("\nDeteniendo motor...")

    finally:
        set_step(BELT_IN_PINS, (0, 0, 0, 0))
        GPIO.cleanup()


if __name__ == "__main__":
    setup_pins(BELT_IN_PINS)
    motor_clockwise()