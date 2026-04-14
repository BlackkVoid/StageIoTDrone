"""
Script visant à prendre une vidéo avec la caméra IA, et à l'afficher sur une page internet avec le module de reconnaissance IA activé
"""
import cv2
from flask import Flask, Response

app = Flask(__name__)
cam = cv2.VideoCapture(0)

def generate():
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=5000)
