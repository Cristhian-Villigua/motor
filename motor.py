"""
Prueba simple del motor: gira SOLO en sentido horario durante N segundos.
No depende de stepper_belt.py ni modifica ningún flujo existente.
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
        def setmode(mode): pass
        @staticmethod
        def setup(pin, mode): pass
        @staticmethod
        def output(pin, val): pass

# Secuencia de 4 pasos completos para L298N (sentido horario)
STEP_SEQUENCE = [
    (1, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 1, 0, 1),
    (1, 0, 0, 1),
]

STEP_DELAY = 0.003
BELT_IN_PINS = [5, 6, 13, 19]

DURATION_S = 15.0  # tiempo de la prueba


def setup_pins(pins):
    if IS_RPI:
        GPIO.setmode(GPIO.BCM)
    for p in pins:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)


def set_step(pins, step):
    for pin, val in zip(pins, step):
        GPIO.output(pin, GPIO.HIGH if val else GPIO.LOW)


def run_clockwise(pins, duration_s):
    print(f"🧪 Girando en sentido horario durante {duration_s}s...")
    start = time.time()
    i = 0
    while (time.time() - start) < duration_s:
        step = STEP_SEQUENCE[i % len(STEP_SEQUENCE)]
        set_step(pins, step)
        time.sleep(STEP_DELAY)
        i += 1
    # Apagar bobinas al terminar
    set_step(pins, (0, 0, 0, 0))
    print("✅ Prueba finalizada.")


if __name__ == "__main__":
    setup_pins(BELT_IN_PINS)
    run_clockwise(BELT_IN_PINS, DURATION_S)