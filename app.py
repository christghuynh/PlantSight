from flask import Flask, Response, request, send_file, render_template
from gtts import gTTS
import tempfile
import os
import cv2
import google.generativeai as genai

video = cv2.VideoCapture(0)

genai.configure(api_key=os.environ["API-KEY"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You will get an image and tell us if the plant is poisonous or not",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)'''

app = Flask(__name__)

def displayFrames():
    while True:
        ret, frame = video.read()

        if not ret:
            print("Can't receive frame")
            break

        if cv2.waitKey(1) == ord('q'):
            break
        
        try:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            frame = buffer.tobytes()
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame)
        except Exception as e:
            pass
    else:
        pass

@app.route('/')
def index():
    return Response(displayFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return render_template("index.html")



'''@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')'''

'''@app.route('/stream/<filename>')
def stream(filename):
    return send_file(os.path.join(tempfile.gettempdir(), filename), mimetype='audio/mp3')'''


if __name__ == '__main__':
    app.run(debug=True)



'''from flask import Flask, request, send_file, render_template
from gtts import gTTS
import tempfile
import os
from ultralytics import YOLO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", audio_url=None)


@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
   
    if not text:
        return render_template("index.html", audio_url=None)


    # Create a gTTS object and save the audio file to a temporary file
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file_path = temp_file.name
    temp_file.close()
    tts.save(temp_file_path)


    # Provide the path to the generated MP3 file
    return render_template("index.html", audio_url=f'/stream/{os.path.basename(temp_file_path)}')


@app.route('/stream/<filename>')
def stream(filename):
    return send_file(os.path.join(tempfile.gettempdir(), filename), mimetype='audio/mp3')


if __name__ == '__main__':
    app.run(debug=True)
'''
