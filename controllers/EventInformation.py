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
Event_Information = Blueprint('Event_Information', __name__,
                           template_folder='templates')
@Event_Information.route('/api/eventInformation', methods=['POST'])
def eventInformation():
    try:
        dic = Dbconnection.DBConnection()
        apartmentId="ADADA"
        username = "kumar"
        today = datetime.now()
        myquery = {'apartmentId': apartmentId,"eventId": request.get_json()['eventId'].strip()}
        mydoc = dic['eventId'].find(myquery)
        print(mydoc.count())
        if mydoc.count() != 0:
            myUserJson={
            "$set":{
                  "apartmentId": apartmentId,
                  "eventId": request.get_json()['eventId'].strip(),
                  "eventName": request.get_json()['eventName'].strip(),
                  "budget": request.get_json()['budget'].strip(),
                  "eventDate": request.get_json()['eventDate'].strip()

             }
            }
            dic['eventId'].update_one(myquery,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            myquery1 = {'apartmentId': apartmentId,"eventId": request.get_json()['eventId'].strip(),"latestEvent": 1}
            mydoc1 = dic['eventId'].find(myquery)
            myUserJson11={
            "$set":{
                  "latestEvent": 0

             }
            }
            if mydoc1.count() != 0:
                dic['eventId'].update_one(myquery1,myUserJson1)
            myUserJson= [{
             "apartmentId": apartmentId,
             "eventId": request.get_json()['eventId'].strip(),
             "eventName": request.get_json()['eventName'].strip(),
             "latestEvent": 1,
             "ownerName": username,
             "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['eventId'].insert_many(myUserJson)
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
@Event_Information.route('/api/eventIdList', methods=['GET'])
#@auth.login_required
def eventIdList():
    """
    This function responds to a request for /api/Inventory
    with the complete lists of Inventory
    :return:        sorted list of Inventory
    """

    # Create the list of Inventory from our data
    # return jsonify(INVENTORY)
    user = "kumar"
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
        task = dumps(dic['eventId'].find(myquery))
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
@Event_Information.route('/api/eventItemInformation', methods=['POST'])
def eventItemInformation():
    try:
        dic = DBConnection()
        apartmentId="ADADA"
        username = "kumar"
        today = datetime.now()
        myquery = {'apartmentId': apartmentId,"eventId": request.get_json()['eventId'].strip()}
        mydoc = dic['eventId'].find(myquery)
        print(mydoc.count())
        if mydoc.count() != 0:
            myUserJson={
            "$set":{
                  "apartmentId": apartmentId,
                  "eventId": request.get_json()['eventId'].strip(),
                  "eventName": request.get_json()['eventName'].strip()

             }
            }
            dic['eventId'].update_one(myquery,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            myquery1 = {'apartmentId': apartmentId,"eventId": request.get_json()['eventId'].strip(),"latestEvent": 1}
            mydoc1 = dic['eventId'].find(myquery)
            myUserJson11={
            "$set":{
                  "latestEvent": 0

             }
            }
            if mydoc1.count() != 0:
                dic['eventId'].update_one(myquery1,myUserJson1)
            myUserJson= [{
             "apartmentId": apartmentId,
             "eventId": request.get_json()['eventId'].strip(),
             "eventName": request.get_json()['eventName'].strip(),
             "eventAmountCollected": request.get_json()['eventAmountCollected'].strip(),
             "latestEvent": 1,
             "ownerName": username,
             "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['eventId'].insert_many(myUserJson)
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
@Event_Information.route('/api/eventItemList', methods=['GET'])
#@auth.login_required
def eventItemList():
    """
    This function responds to a request for /api/Inventory
    with the complete lists of Inventory
    :return:        sorted list of Inventory
    """

    # Create the list of Inventory from our data
    # return jsonify(INVENTORY)
    user = "kumar"
    #apartmentId = session.get('apartmentId')
    apartmentId="ADADA"
    myquery = {'apartmentId': apartmentId}
    print(session)
    print(str(user))
    if user == '':
        task = {'status': 'Redirect to login page'}
        return jsonify(task)
    try:
        dic = DBConnection()
        task = dumps(dic['eventId'].find(myquery))
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