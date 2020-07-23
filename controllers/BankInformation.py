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
Bank_Information = Blueprint('Bank_Information', __name__,
                           template_folder='templates')
@Bank_Information.route('/api/bankInformation', methods=['POST'])
def paymentInformationInital():
    try:
        dic = Dbconnection.DBConnection()
        apartmentId="ADADA"
        username = "kumar"
        today = datetime.now()
        myquery = {'apartmentId': apartmentId,"accountNumber": request.get_json()['accountNumber'].strip()}
        mydoc = dic['paymentInformation'].find(myquery)
        print(mydoc.count())
        if mydoc.count() != 0:
            myUserJson={
            "$set":{
                  "apartmentId": apartmentId,
                  "accountNumber": request.get_json()['accountNumber'].strip(),
                  "ifscCode": request.get_json()['ifscCode'].strip(),
                  "bankName": request.get_json()['bankName'].strip(),
                  "bankAddress": request.get_json()['bankAddress'].strip(),
                  "branchName": request.get_json()['branchName'].strip(),
                  "pincode": request.get_json()['pincode'].strip(),
                  "city": request.get_json()['city'].strip(),
                  "state1": request.get_json()['state1'].strip(),
                  "country": request.get_json()['country'].strip(),
                  "ownerName": username,
                  "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 

             }
            }
            dic['paymentInformation'].update_one(myquery,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            myUserJson= [{
             "apartmentId": apartmentId,
             "accountNumber": request.get_json()['accountNumber'].strip(),
             "ifscCode": request.get_json()['ifscCode'].strip(),
             "bankName": request.get_json()['bankName'].strip(),
             "bankAddress": request.get_json()['bankAddress'].strip(),
             "branchName": request.get_json()['branchName'].strip(),
             "pincode": request.get_json()['pincode'].strip(),
             "city": request.get_json()['city'].strip(),
             "state1": request.get_json()['state1'].strip(),
             "country": request.get_json()['country'].strip(),
             "ownerName": username,
             "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['paymentInformation'].insert_many(myUserJson)
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
@Bank_Information.route('/api/bankInformationList', methods=['GET'])
#@auth.login_required
def bankInformationList():
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
        task = dumps(dic['paymentInformation'].find(myquery))
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


@Bank_Information.route('/api/upload', methods=['POST'])
def upload_file():
   print (request.files)
   print (request.form['depositAmount'])
   dic = Dbconnection.DBConnection()
   apartmentId = "ADADA"
   user = "kumar"
   today = datetime.now()
   statementName=apartmentId + str('-bankStatements-')+str(today.strftime('%Y-%m-%d-%H-%M-%S'))+".jpg"
   myquery = {'apartmentId': apartmentId,'username': user}
   mydoc = dic['bankBalanceInformation'].find(myquery)
   myquery1 = {'apartmentId': apartmentId,'ownerName': user,"latestValue": 1}
   mydoc1 = dic['bankBalanceInformation'].find(myquery1)
   task = dumps(mydoc1)
   res = json.dumps(task)
   print(res)
   res1=json.loads(res).strip('[]')
   res2=eval(res1)
   currentAmount=res2.get('currentAmount')
   totalAmount=res2.get('totalAmount')
   print(currentAmount)
   if mydoc1.count != 0:
            myUserJson= {"$set":{
             "latestValue": 0,
             }
             }
            dic['bankBalanceInformation'].update_one(myquery1,myUserJson)
   user="kumar"
   if user == '':
       task = {'status': 'Redirect to login page'}
       return jsonify(task)
   if not os.path.exists("/tmp/inventory/"):
       os.makedirs("/tmp/inventory/")
   if not os.path.exists("/tmp/inventory/{}".format(apartmentId)):
       os.makedirs("/tmp/inventory/{}".format(apartmentId))
   if not os.path.exists("/tmp/inventory/{}/{}".format(apartmentId,"bankStatements")):
       os.makedirs("/tmp/inventory/{}/{}".format(apartmentId,"bankStatements"))
   if 'file' not in request.files:
       return "No file found"
   else:
       file = request.files['file']
       file.save("/tmp/inventory/{}/bankStatements/{}".format(apartmentId,statementName))
   if mydoc.count != 0:
            myUserJson= [{
             "depositAmount": request.form['depositAmount'].strip(),
             "currentAmount": str(int(currentAmount)+ int(request.form['depositAmount'].strip())),
             "totalAmount": str(int(totalAmount)+ int(request.form['depositAmount'].strip())),
             "statementName": statementName,
             "amountType": request.form['amountType'].strip(),
             "ownerName": user,
             "depositOwnerFlatNo": request.form['depositOwnerFlatNo'].strip(),
             "apartmentId": apartmentId,
             "latestValue": 1,
             "statementDate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
             }]
            x =  dic['bankBalanceInformation'].insert_many(myUserJson)
            task = {'status': 'Success',"message":"Sucessfully Update"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
   
   task = {'status': 'Sucessfully updated record'}
   return jsonify(task)
@Bank_Information.route('/api/bankStatementInformationList', methods=['GET'])
#@auth.login_required
def bankStatementInformationList():
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
        task = dumps(dic['bankBalanceInformation'].find(myquery))
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
@Bank_Information.route('/api/ownerPaymentInformationList', methods=['GET'])
#@auth.login_required
def ownerPaymentInformationList():
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
    myquery = {'apartmentId': apartmentId,'depositOwnerFlatNo':'310'}
    print(session)
    print(str(user))
    if user == '':
        task = {'status': 'Redirect to login page'}
        return jsonify(task)
    try:
        dic = Dbconnection.DBConnection()
        task = dumps(dic['bankBalanceInformation'].find(myquery))
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
@Bank_Information.route('/api/download/<fileName>', methods=['GET'])
#@Api_Controller.route('/api/deleteInventory', methods=['DELETE'])
#def delete():
def downloadFile(fileName):
    apartmentId="ADADA"
    print(fileName)
    path="/tmp/inventory/"+apartmentId+"/bankStatements/"+fileName
    
    print(path)
    return send_file("/tmp/inventory/{}/bankStatements/{}".format(apartmentId,fileName),
                     mimetype='jpg',
                     attachment_filename='{}'.format(fileName),
                     as_attachment=True)



