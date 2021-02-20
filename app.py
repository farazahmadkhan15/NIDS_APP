from flask import Flask, render_template
from pyfladesk import init_gui

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/register')
def register():
    v=7;
    return render_template('register.html')

if __name__ == '__main__':
    init_gui(app,
             window_title="Eng@ge", icon="appicon.png", argv=None)
