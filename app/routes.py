from flask import render_template,flash,redirect,url_for,request, session,  Response
from flask import request,json,jsonify, Response

from sklearn import metrics
from flask_sse import sse
import psutil
import netifaces
import json
import os
import subprocess
import sys
import numpy as np
import pandas as pd 
import pickle
import os, signal
from app.forms import If_form
from app import app
flows = []
resp = {}
pid = None
interface = ''
basedir = os.path.abspath(os.path.dirname(__file__))





@app.route('/',methods=['POST','GET'])           # decorators that modifies function follows
def index():
       interface = netifaces.interfaces()
       form = If_form();
       print(request.url)
       interface.insert(0,"-- Please Select Interface --")
       form.interface.choices = interface
       form.interface.default = interface[0]
       
       ifconfig = subprocess.check_output(['ifconfig'])

       return render_template('interface.html', form = form, ifconfig = ifconfig)
       

def cicflowmeter(start,interface):
    global pid
    if start:
     
        p = subprocess.Popen(["cicflowmeter","-i",
                               interface,"-c",
                              os.path.join(basedir, 'static/flows.csv') ,
                               "-u",
                               request.url_root+"/predict/"]) # Call subprocess
        pid = p.pid
       

    elif not start:
        print(pid)
        os.kill(pid, signal.SIGSTOP)
        print("stop")



@app.route('/start',methods=['POST','GET'])           # decorators that modifies function follows
def start():
        form = If_form();      
        cicflowmeter(True,form.interface.data)
        session['interface'] = form.interface.data
        return redirect(url_for('home'))




@app.route('/ip', methods=['GET'])
def ip():
    ip = request.args.get('ip')
    if request.method == 'GET':
        whois = subprocess.check_output([f'whois {ip}'],shell=True)
        # traceroute = subprocess.check_output([f'traceroute  {ip}'],shell=True)
        
        message = {'whois': whois.decode("utf-8")}
        return jsonify(message)  # serialize and use JSON headers


@app.route('/newInterface')
def newInterface():
    cicflowmeter(False,None)
    return redirect(url_for('index'))


@app.route('/stop')
def stop():
    cicflowmeter(False,None)
    print("Stooooooooooooooop")
    return ('', 204)


#De-Serializing Model
model = pickle.load(open(os.path.join(basedir, 'nids_model_ADABoost.pkl'),"rb"))

@app.route('/testing')
def testing():
    benign = 0
    bot = 0
    ddos = 0
    portScan = 0
    infliteration = 0
    bruteForce = 0
    sqlInjection = 0
    xss = 0
    total = 0
    df = pd.read_csv(os.path.join(basedir, 'smt_X_Test.csv'));
    y_test = pd.read_csv(os.path.join(basedir, 'smt_y_Test.csv'));
    df.drop('Unnamed: 0',
    axis='columns', inplace=True)
    pred = model.predict(df)
    
    # (unique, counts) = np.unique(pred, return_counts=True)
    accuracy = metrics.accuracy_score(y_test["0"].values.reshape(-1, 1),pred)

    for x in pred:
        total += 1
        if x == 0:
            benign += 1
        elif x == 1:
            bot += 1          
        elif x == 2:
            ddos += 1
        elif x == 3:
            infliteration += 1
        elif x == 4:
            portScan += 1
        elif x == 5:
            bruteForce += 1
        elif x == 6:
            sqlInjection += 1
        elif x == 7:
            xss += 1

    accuracy = accuracy*100

    result = {"accuracy" : accuracy,
                "benign": benign, "bot" : bot, "total" : total,
                "ddos":ddos,"infliteration": infliteration,
                "portscan" : portScan,"bruteforce": bruteForce,"sqlInjection":sqlInjection,"xss":xss}

    print(result)
    # pred_labels = pd.Series(pred).to_json(orient='values')
    # print(type(pred_labels))
    # for x in pred:
  
    # print(result)
    # sse.publish(result, type='greeting')

   
    # frequencies = np.asarray((unique, counts)).T

    return render_template('testing.html', result = result)


@app.route('/predict/', methods=['POST'])
def predict():
    req = request.get_json()
    df1 = pd.DataFrame(data=req["data"], columns=req["columns"] )
    df2 = df1.copy()
    cols = [' Bwd Packet Length Std', ' min_seg_size_forward', ' PSH Flag Count', ' Min Packet Length',
             ' Init_Win_bytes_backward', ' ACK Flag Count', 'Total Length of Fwd Packets', ' Subflow Fwd Bytes',
              'Init_Win_bytes_forward', ' Bwd Packet Length Min', ' Fwd IAT Std', ' Flow IAT Max', ' URG Flag Count',
               ' Destination Port', ' Flow IAT Mean', ' Flow Duration', ' Bwd Packets/s', 'Fwd IAT Total', 'Bwd IAT Total', 
               ' act_data_pkt_fwd', ' Down/Up Ratio', ' Idle Min', ' Fwd Packet Length Min', ' Bwd IAT Max', ' Fwd Packet Length Mean']
    feature = df1[cols]


   

    # Making Pridiction
    pred = model.predict(feature) 


    label = pred[0]
    if label == 0:
        df1['label'] = 'Benign'
    elif label == 1:
        df1['label'] = 'Bot'
    elif label == 2:
        df1['label'] = 'DDoS'
    elif label == 3:
        df1['label'] = 'Infilteration'
    elif label == 4:
        df1['label'] = 'PortScan'
    elif label == 5:
        df1['label'] = 'Brute-Force'
    elif label == 6:
        df1['label'] = 'Sql-Injection'
    elif label == 7:
        df1['label'] = 'XSS'


    df1.rename(columns = {" Destination Port": "dst_port"}, 
          inplace = True)
    result = df1.to_json(orient="records")
    
 
    
    
    
    # sendData(msg)
    sse.publish(result, type='greeting')
    
    # handleMessage(msg)
    # flows.append(re
  
    return jsonify(label = df1['label'].values[0])


# @socketio.on('my event', namespace='/hello')
# def hello():
#     emit('my response', {'data': 'got it!'})
#     return "11"

	

@app.route('/home')
def home():    
    return render_template('home.html')