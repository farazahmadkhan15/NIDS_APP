from flask import Flask
from config import Config
from flask_socketio import SocketIO, send
from flask_sse import sse




app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


app.config.from_object(Config)
app.register_blueprint(sse, url_prefix='/stream')



from app import routes



