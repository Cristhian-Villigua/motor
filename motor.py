import RPi.GPIO as GPIO
import time

# Configurar el modo BCM (para usar los números de pin reales del chip)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ¡AQUÍ ESTÁ TU ACTUALIZACIÓN! 
# Pines GPIO conectados a IN1, IN2, IN3, IN4 respectivamente
pines_motor = [12, 16, 20, 21]

# Configurar todos los pines como salida y asegurar que inicien apagados
for pin in pines_motor:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Secuencia de "Paso Completo" (Full Step)
# Cada fila representa el estado de [IN1, IN2, IN3, IN4]
secuencia_pasos = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

def girar_motor(pasos, direccion_horaria=True, retardo=0.005):
    """
    Gira el motor usando la secuencia del puente H.
    """
    secuencia = secuencia_pasos if direccion_horaria else list(reversed(secuencia_pasos))
    
    print(f"Girando {pasos} ciclos...")
    
    for _ in range(pasos):
        for paso_actual in secuencia:
            # Asignar los valores a tus pines 12, 16, 20 y 21
            for pin in range(4):
                GPIO.output(pines_motor[pin], paso_actual[pin])
            time.sleep(retardo)
            
def apagar_bobinas():
    """Apaga todas las bobinas por seguridad (evita que el motor se queme)"""
    for pin in pines_motor:
        GPIO.output(pin, False)

try:
    print("Iniciando prueba con L298N (Pines 12, 16, 20, 21). Ctrl+C para detener.")
    
    # 50 bucles de 4 pasos = 200 pasos (1 revolución completa en un NEMA 17)
    pasos_por_revolucion = 50 
    
    # Girar en un sentido
    girar_motor(pasos_por_revolucion, direccion_horaria=True, retardo=0.005)
    
    # Pausa segura
    apagar_bobinas() 
    time.sleep(1)
    
    # Girar en sentido contrario
    girar_motor(pasos_por_revolucion, direccion_horaria=False, retardo=0.005)

    print("Prueba finalizada exitosamente.")

except KeyboardInterrupt:
    print("\nDetenido manualmente por el usuario.")

finally:
    # Siempre apagamos y limpiamos al final
    apagar_bobinas()
    GPIO.cleanup()
    print("Pines GPIO limpiados y listos.")