#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request,send_file,make_response,session
from jinja2 import TemplateNotFound
from datetime import datetime
from pymongo.errors import BulkWriteError
from flask import jsonify
from bson.json_util import dumps
import pymongo
import json
import time
from cryptography.fernet import Fernet
import validators
import os
import shutil
import Dbconnection
Api_Controller = Blueprint('Api_Controller', __name__,
                           template_folder='templates')
def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@Api_Controller.route('/api/userList', methods=['GET'])
#@auth.login_required
def read():
    """
    This function responds to a request for /api/Inventory
    with the complete lists of Inventory
    :return:        sorted list of Inventory
    """

    # Create the list of Inventory from our data
    # return jsonify(INVENTORY)
    user = session.get('username')
    #apartmentId = session.get('apartmentId')
    apartmentId="ADADA"
    myquery = {'apartmentId': apartmentId}
    print(session)
    print(str(user))
    if user == '':
        task = {'status': 'Redirect to login page'}
        return jsonify(task)
    try:
        dic = Dbconnection.DBConnection()
        task = dumps(dic['user'].find(myquery))
        res = json.dumps(task)
        res1=json.loads(res)
        response=make_response(res1,200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except BulkWriteError as e:
        task = {'status': 'Someting went wrong in GET data %s' % e}
        #abort(404)
        res = json.dumps(task)
        res1=json.loads(res)
        response=make_response(res1,401)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return jsonify(task)
@Api_Controller.route('/api/adminRegister', methods=['POST'])
def adminRegister():
    try:
        if not validators.length(request.get_json()['username'].strip(), min=2) or not validators.length(request.get_json()['password'].strip(), min=2) or not validators.length(request.get_json()['fullName'].strip(), min=2) or not validators.length(request.get_json()['flatNo'].strip(), min=2) or not validators.email(request.get_json()['emailId'].strip()) or not validators.length(request.get_json()['mobile'].strip(), min=2):
              task = {'status': 'All Fields are manditory'}
              res2 = json.dumps(task)
              res1=json.loads(res2)
              response=make_response(res1,400)
              response.headers.add('Access-Control-Allow-Origin', '*')
              return response
        if not validators.length(request.get_json()['apartmentId'].strip(), min=2) or not validators.length(request.get_json()['apartmentName'].strip(), min=2) or not validators.length(request.get_json()['address'].strip(), min=2) or not validators.length(request.get_json()['city'].strip(), min=2) or not validators.length(request.get_json()['state'].strip(), min=2):
              task = {'status': 'All Fields are manditory'}
              res2 = json.dumps(task)
              res1=json.loads(res2)
              response=make_response(res1,400)
              response.headers.add('Access-Control-Allow-Origin', '*')
              return response
        today = datetime.now()
        dic = Dbconnection.DBConnection()
        key = Fernet.generate_key()
        f = Fernet(key)
        myquery = {'apartmentId': request.get_json()['apartmentId'].strip()}
        mydoc = dic['admin'].find(myquery)
        print(mydoc.count())
        if mydoc.count() != 0:
            task = {'status': 'Already apartmentId exist'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            myAdminJson= [{
             "apartmentId": request.get_json()['apartmentId'].strip(),
             "apartmentName": request.get_json()['apartmentName'].strip(),
             "address": request.get_json()['address'].strip(),
             "city": request.get_json()['city'].strip(),
             "state": request.get_json()['state'].strip(), 
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))
            }]
            x = dic['admin'].insert_many(myAdminJson)
            time.sleep(5)
            myUserJson= [{
             "apartmentId": request.get_json()['apartmentId'].strip(),
             "fullName": request.get_json()['fullName'].strip(),
             "username": request.get_json()['username'].strip(),
             "password": f.encrypt(bytes(request.get_json()['password'].strip())),
             "flatNo": request.get_json()['flatNo'],
             "emailId": request.get_json()['emailId'].strip(),
             "mobile": request.get_json()['mobile'].strip(),
             "type": "President",
             "key": key,
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['user'].insert_many(myUserJson)
            task = {'status': 'Success',"message":"Success"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except BulkWriteError as e:
        task = {'status': 'Someting went wrong in post data %s' % e}
        abort(404)
        return jsonify(task)
@Api_Controller.route('/api/login', methods=['POST'])
def login():
    try:
        if not validators.length(request.get_json()['username'].strip(), min=2) or not validators.length(request.get_json()['password'].strip(), min=2):
              task = {'status': 'username and password should not be null'}
              res2 = json.dumps(task)
              res1=json.loads(res2)
              response=make_response(res1,400)
              response.headers.add('Access-Control-Allow-Origin', '*')
              return response
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        key = Fernet.generate_key()
        #apartmentId = session.get('apartmentId')
        myquery = {'username': request.get_json()['username'].strip()}
        mydoc = dic['user'].find(myquery)
        print(mydoc.count())
        if mydoc.count() == 0:
            task = {'status': 'Invalid username and password'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,400)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        task = dumps(mydoc)
        res = json.dumps(task)
        res1=json.loads(res).strip('[]')
        res2=eval(res1)
        password=res2.get('password')
        f = Fernet(res2.get('key'))
        if f.decrypt(password) == request.get_json()['password'].strip():
          session['username']= res2.get('username')
          session['apartmentId']= res2.get('apartmentId')
          task = {'status': 'Success'}
          res2 = json.dumps(task)
          res1=json.loads(res2)
          response=make_response(res1,200)
          response.headers.add('Access-Control-Allow-Origin', '*')
          return response
        else:
            task = {'status': 'Invalid username and password'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,400)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except BulkWriteError as e:
        task = {'status': 'Someting went wrong in post data %s' % e}
        res2 = json.dumps(task)
        res1=json.loads(res2)
        response=make_response(res1,404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response





@Api_Controller.route('/api/userRegister', methods=['POST'])
def userRegister():
    try:
        if not validators.length(request.get_json()['username'].strip(), min=2) or not validators.length(request.get_json()['password'].strip(), min=2) or not validators.length(request.get_json()['fullName'].strip(), min=2) or not validators.length(request.get_json()['flatNo'].strip(), min=2) or not validators.email(request.get_json()['emailId'].strip()) or not validators.length(request.get_json()['mobile'].strip(), min=2):
              task = {'status': 'All Fields are manditory'}
              res2 = json.dumps(task)
              res1=json.loads(res2)
              response=make_response(res1,400)
              response.headers.add('Access-Control-Allow-Origin', '*')
              return response
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        key = Fernet.generate_key()
        f = Fernet(key)
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        print(apartmentId)
        myquery1 = {'emailId': request.get_json()['emailId'].strip(), 'username': request.get_json()['username'].strip()}
        mydoc1 = dic['user'].find(myquery1)
        if mydoc1.count() != 0:
             task = {'status': 'user Already exist'}
             res2 = json.dumps(task)
             res1=json.loads(res2)
             response=make_response(res1,404)
             response.headers.add('Access-Control-Allow-Origin', '*')
             return response
        myquery2 = {'username': request.get_json()['username'].strip()}
        mydoc2 = dic['user'].find(myquery2)
        if mydoc2.count() != 0:
             task = {'status': 'user Already exist'}
             res2 = json.dumps(task)
             res1=json.loads(res2)
             response=make_response(res1,404)
             response.headers.add('Access-Control-Allow-Origin', '*')
             return response
        myquery = {'apartmentId': apartmentId,'emailId': request.get_json()['emailId'].strip(), 'username': request.get_json()['username'].strip()}
        mydoc = dic['user'].find(myquery)
        if mydoc.count() != 0:
             task = {'status': 'user Already exist'}
             res2 = json.dumps(task)
             res1=json.loads(res2)
             response=make_response(res1,404)
             response.headers.add('Access-Control-Allow-Origin', '*')
             return response
        else:
            myUserJson= [{
             "apartmentId": apartmentId,
             "fullName": request.get_json()['fullName'].strip(),
             "username": request.get_json()['username'].strip(),
             "password": f.encrypt(bytes(request.get_json()['password'].strip())),
             "flatNo": request.get_json()['flatNo'],
             "emailId": request.get_json()['emailId'].strip(),
             "mobile": request.get_json()['mobile'].strip(),
             "type": request.get_json()['type'].strip(),
             "key": key,
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['user'].insert_many(myUserJson)
            task = {'status': 'Success',"message":"Sucessfully Update"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except BulkWriteError as e:
        task = {'status': 'Someting went wrong in post data %s' % e}
        res2 = json.dumps(task)
        res1=json.loads(res2)
        response=make_response(res1,404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
@Api_Controller.route('/api/updateUserRegister', methods=['PUT'])
def updateUserRegister():
    try:
        if not validators.length(request.get_json()['username'].strip(), min=2) or not validators.length(request.get_json()['password'].strip(), min=2) or not validators.length(request.get_json()['fullName'].strip(), min=2) or not validators.length(request.get_json()['flatNo'].strip(), min=2) or not validators.email(request.get_json()['emailId'].strip()) or not validators.length(request.get_json()['mobile'].strip(), min=2):
              task = {'status': 'All Fields are manditory'}
              res2 = json.dumps(task)
              res1=json.loads(res2)
              response=make_response(res1,400)
              response.headers.add('Access-Control-Allow-Origin', '*')
              return response
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        key = Fernet.generate_key()
        f = Fernet(key)
        apartmentId="ADADA"
        myquery = {'apartmentId': apartmentId,'username': request.get_json()['username'].strip()}
        print(myquery)
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        if apartmentId == "":
             print(apartmentId)
             task = {'status': 'redirect to login'}
             res2 = json.dumps(task)
             res1=json.loads(res2)
             response=make_response(res1,404)
             response.headers.add('Access-Control-Allow-Origin', '*')
             return response
        else:
            myUserJson= {'$set':{
             "apartmentId": apartmentId,
             "fullName": request.get_json()['fullName'].strip(),
             "username": request.get_json()['username'].strip(),
             "password": f.encrypt(bytes(request.get_json()['password'].strip())),
             "flatNo": request.get_json()['flatNo'],
             "emailId": request.get_json()['emailId'].strip(),
             "mobile": request.get_json()['mobile'].strip(),
             "type": request.get_json()['type'].strip(),
             "key": key,
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }
            }
            dic['user'].update_one(myquery,myUserJson)
            task = {'status': 'Success',"message":"Sucessfully Update"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except BulkWriteError as e:
        task = {'status': 'Someting went wrong in post data %s' % e}
        res2 = json.dumps(task)
        res1=json.loads(res2)
        response=make_response(res1,404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


