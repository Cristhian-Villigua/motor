#!/usr/bin/env python3
# =======================================
# Raspberry Pi 3B+ + L298N
# Prueba de motor DC
# Gira 15s en un sentido, se detiene,
# gira 15s en el otro sentido, y repite
# =======================================

import RPi.GPIO as GPIO
import time

# -------- Pines del L298N (numeración BCM) --------
IN1 = 13
IN2 = 19
ENA = 26

# -------- Configuración --------
velocidad = 80      # 0-100 (duty cycle en %)
pwmFreq = 1000       # Frecuencia del PWM en Hz

# -------- Tiempos --------
tiempoGiro = 15      # segundos
tiempoPausa = 1      # segundos

# -------- Setup GPIO --------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pwm = GPIO.PWM(ENA, pwmFreq)
pwm.start(0)


def detener_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)


def girar_adelante():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(velocidad)


def girar_atras():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(velocidad)


try:
    detener_motor()
    print("Prueba de motor DC iniciada...")

    while True:
        print("Girando ADELANTE...")
        girar_adelante()
        time.sleep(tiempoGiro)

        print("Deteniendo motor...")
        detener_motor()
        time.sleep(tiempoPausa)

        print("Girando ATRAS...")
        girar_atras()
        time.sleep(tiempoGiro)

        print("Deteniendo motor...")
        detener_motor()
        time.sleep(tiempoPausa)

except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario.")

finally:
    detener_motor()
    pwm.stop()
    GPIO.cleanup()
    print("GPIO liberado correctamente.")