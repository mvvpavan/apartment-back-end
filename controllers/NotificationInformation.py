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
import cv2
import pytesseract

Notification_Information = Blueprint('Notification_Information', __name__,
                           template_folder='templates')
@Notification_Information.route('/api/notificationInformation', methods=['POST'])
def notificationInformation():
    try:
        dic = Dbconnection.DBConnection()
        today = datetime.now()
        #apartmentId = session.get('apartmentId')
        apartmentId="ADADA"
        text=''
        statementName=apartmentId + str('-notificationStatements-')+str(today.strftime('%Y-%m-%d-%H-%M-%S'))+".jpg"
        print(apartmentId)
        if request.form['description'] == "":
           if not os.path.exists("/tmp/inventory/"):
                os.makedirs("/tmp/inventory/")
           if not os.path.exists("/tmp/inventory/{}".format(apartmentId)):
                os.makedirs("/tmp/inventory/{}".format(apartmentId))
           if not os.path.exists("/tmp/inventory/{}/{}".format(apartmentId,"notification")):
                 os.makedirs("/tmp/inventory/{}/{}".format(apartmentId,"notification")) 
           if 'file' not in request.files:
               return "No file found"
           else:
              file = request.files['file']
              file.save("/tmp/inventory/{}/notification/{}".format(apartmentId,statementName))
              path="/tmp/inventory/{}/notification/{}".format(apartmentId,statementName)
              img=cv2.imread(path)
              text=pytesseract.image_to_string(img)
              print(text)
        else:
            text=request.form['description']
        myquery1 = { 'apartmentId': apartmentId,'notificationId': request.form['notificationId'].strip()}
        mydoc1 = dic['notificationInformation'].find(myquery1)
        if mydoc1.count() != 0:
            myUserJson={
             "$set":{
              "notificationId": request.form['notificationId'].strip(),
              "description": text.strip()
             }
             }
            dic['notificationInformation'].update_one(myquery1,myUserJson)
            task = {'status': 'Successfull updated'}
            res2 = json.dumps(task)
            res1=json.loads(res2)
            response=make_response(res1,200)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
           
        else:
            myquery2 = {'apartmentId': apartmentId,"latestValue": 1}
            mydoc2 = dic['notificationInformation'].find(myquery2)
            if mydoc1.count != 0:
               myUserJson2= {"$set":{
                 "latestValue": 0,
                }
               }
               dic['notificationInformation'].update_one(myquery2,myUserJson2)
            myUserJson= [{
             "apartmentId": apartmentId,
             "notificationId":request.form['notificationId'].strip(),
             "description": text.strip(),
             "latestValue":1,
             "createDate": str(today.strftime('%Y-%m-%d %H:%M:%S'))
            }]
            x = dic['notificationInformation'].insert_many(myUserJson)
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
@Notification_Information.route('/api/pushNotificationInformation', methods=['POST'])
def pushNotificationInformation():
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
              "status": request.get_json()['status']
              }
             }
             }
            dic['notificationInformation'].update_one(myquery1,myUserJson)
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
@Notification_Information.route('/api/notificationList', methods=['GET'])
#@auth.login_required
def notificationList():
    """
    This function responds to a request for /api/Inventory
    with the complete lists of Inventory
    :return:        sorted list of Inventory
    """

    # Create the list of Inventory from our data
    # return jsonify(INVENTORY)
    #user = session.get('username')
    #apartmentId = session.get('apartmentId')
    apartmentId="ADADA"
    myquery = {'apartmentId': apartmentId}
    #print(session)
    #print(str(user))
    #if user == '':
     #   task = {'status': 'Redirect to login page'}
     #   return jsonify(task)
    try:
        dic = Dbconnection.DBConnection()
        task = dumps(dic['notificationInformation'].find(myquery))
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


