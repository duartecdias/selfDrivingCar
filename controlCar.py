import flask
import socketio
import eventlet
import tensorflow
import keras
import base64
import io
import PIL
import numpy as np
import cv2
import matplotlib
import imageio

print("TensorFlow version:", tensorflow.__version__)
print("Keras version:", keras.__version__)


webserver = socketio.Server()

app = flask.Flask(__name__) #'__main__'

model = keras.models.load_model('model2.h5')

# @app.route('/home')
# def greeting():
# 	return "Welcome!"
#

speedLimit = 20.0

def imagePreProcess(image):
  croppedImage = image[60:135, :, :]
  yuvImage = cv2.cvtColor(croppedImage, cv2.COLOR_RGB2YUV)
  smoothedImage = cv2.GaussianBlur(yuvImage, (3, 3), 0)
  resizedImage = cv2.resize(smoothedImage, (200, 66)) # size of the NVIDIA model architecture
  print(resizedImage.dtype) 
  # normalizedImage = resizedImage.astype(float)
  normalizedImage = resizedImage / 255.0
  print(normalizedImage.dtype) 

  return normalizedImage

@webserver.on('telemetry')
def telemetry(sid, data):
	speed = float(data['speed'])
	image = PIL.Image.open(io.BytesIO(base64.b64decode(data['image'])))
	image = np.asarray(image)
	imageio.v2.imwrite('output_image.png', image)
	print(image.shape)
	image = imagePreProcess(image)
	print(image.shape)

	imageio.v2.imwrite('output_image_porcessed.png', (255.0 * image).astype(np.uint8))

	image = np.array([image])

	predictedSteering = float(model.predict(image))
	print(predictedSteering)

	throttle = 1.0 - speed / speedLimit

	send_control(predictedSteering,throttle)

@webserver.on('connect') # message, disconnect
def connect(sid, environ):
	print('Connected------')
	send_control(0.0, 0.0)

def send_control(steering_angle, throttle):
	webserver.emit('steer', data = {"steering_angle": steering_angle.__str__(), "throttle":  throttle.__str__()})

if __name__ == '__main__':
	app = socketio.Middleware(webserver, app)

	eventlet.wsgi.server(eventlet.listen(('', 4567)), app)

