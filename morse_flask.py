from flask import Flask, render_template, Response
from morse_camera import Camera
from morse_eyes import Detectmorse
import time
from morse_log import log

app = Flask(__name__)
morse = Detectmorse()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        png, L = morse.calculate(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + png.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/yield')
def streambyte():
    L = morse.current_morse_seq
    final = ''.join(morse.finalString)
    b = (''.join(L)).encode('utf-8')
    c = final.encode('utf-8')
    log(b)
    log(c)
    def events():
        yield f"data: {b.decode()} {c.decode()}\n\n"
        time.sleep(1)
    return Response(events(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
