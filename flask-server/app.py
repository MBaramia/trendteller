from flask_socketio import SocketIO
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdhsbfdsh3274y327432"

# add cors policy
CORS(app, resources={r"/*":{"origins":"*"}})

# create websocket
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

