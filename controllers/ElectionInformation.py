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
Election_Information = Blueprint('Election_Information', __name__,
                           template_folder='templates')
@Election_Information.route('/api/electionInformation', methods=['POST'])
def electionInformation():
    try:
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        print(apartmentId)
        myquery1 = { 'apartmentId': apartmentId,'candidateId': request.get_json()['candidateId'].strip()}
        mydoc1 = dic['notificationInformation'].find(myquery1)
        if mydoc1.count() != 0:
            myUserJson={
            "$set":{
             "candidateflatNo": request.get_json()['candidateflatNo'],
             "candidateId": request.get_json()['candidateId'],
             "candidateName": request.get_json()['candidateName'],
             "anounceDate": request.get_json()['anounceDate'],
             "electionDate": request.get_json()['electionDate'],
             "position": request.get_json()['position']
            }
            }
            dic['electionInformation'].update_one(myquery1,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
           
        else:
            myUserJson= [{
             "apartmentId": apartmentId,
             "candidateflatNo": request.get_json()['candidateflatNo'],
             "candidateId": request.get_json()['candidateId'],
             "candidateName": request.get_json()['candidateName'],
             "electionDate": request.get_json()['electionDate'],
             "anounceDate": request.get_json()['anounceDate'],
             "position": request.get_json()['position'],
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))
            }]
            x = dic['electionInformation'].insert_many(myUserJson)
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
@Election_Information.route('/api/pushElectionInformation', methods=['POST'])
def pushElectionInformation():
    try:
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        print(apartmentId)
        myquery1 = { 'apartmentId': apartmentId,'notificationId': request.get_json()['notificationId'].strip(),"latestValue":1}
        mydoc1 = dic['notificationInformation'].find(myquery1)
        if mydoc1.count() != 0:
            myUserJson={
             "$push":{
              "approval":
               {
              "flatNo": request.get_json()['flatNo'],
              "status": request.get_json()['status'],
              "candidateId": request.get_json()['candidateId']
              }
             }
             }
            dic['electionInformation'].update_one(myquery1,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
           
        else:
            task = {'status': 'Failed',"message":"Notification Information not latest"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,404)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except BulkWriteError as e:
        task = {'status': 'Someting went wrong in post data %s' % e}
        res2 = json.dumps(task)
        res1=json.loads(res2)
        response=make_response(res1,404)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
@Election_Information.route('/api/electionList', methods=['GET'])
#@auth.login_required
def electionList():
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
        task = dumps(dic['electionInformation'].find(myquery))
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