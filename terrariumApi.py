from fastapi import FastAPI
import board
import time
import adafruit_dht
import subprocess
import random
import base64
import os

app = FastAPI()

# init DHT22 Temp/Hum Sensor on GPIO pin 4
dht_device = adafruit_dht.DHT22(board.D4)




def read_sensor():
	try:
		#read temp and hum
		temperature_celsius = dht_device.temperature
		humidity = dht_device.humidity
		
		#convert temp to F
		temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32
		
		# return data as dict
		if temperature_celsius is not None and humidity is not None:
			return {"temperature_celsius": temperature_celsius, "temperature_fahrenheit": temperature_fahrenheit, "humidity": humidity}
		else:
			return {"error": "Failed to read from DHT sensor"}
	except Exception as e:
		return {"error": str(e)}


@app.get("/")
def read_root():
	return {"message": "Welcome to the Terrarium API!"}
	
@app.get("/sensor")
def get_sensor_data():
	# process or save data here
	data = read_sensor()
	return data
	
@app.get("/camera")
def camera_capture():
	random_number = random.randint(1000,9999)
	image_path = f"/home/juan-pi/Desktop/img_{random_number}.jpg"
	subprocess.run(["libcamera-still",
					"--nopreview",
					"--datetime",
					"--quality", "90",
					"-o", image_path])
					
	while not os.path.exists(image_path):
		time.sleep(0.1)
		if(os.path.exists(image_path)):
			continue
					
	with open(image_path, "rb") as image_file:
		image_data = base64.b64encode(image_file.read()).decode("utf-8")
	
	return {"image_data": image_data}

