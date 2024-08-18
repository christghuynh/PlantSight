from flask import Flask, Response
import time
import cv2
import google.generativeai as genai
import io
from PIL import Image
import playsound

video = cv2.VideoCapture(0)

genai.configure(api_key="API-KEY") 

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
  system_instruction="You will get an image and give us a one word yes or no answer if there is a poisonous plant within the image",
)

app = Flask(__name__)

def displayFrames():
    while True:
        ret, frame = video.read()

        if not ret:
            print("Can't receive frame")
            break

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
        
        ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
        frame = buffer.tobytes()

        response = processGemini(frame)
        resultText = response.text
        if resultText == "Yes.":
            playsound('./sounds/alert.mp3')
        print(response.text)

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame)
        time.sleep(0.5)

def processGemini(frame):
    image = Image.open(io.BytesIO(frame))
    response = model.generate_content(image)
    return response

@app.route('/')
def index():
    return Response(displayFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=5000)
