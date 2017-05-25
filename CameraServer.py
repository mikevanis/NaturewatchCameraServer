import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print self.path
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			try:
				print("Opening camera...")
				camera = PiCamera()
				camera.resolution = (640, 480)
				camera.framerate = 32
				rawCapture = PiRGBArray(camera, size=(640,480))
				time.sleep(0.1)
				
				for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
					img = frame.array
					imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
					r, buf = cv2.imencode(".jpg",imgRGB)
					self.wfile.write("--jpgboundary\r\n")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(len(buf)))
					self.end_headers()
					self.wfile.write(bytearray(buf))
					self.wfile.write('\r\n')
					#time.sleep(0.5)
					rawCapture.truncate(0)
			except KeyboardInterrupt:
				print("keyboard interrupt")
		if self.path.endswith('.html') or self.path=="/":
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://127.0.0.1:9090/cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return

def main():
	try:
		server = HTTPServer(('',9090),CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()

if __name__ == '__main__':
	main()