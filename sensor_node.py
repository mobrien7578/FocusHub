from sense_hat import SenseHat
import time

sense = SenseHat()

while True:
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()

    print(f"Temperature: {temperature:.1f}°C")
    print(f"Humidity: {humidity:.1f}%")
    print("-------------------")

    time.sleep(5)
