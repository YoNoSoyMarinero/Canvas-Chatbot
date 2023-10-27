from flask import Flask
from config import Config
from routes import chatbot
from dotenv import load_dotenv
import os


#Creating flask app
app: Flask = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(chatbot.chatbot_bp)
load_dotenv('.env')

if (__name__ == '__main__'):
    app.run(debug=True, host=os.getenv("HOST"), port=os.getenv("PORT"))