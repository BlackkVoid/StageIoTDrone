"""
Script visant à prendre une vidéo avec la caméra IA et à l'afficher dans une page internet avec la reconnaissance IA activée
"""
from flask import Flask, Response
import subprocess

app = Flask(__name__)

CMD = [
    "rpicam-vid",
    "-t", "0",
    "--width", "1280",
    "--height", "720",
    "--framerate", "30",
    "--codec", "mjpeg",
    "--post-process-file", "/usr/share/rpi-camera-assets/imx500_mobilenet_ssd.json",
    "--output", "-"
]

process = subprocess.Popen(CMD, stdout=subprocess.PIPE, bufsize=10**8)

def generate():
    stream = b""

    while True:
        data = process.stdout.read(1024)
        if not data:
            continue

        stream += data

        # découpe MJPEG frames
        a = stream.find(b'\xff\xd8')  # JPEG start
        b = stream.find(b'\xff\xd9')  # JPEG end

        if a != -1 and b != -1 and b > a:
            jpg = stream[a:b+2]
            stream = stream[b+2:]

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

@app.route('/')
def index():
    return """
    <html>
        <body>
            <h2>IMX500 AI Stream</h2>
            <img src="/video">
        </body>
    </html>
    """

@app.route('/video')
def video():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
