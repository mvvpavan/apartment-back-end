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
Apartment_Equipment = Blueprint('Apartment_Equipment', __name__,
                           template_folder='templates')
@Apartment_Equipment.route('/api/equipmentInfomation', methods=['POST'])
def equipmentInfomation():
        dic = Dbconnection.DBConnection()
        apartmentId="ADADA"
        username = "kumar"
        today = datetime.now()
        myquery = {'apartmentId': apartmentId,"equipmentId": request.get_json()['equipmentId'].strip()}
        mydoc = dic['equipment'].find(myquery)
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
        if int(currentAmount) < int(request.get_json()['equipmentPrice'].strip()):
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
            equipmentPrice=res2.get('equipmentPrice')
            updateAmount=int(currentAmount)+int(equipmentPrice)
            myUserJson1={
              "$set":{
                  "apartmentId": apartmentId,
                  "currentAmount": str(int(updateAmount)-int(request.get_json()['equipmentPrice'].strip()))

             }
            }
            dic['bankBalanceInformation'].update_one(myquery1,myUserJson1)
            myUserJson={
            "$set":{
                  "apartmentId": apartmentId,
                  "equipmentId": request.get_json()['equipmentId'].strip(),
                  "equipmentName": request.get_json()['equipmentName'].strip(),
                  "equipmentPrice": request.get_json()['equipmentPrice'].strip(),
                  "equipmentType": request.get_json()['equipmentType'].strip(),
                  "ownerid": username,
                  "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 

             }
            }
            dic['equipment'].update_one(myquery,myUserJson)
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
                  "currentAmount": str(int(currentAmount)-int(request.get_json()['equipmentPrice'].strip()))

             }
            }
            dic['bankBalanceInformation'].update_one(myquery1,myUserJson1)
            myUserJson= [{
              "apartmentId": apartmentId,
              "equipmentId": request.get_json()['equipmentId'].strip(),
              "equipmentName": request.get_json()['equipmentName'].strip(),
              "equipmentPrice": request.get_json()['equipmentPrice'].strip(),
              "equipmentType": request.get_json()['equipmentType'].strip(),
              "ownerid": username,
              "createOrUpdate": str(today.strftime('%Y-%m-%d %H:%M:%S')) 
            }]
            x = dic['equipment'].insert_many(myUserJson)
            task = {'status': 'Success',"message":"Sucessfully Update"}
            res = json.dumps(task)
            res1=json.loads(res)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

@Apartment_Equipment.route('/api/equipmentInformationList', methods=['GET'])
def equipmentInformationList():
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
        task = dumps(dic['equipment'].find(myquery))
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