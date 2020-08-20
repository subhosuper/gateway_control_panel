from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from wtforms import Form, TextField, validators, SubmitField, SelectField
from signal_strength import ssid_list
from attributes_ssid import *
import datetime
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,JWTManager,jwt_refresh_token_required,create_refresh_token,get_jwt_identity,set_access_cookies,set_refresh_cookies,unset_jwt_cookies

app = Flask(__name__)
app.config.from_object(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/template'
app.config['SECRET_KEY'] = "key12345"

USER_DATA = {'bro' : '12345','subham' : 'subham'}

jwt = JWTManager(app)

@app.route('/')
def index():
   return render_template('login.html')

#def wifi_name(SSID):
 #   global SSID_name = SSID 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['user']
        password = request.form['pass']
        for user_loop in USER_DATA:
            if user_loop == username and USER_DATA[user_loop] == password:
                access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(seconds=15))
                resp = make_response(render_template('home.html'))
                resp.set_cookie('access_token_cookie', access_token)
                return resp
        else:
            return make_response('Username or Password is invalid')

    return render_template('login.html')

@app.route('/home', methods=['GET','POST'])
@jwt_required
def home():
    return render_template('home.html')

@app.route('/system_config', methods=['GET','POST'])
@jwt_required
def sysconf():
    return render_template('system_config.html')

@app.route('/software_update')
@jwt_required
def sofupd():
    return render_template('software_update.html')

@app.route('/endpoint_config', methods=['GET','POST'])
def endconf():
    return render_template('endpoint_config.html')

if __name__ == '__main__':
   app.run(debug = True)