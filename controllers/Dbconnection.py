#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pymongo
def DBConnection():
    try:
        dic = dict();  
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['apartment']
        dic['admin'] = mydb['adminRegister']
        dic['user'] = mydb['userRegister']
        dic['guest'] = mydb['guestRegister']
        dic['paymentInformation'] = mydb['paymentInformation']
        dic['bankBalanceInformation'] = mydb['bankBalanceInformation']
        dic['equipment'] = mydb['equipment']
        dic['employeePayment'] = mydb['employeePayment']
        dic['employee'] = mydb['employee']
        dic['eventId'] = mydb['eventId'] 
        dic['eventMaintenance'] = mydb['eventMaintenance'] 
        dic['notificationInformation'] = mydb['notificationInformation'] 
        dic['electionInformation'] = mydb['electionInformation']
        dic['parkingAllotment'] = mydb['parkingAllotment'] 
        dic['vehicalInforamtion'] = mydb['vehicalInforamtion'] 
        dic['parkingRequest'] = mydb['parkingRequest'] 
        return dic
    except pymongo.errors.ConnectionFailure as e:
        print ('Could not connect to server: %s', e)