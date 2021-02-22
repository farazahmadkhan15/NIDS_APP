from flask import render_template,flash,redirect,url_for,request
from flask import request
import netifaces
import json
from app.forms import If_form
from app import app


 



@app.route('/',methods=['POST','GET'])           # decorators that modifies function follows
def index():
       interface = netifaces.interfaces()
       form = If_form();
       interface.insert(0,"-- Please Select Interface --")
       form.interface.choices = interface
       form.interface.default = interface[0]
       return render_template('interface.html', form = form)
       


@app.route('/start',methods=['POST','GET'])           # decorators that modifies function follows
def start():
       form = If_form();
       addrs = netifaces.ifaddresses(form.interface.data)
       addrs = addrs[netifaces.AF_INET]
       addrs = addrs[0]
       print(addrs)


       if form.validate_on_submit() and  form.interface.data !=  "-- Please Select Interface --":
             return "<h1> Submit {}  </h1>".format(form.interface.data) 
              
       return render_template("start.html",interface=form.interface.data,addrs = addrs)

       
       