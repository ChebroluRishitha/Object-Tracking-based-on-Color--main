from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import imutils
import threading
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# HSV Color Range
LOWER_HSV = (0, 50, 50)
UPPER_HSV = (10, 255, 255)

class ObjectTracker:
    def __init__(self):
        self.cam = None
        self.init_camera()
        self.status = "Starting..."
        self.direction = "---"
        self.radius = 0
        self.current_frame = None
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self.process_frames, daemon=True)
        self.thread.start()
        time.sleep(1)
    
    def init_camera(self):
        for i in range(3):
            try:
                self.cam = cv2.VideoCapture(0)
                self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cam.set(cv2.CAP_PROP_FPS, 30)
                self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                ret, _ = self.cam.read()
                if ret:
                    print("✓ Camera OK")
                    return
                self.cam.release()
            except:
                pass
            time.sleep(0.3)
    
    def process_frames(self):
        while self.running:
            try:
                if not self.cam or not self.cam.isOpened():
                    self.init_camera()
                    time.sleep(1)
                    continue
                
                ret, frame = self.cam.read()
                if not ret:
                    continue
                
                frame = imutils.resize(frame, width=600)
                frame = cv2.flip(frame, 1)
                blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                
                contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = contours[0] if len(contours) == 2 else contours[1]
                
                with self.lock:
                    self.status = "No Object"
                    self.direction = "---"
                    self.radius = 0
                
                if len(contours) > 0:
                    c = max(contours, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    if radius > 5:
                        M = cv2.moments(c)
                        if M["m00"] > 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                            
                            with self.lock:
                                self.status = "✓ DETECTED"
                                self.radius = int(radius)
                                if radius > 250:
                                    self.direction = "STOP"
                                elif cx < 150:
                                    self.direction = "LEFT"
                                elif cx > 450:
                                    self.direction = "RIGHT"
                                else:
                                    self.direction = "FRONT"
                            
                            cv2.putText(frame, self.status, (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(frame, self.direction, (15, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
                
                with self.lock:
                    self.current_frame = frame
                
                time.sleep(0.02)
            except Exception as e:
                print(f"Error: {str(e)[:30]}")
                time.sleep(0.5)
    
    def get_frame_jpg(self):
        with self.lock:
            if self.current_frame is None:
                blank = np.zeros((480, 640, 3), np.uint8)
                cv2.putText(blank, "Loading...", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                frame = blank
            else:
                frame = self.current_frame
        ret, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return buf.tobytes() if ret else None
    
    def get_status(self):
        with self.lock:
            return {"status": self.status, "direction": self.direction, "radius": self.radius}
    
    def stop(self):
        self.running = False
        if self.cam:
            self.cam.release()

tracker = ObjectTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            try:
                data = tracker.get_frame_jpg()
                if data:
                    yield b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: ' + str(len(data)).encode() + b'\r\n\r\n' + data + b'\r\n'
                time.sleep(0.03)
            except:
                time.sleep(0.1)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame', direct_passthrough=True)

@app.route('/status')
def get_status():
    return jsonify(tracker.get_status())

if __name__ == '__main__':
    print("\n" + "="*50)
    print("OBJECT TRACKER WEB APP")
    print("="*50)
    print(f"\nColor Range: HSV {LOWER_HSV} to {UPPER_HSV}")
    print("\n🌐 Open: http://127.0.0.1:5000")
    print("🛑 Stop: Ctrl+C\n")
    print("="*50 + "\n")
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        tracker.stop()
        print("\n✓ Stopped")
