from flask import Flask


from config import Config

from flask_sse import sse
app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(sse, url_prefix='/stream')



from app import routes



