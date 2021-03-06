from flask import render_template,flash,redirect,url_for,request
from flask import request,json,jsonify, Response
import netifaces
import json
import os
import subprocess
import sys
import numpy as np
import pandas as pd 
import pickle
import os
from app.forms import If_form
from app import app
flows = []
resp = {}
pid = ''
basedir = os.path.abspath(os.path.dirname(__file__))





@app.route('/',methods=['POST','GET'])           # decorators that modifies function follows
def index():
       interface = netifaces.interfaces()
       form = If_form();
       print(request.url)
       interface.insert(0,"-- Please Select Interface --")
       form.interface.choices = interface
       form.interface.default = interface[0]
       return render_template('interface.html', form = form)
       



@app.route('/start',methods=['POST','GET'])           # decorators that modifies function follows
def start():
       form = If_form();
       global pid
       
       pid = subprocess.Popen(["cicflowmeter","-i",
                               form.interface.data,"-c",
                              os.path.join(basedir, 'flows.csv') ,
                               "-u",
                               request.url_root+"/predict/"]) # Call subprocess
         
       
       return redirect(url_for('home'))

@app.route('/flows', methods= ['GET'])
def flows():
    global resp

    print(resp)
    
    return jsonify (resp)
 

    
    
@app.route('/newInterface')
def newInterface():
    print(pid)
    pid.kill()
    return redirect(url_for('index'))

# De-Serializing Model
model = pickle.load(open(os.path.join(basedir, 'nids_model_rf.pkl'),"rb"))

@app.route('/predict/', methods=['POST'])
def predict():
    global flows
    global resp
    req = request.get_json()
    df1 = pd.DataFrame(data=req["data"], columns=req["columns"] )
    df2 = df1.copy()
   
    # droping unwanted columns
    col =['src_ip','dst_ip','src_port','dst_port','protocol','timestamp']
    df1.drop(col, inplace=True, axis=1)
    df1.reset_index(drop=True, inplace=True)
    # Making Pridiction
    pred = model.predict(df1)

    

    
    
    # returning result as JSON
    resp = {'src_ip':df2['src_ip'].values[0],
              'dst_ip':df2['dst_ip'].values[0],
              'timestamp':df2['timestamp'].values[0],
              'result': pred[0] }
   
    
    # flows.append(resp)
    return redirect(url_for('home'))



@app.route('/home')
def home():
    global flows

    return render_template('home.html',flows = flows)