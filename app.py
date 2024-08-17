from flask import Flask, request, send_file, render_template_string
from gtts import gTTS
import tempfile
import os


app = Flask(__name__)
