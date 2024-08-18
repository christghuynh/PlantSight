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
  system_instruction="You will get an image and tell us if the plant is poisonous or not",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)

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

if __name__ == '__main__':
    app.run(debug=True)
