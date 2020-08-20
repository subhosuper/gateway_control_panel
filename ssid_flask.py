from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from wtforms import Form, TextField, validators, SubmitField, SelectField
from signal_strength import ssid_list
from attributes_ssid import *
from connected_ssid import connected_ssid
import datetime
from flask_jwt_extended import JWTManager,jwt_required,jwt_optional,create_access_token,JWTManager,jwt_refresh_token_required,create_refresh_token,get_jwt_identity,set_access_cookies,set_refresh_cookies,unset_jwt_cookies
from pymongo import MongoClient
from tag_status import tag_value
import socket
import jwt
import time
import threading

app = Flask(__name__)
app.config.from_object(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/template'
app.config['SECRET_KEY'] = "key12345"

#USER_DATA = {'bro' : '12345','subham' : 'subham'}
JWTManager(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["gateway_control"]
login_collection = db["login_database"]
tags_collection = db["tags"]
store_config_collection = db["store_config"]

password_global_check = ""
store_user = ''

@app.route('/')
def index():
    auth_cookie = request.cookies.get("access_token_cookie")
    extract_cookie = request.cookies.get("reboot_token")
    if auth_cookie != None and extract_cookie == None:
        return redirect("home", code=303)
    elif extract_cookie == None and auth_cookie == None:
        print(extract_cookie," None")
        return redirect("login", code=303)
    else:
        extract_cookie = jwt.decode(extract_cookie, '12345reboot', algorithm=['HS256'])
        print(extract_cookie, " not None")
        if extract_cookie["state"] == "off":
            print(extract_cookie, " cookie off")
            resp = make_response(redirect('home')) #only opens home without reboot dialougue box
            # resp.delete_cookie("access_token_cookie")
            resp.delete_cookie("reboot_token")
            return resp
        elif extract_cookie["state"] == "on":
            print(extract_cookie, " cookie on")
            resp = make_response(redirect("home", code=303)) #only showing home page,reboot dialouge box should pop up
            resp.delete_cookie("reboot_token")
            return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    global password_global_check
    if request.method == "POST":
        user_resp = request.form['user']
        pass_resp = request.form['pass']
        query = login_collection.find({"username": user_resp}) 
        print("query=", query)
        if query:
            document_db = list(query)
            # username_db = document_db[0]["username"]
            password_db = document_db[0]["password"]
            print(password_db)
            if pass_resp == password_db:
                password_global_check = pass_resp
                access_token = create_access_token(identity=user_resp, expires_delta=datetime.timedelta(days=15))
                resp = make_response(redirect('home'))
                resp.set_cookie('access_token_cookie', access_token)
                return resp
            else:
                return make_response("Username or Password is invalid")
                print("entered incorrect password")
        else:
            return make_response('Username or Password is invalid')
            print("entered incorrect username")

    return render_template('login.html')

@app.route('/home', methods=['GET','POST'])
@jwt_required
def home():
    global store_user
    global password_global_check
    store_user = get_jwt_identity()
    print("routed to home")
    return render_template('home.html', pswd = password_global_check)

@app.route('/system_config', methods=['GET','POST'])
@jwt_required
def sysconf():
    global password_global_check 
    return render_template('system_config.html', pswd = password_global_check)

@app.route('/software_update',methods=['GET','POST'])
@jwt_required
def sofupd():
    global password_global_check
    return render_template('software_update.html', pswd = password_global_check)

@app.route('/endpoint_config', methods=['GET','POST'])
def endconf():
    global password_global_check
    form_json = request.form.to_dict()
    store_config_collection.insert_one(form_json)
    return render_template('endpoint_config.html', pswd = password_global_check)

@app.route('/logout', methods=['GET','POST'])
@jwt_required
def logout():
    global password_global_check
    resp = make_response(render_template('login.html', pswd = password_global_check))
    resp.delete_cookie('access_token_cookie')
    return resp

@app.route("/tag_status", methods=['GET','POST'])
@jwt_required
def tagsta():
    global password_global_check
    return render_template('tag_status.html',list=tag_value(),length=len(tag_value()), pswd = password_global_check)

@app.route('/all_status', methods=['GET','POST'])
@jwt_required
def allsta():
    global password_global_check
    return render_template('all_status.html', pswd = password_global_check)

@app.route('/opc_conf', methods=['GET','POST'])
@jwt_required
def opcconf():
    global password_global_check
    return render_template('opc_config.html', pswd = password_global_check)

@app.route('/remove_tag', methods=['GET','POST'])
def remtag():
    global password_global_check
    # query = "tags_collection.remove("
    if request.method == "POST":
        tag_name = request.form["tag_name"]
        remove_tag_query = tags_collection.remove({"tags":tag_name})
        if remove_tag_query['n'] == 1:
            return jsonify({'response':'successful'})
        return jsonify({'response':'unsuccessful'})

@app.route('/change_tag_name', methods=['GET','POST'])
def chatagnam():
    global password_global_check
    if request.method == 'POST':
        tag_value1 = request.form["tag_name1"]
        tag_value2 = request.form["tag_name2"]
        update_tag_query = tags_collection.update({"tags":tag_value1}, {"$set":{"tags":tag_value2}})

@app.route('/gateway_conf', methods=['GET','POST'])
@jwt_required
def gatcon():
    global password_global_check
    status = ""
    ip_of_machine = ""
    network_ssid = connected_ssid()
    if network_ssid != "127.0.0.1_NoT_CoNnEcTeD":
        try:
            ip_of_machine = socket.gethostbyname("www.google.com")
        except:
            ip_of_machine = '127.0.0.1'
    if ip_of_machine == '127.0.0.1':
        status = "Connected, No Internet access"
    else:
        status = "Connected"
    return render_template('gateway_config.html', list=ssid_list(), length=len(ssid_list()), i=0, network_ssid=network_ssid, status=status, pswd = password_global_check)

def thread_reboot():
    time.sleep(5)
    subprocess.run(["Notepad"]) #replace this line with -> subprocess.run(["shutdown","/r","/t","30"])

#below function is just for testing
# def thread_reboot_off():
#     time.sleep(10)
#     subprocess.run(["Notepad"])

@app.route('/reboot', methods=['GET','POST'])
def reboot():
    checkbox_resp = request.form["check_relaunch"]
    encode_relaunch_token = jwt.encode({"state": checkbox_resp},'12345reboot', algorithm='HS256')
    if checkbox_resp:
        thread_start = threading.Thread(target=thread_reboot)
        thread_start.start()
        resp = make_response("System is about to restart")
        resp.set_cookie('reboot_token', encode_relaunch_token)
        return resp
#below else block is just for testing
    # else:
    #     thread_start = threading.Thread(target=thread_reboot_off)
    #     thread_start.start()
    #     resp = make_response("System is about to restart without relaunch")
    #     resp.set_cookie('reboot_token', encode_relaunch_token)
    #     # subprocess.run(["Notepad", "C:/Users/garai/Desktop/pesting"]) 
    #     return resp   

@app.route('/change_password', methods=['GET','POST'])
def chapas():
    global store_user
    global password_global_check
    # redirect(url_for('home'))
    print("password entered")
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        current_user = store_user
        print("current password: ", current_password)
        print("current user: ", current_user)
        query = list(login_collection.find({"username": current_user}))
        actual_password = query[0]["password"]
        if actual_password == current_password:
            new_password = request.form["new_password"]
            password_update_query = login_collection.update_one({"username":current_user},{"$set": {"password":new_password}})
            password_global_check = new_password
            print(password_global_check)
            print("password done")
    return redirect("home")

if __name__ == '__main__':
   app.run(debug = True)