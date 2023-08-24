import RPi.GPIO as GPIO
import time
import subprocess

# Set up GPIO mode and pin
GPIO.setmode(GPIO.BCM)
SENSOR_PIN = 17
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables for tracking the script state
running = False
process = None

try:
    while True:
        # Read sensor input
        input_state = GPIO.input(SENSOR_PIN)

        if input_state == GPIO.LOW:
            if not running:
                print("Starting script...")
                process = subprocess.Popen(["python", "your_script.py"])
                running = True
            else:
                print("Stopping script...")
                process.terminate()
                running = False
        
        time.sleep(0.2)

finally:
    GPIO.cleanup()