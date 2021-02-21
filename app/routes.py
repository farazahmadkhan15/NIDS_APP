from flask import render_template,flash,redirect,url_for
from flask import request
from app import app
 



@app.route('/')           # decorators that modifies function follows
def index():
       return render_template('interface.html')
       
       
