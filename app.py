from flask import Flask, request, send_file, render_template
from gtts import gTTS
import tempfile
import os
import google.generativeai as genai

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

@app.route('/')
def index():

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file_path = temp_file.name
    temp_file.close()

    return render_template("index.html", audio_url=f'/stream/{os.path.basename(temp_file_path)}')


@app.route('/stream/<filename>')
def stream(filename):
    return send_file(os.path.join(tempfile.gettempdir(), filename), mimetype='audio/mp3')


if __name__ == '__main__':
    app.run(debug=True)
