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
Employee_Information = Blueprint('Employee_Information', __name__,
                           template_folder='templates')
@Employee_Information.route('/api/employeePaymentInformation', methods=['POST'])
def employeePaymentInformation():
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
             "username": request.get_json()['username'].strip(),
             "password": f.encrypt(bytes(request.get_json()['password'].strip())),
             "employeeId": request.get_json()['employeeId'],
             "employeeAddress": request.get_json()['employeeAddress'],
             "pincode": request.get_json()['pincode'],
             "state": request.get_json()['state'],
             "nationality": request.get_json()['nationality'],
             "employeeIdProof": request.get_json()['employeeIdProof'],
             "emailId": request.get_json()['emailId'].strip(),
             "mobile": request.get_json()['mobile'].strip(),
             "altmobile": request.get_json()['altmobile'].strip(),
             "occupation": request.get_json()['occupation'].strip(),
             "type": request.get_json()['type'].strip(),
             "status": request.get_json()['status'].strip(),
             "startDate": request.get_json()['startDate'].strip(),
             "endDate": request.get_json()['endDate'].strip(),
             "key": key,
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))

             }
            }
            dic['equipment'].update_one(myquery1,myUserJson)
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
             "username": request.get_json()['username'].strip(),
             "password": f.encrypt(bytes(request.get_json()['password'].strip())),
             "employeeId": request.get_json()['employeeId'],
             "employeeAddress": request.get_json()['employeeAddress'],
             "pincode": request.get_json()['pincode'],
             "state": request.get_json()['state'],
             "nationality": request.get_json()['nationality'],
             "employeeIdProof": request.get_json()['employeeIdProof'],
             "emailId": request.get_json()['emailId'].strip(),
             "mobile": request.get_json()['mobile'].strip(),
             "occupation": request.get_json()['occupation'].strip(),
             "type": request.get_json()['type'].strip(),
             "status": request.get_json()['status'].strip(),
             "startDate": request.get_json()['startDate'].strip(),
             "endDate": request.get_json()['endDate'].strip(),
             "key": key,
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['employee'].insert_many(myUserJson)
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
@Employee_Information.route('/api/employeeInformation', methods=['POST'])
def employeeInformation():
        dic = DBConnection()
        apartmentId="ADADA"
        username = "kumar"
        today = datetime.now()
        myquery = {'apartmentId': apartmentId,"employeeId": request.get_json()['employeeId'].strip()}
        mydoc = dic['employeePayment'].find(myquery)
        myquery1 = {'apartmentId': apartmentId,'ownerName': username,"latestValue": 1}
        mydoc1 = dic['bankBalanceInformation'].find(myquery1)
        if mydoc1.count() == 0:
            task = {'status': 'Failed',"message":"Insufficent balance"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,402)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        task = dumps(mydoc1)
        res = json.dumps(task)
        res1=json.loads(res).strip('[]')
        res2=eval(res1)
        currentAmount=res2.get('currentAmount')
        print(currentAmount)
        if int(currentAmount) < int(request.get_json()['employeePayment'].strip()):
            task = {'status': 'Failed',"message":"Insufficent balance"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,402)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        print(currentAmount)
        if mydoc.count() != 0:
            task1 = dumps(mydoc)
            res = json.dumps(task1)
            res1=json.loads(res).strip('[]')
            res2=eval(res1)
            equipmentPrice=res2.get('employeePayment')
            updateAmount=int(currentAmount)+int(equipmentPrice)
            myUserJson1={
              "$set":{
                  "apartmentId": apartmentId,
                  "currentAmount": str(int(updateAmount)-int(request.get_json()['employeePayment'].strip()))

             }
            }
            dic['bankBalanceInformation'].update_one(myquery1,myUserJson1)
            myUserJson={
            "$set":{
              "apartmentId": apartmentId,
              "employeeId": request.get_json()['employeeId'].strip(),
              "employeePayment": request.get_json()['employeePayment'].strip(),
              "employeePaymentDate": request.get_json()['employeePaymentDate'].strip(),
              "ownerid": username,
              "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 

             }
            }
            dic['employeePayment'].update_one(myquery,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            myUserJson1={
              "$set":{
                  "apartmentId": apartmentId,
                  "currentAmount": str(int(currentAmount)-int(request.get_json()['employeePayment'].strip()))

             }
            }
            dic['bankBalanceInformation'].update_one(myquery1,myUserJson1)
            myUserJson= [{
              "apartmentId": apartmentId,
              "employeeId": request.get_json()['employeeId'].strip(),
              "employeePayment": request.get_json()['employeePayment'].strip(),
              "employeePaymentDate": request.get_json()['employeePaymentDate'].strip(),
              "ownerid": username,
              "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['employeePayment'].insert_many(myUserJson)
            task = {'status': 'Success',"message":"Sucessfully Update"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


