import re
import collections
import sys
import os
import numpy as np
import datetime
#this is for windows
import MySQLdb as mysql
#import mysql.connector as mysql
import json
import glob
import csv

#this is for windows
#conn = mysql.connect(user='root', password='dupa@123',host='127.0.0.1',database='scraper',  use_unicode=True, charset="utf8")
conn = mysql.connect(user='root', password='dupa@123',host='127.0.0.1',database='routcom',  use_unicode=True, charset="utf8")
cursor = conn.cursor()        

sql = "select * from locations_locations"
cursor.execute(sql)
row = cursor.fetchall()
for r in row:
    print(r)

cust_type = 'active'
sitesurvey_ok = '0'
comments = 'existing customer'

total = 0
with open('./customerlistwith_geo.csv', 'r', newline='\n') as csvfile:
    cfile = csv.reader(csvfile, delimiter='|')
    headers = next(cfile, None) 
    for line in cfile:
        name = line[0]
        address1 = line[1]
        address2 = line[2]
        city =line[3]
        province = line[4]
        postalcode = line[5]
        country = line[6]
        winbox = line[7]
        lat = line[9]
        lng = line[10]
        values = "'"+ name+"','"+ address1+"','"+address2+"','"+city+"','"+province+"','"+postalcode+"','"+country+"','"+cust_type+"','"+ winbox+"','"+lat+"','"+lng+"','"+sitesurvey_ok+"','"+ comments +"'"
      #  print(values)
        try:
            #sql = "insert into locations_locations (name,address1,address2,city,province,postalcode,country,cust_type, winbox,lat,lng,sitesurvey_ok, comments) values(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
            sql = "insert into locations_locations (name,address1,address2,city,province,postalcode,country,cust_type, winbox,lat,lng,sitesurvey_ok, comments) values("+values+")"
            print(sql)
            cursor.execute(sql)
            total+=1
        except:
            #print('error updating', line)
            continue
cursor.execute('COMMIT')        
print("successfully uploaded {0} records".format(total))        
