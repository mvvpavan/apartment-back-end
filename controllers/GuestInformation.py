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
Guest_Information = Blueprint('Guest_Information', __name__,
                           template_folder='templates')
@Guest_Information.route('/api/guestInformation', methods=['POST'])
def guestInformation():
    try:
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        key = Fernet.generate_key()
        f = Fernet(key)
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        print(apartmentId)
        myquery1 = { 'apartmentId': apartmentId,'username': request.get_json()['username'].strip()}
        mydoc1 = dic['user'].find(myquery1)
        if mydoc1.count() != 0:
            myUserJson={
            "$set":{
             "apartmentId": apartmentId,
             "fullName": request.get_json()['fullName'].strip(),
             "vehicalId": request.get_json()['vehicalId'],
             "permanentIdName": request.get_json()['permanentIdName'].strip(),
             "permanentId": request.get_json()['permanentId'].strip(),
             "mobile": request.get_json()['mobile'].strip(),
             "purpose": request.get_json()['purpose'].strip(),
             "ownerFlatNo": request.get_json()['ownerFlatNo'].strip(),
             "employeeId": request.get_json()['employeeId'].strip(),
             "status": request.get_json()['status'].strip(),
             "startDate": request.get_json()['startDate'].strip(),
             "endDate": request.get_json()['endDate'].strip(),
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))

             }
            }
            dic['guest'].update_one(myquery1,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
           
        else:
            myUserJson= [{
             "apartmentId": apartmentId,
             "fullName": request.get_json()['fullName'].strip(),
             "vehicalId": request.get_json()['vehicalId'],
             "permanentIdName": request.get_json()['permanentIdName'].strip(),
             "permanentId": request.get_json()['permanentId'].strip(),
             "mobile": request.get_json()['mobile'].strip(),
             "employeeId": request.get_json()['employeeId'].strip(),
             "purpose": request.get_json()['purpose'].strip(),
             "ownerFlatNo": request.get_json()['ownerFlatNo'].strip(),
             "status": request.get_json()['status'].strip(),
             "startDate": request.get_json()['startDate'].strip(),
             "endDate": request.get_json()['endDate'].strip(),
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))
            }]
            x = dic['guest'].insert_many(myUserJson)
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
@Guest_Information.route('/api/guestList', methods=['GET'])
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
        task = dumps(dic['guest'].find(myquery))
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


