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
import Dbconnection
import os
import shutil
Parking_Information = Blueprint('Parking_Information', __name__,
                           template_folder='templates')
@Parking_Information.route('/api/parkingAllotment', methods=['POST'])
def parkingAllotment():
    try:
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        print(apartmentId)
        myquery1 = { 'apartmentId': apartmentId,'ownerFlatNo': request.get_json()['ownerFlatNo'].strip()}
        mydoc1 = dic['parkingAllotment'].find(myquery1)
        if mydoc1.count() != 0:
            myUserJson={
            "$set":{
             "parkingNo": request.get_json()['parkingNo']
            }
            }
            dic['parkingAllotment'].update_one(myquery1,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
           
        else:
            myUserJson= [{
             "apartmentId": apartmentId,
             "ownerFlatNo": request.get_json()['ownerFlatNo'].strip(),
             "parkingNo": request.get_json()['parkingNo'],
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))
            }]
            x = dic['parkingAllotment'].insert_many(myUserJson)
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

@Parking_Information.route('/api/vehicalInforamtion', methods=['POST'])
def vehicalInforamtion():
    try:
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        print(apartmentId)
        myquery1 = { 'apartmentId': apartmentId,'notificationId': request.get_json()['notificationId'].strip()}
        mydoc1 = dic['vehicalInforamtion'].find(myquery1)
        if mydoc1.count() != 0:
            myUserJson={
            "$set":{
             "vehicalType": request.get_json()['vehicalType'],
             "vehicalNumber": request.get_json()['vehicalNumber'],
             "parkingNo": request.get_json()['parkingNo']
            }
            }
            dic['vehicalInforamtion'].update_one(myquery1,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
           
        else:
            myUserJson= [{
             "apartmentId": apartmentId,
             "ownerFlatNo":request.get_json()['ownerFlatNo'].strip(),
             "vehicalType": request.get_json()['vehicalType'],
             "vehicalNumber": request.get_json()['vehicalNumber'],
             "parkingNo": request.get_json()['parkingNo'],
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))
            }]
            x = dic['vehicalInforamtion'].insert_many(myUserJson)
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
@Parking_Information.route('/api/parkingRequest', methods=['POST'])
def parkingRequest():
    try:
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        print(apartmentId)
        myquery1 = { 'apartmentId': apartmentId,'notificationId': request.get_json()['notificationId'].strip()}
        mydoc1 = dic['notificationInformation'].find(myquery1)
        if mydoc1.count() != 0:
            myUserJson={
            "$set":{
             "parkingNo": request.get_json()['parkingNo'],
             "price": request.get_json()['price'],
             "type": request.get_json()['type']
            }
            dic['parkingRequest'].update_one(myquery1,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
           
        else:
            myUserJson= [{
             "apartmentId": apartmentId,
             "ownerFlatNo":request.get_json()['ownerFlatNo'].strip(),
             "parkingNo": request.get_json()['parkingNo'],
             "price": request.get_json()['price'],
             "type": request.get_json()['type'],
             "status": request.get_json()['status'],
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))
            }]
            x = dic['parkingRequest'].insert_many(myUserJson)
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
@Parking_Information.route('/api/parkingAllotmentList', methods=['GET'])
#@auth.login_required
def parkingAllotmentList():
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
        task = dumps(dic['parkingAllotment'].find(myquery))
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
@Parking_Information.route('/api/vehicalInforamtionList', methods=['GET'])
#@auth.login_required
def vehicalInforamtionList():
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
        task = dumps(dic['vehicalInforamtion'].find(myquery))
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
@Parking_Information.route('/api/parkingRequestList', methods=['GET'])
#@auth.login_required
def parkingRequestList():
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
        task = dumps(dic['parkingRequest'].find(myquery))
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

