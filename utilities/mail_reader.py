import email
import poplib
import email.parser
import mysql.connector as mysql
#for windows
#import MySQLdb as mysql

import csv
import googlemaps


gmaps = googlemaps.Client(key='AIzaSyD6l2HKrp-1hDGftsxeasdiN4yr9Lg78Tw')

def fetchAddress(address):
    try:
        geocode_result = gmaps.geocode(address)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
    except Exception:
        lat = 0.0
        lon = 0.0
        print("lat", lat, "lon", lon)
        return lat, lon

    print("lat", lat, "lon", lon)
    return lat, lon



conn = mysql.connect(user='root', password='dupa@123',host='127.0.0.1',database='scraper',  use_unicode=True, charset="utf8")
#production database
#conn = mysql.connect(user='root', password='dupa@123',host='127.0.0.1',database='routcom',  use_unicode=True, charset="utf8")
cursor = conn.cursor()        




subject_phrase = "Site Survey Request:"
invalid_str = "http:"

def site_surveys(item):
    #print(item['subject'], item['message'])
    mesg = item['message']
    #print('messssage', mesg)
    valid = True
    for e in mesg:
        if invalid_str in e.strip().lower():
            valid = False
            print("found invalid string (http...)", e)
    #print('valid', valid, len(mesg))
    if valid and mesg and mesg[1] and len(mesg) > 13:
        if mesg[1]:
            name = mesg[1]
        else:
            valid = False
        if mesg[3]:
            address = mesg[3]
        else:
            valid = False
        if mesg[5]:    
            city = mesg[5]
        else:
            valid = False
        if mesg[7]:
            postalcode = mesg[7]
        else:
            valid = False
        if mesg[9]:
            phone = mesg[9]
        else:
            valid = False
        if mesg[11]:
            email = mesg[11]
        else:
            valid = False
        if mesg[13]:
            comment = mesg[13]
            if len(comment) > 500:
                comment = comment[:499]
        else:
            valid = False
        
        province = "ON"
        country = "Canada"
        cust_type = "site_survey_waiting"
        contact = name + ',' + address + ',' + city + ',' + province + ',' + country + ',' + postalcode + ',' + phone + ',' + email + ',' + comment
        
        
        if valid:
            sql = "select * from locations_locations where name='"+ name.strip() + "'"
            cursor.execute(sql)
            row = cursor.fetchall()
            print('length', len(row))
            if len(row) == 0:
                geo_data = address + ',' + city + ',' + province + ',' + country + ',' + postalcode
                lat, lng = fetchAddress(geo_data)
                print(contact, lat,lng)

                sql = "insert into locations_locations (name, address1, city, province, postalcode,country, lat, lng,cust_type, comments) values ('"+name.strip() +"','" +address+ "','" +city+"','" +province+"','" +postalcode+"','" + country+"','" +str(lat)+"','" +str(lng)+"','"+ cust_type+"','" + comment + "')"
                print(sql)
                cursor.execute(sql)
                #print('added',name)
                cursor.execute('COMMIT')
                sql = "select * from locations_locations where name='"+name.strip() + "'"
                cursor.execute(sql)
                row = cursor.fetchone()
                #print('row details', row[0][0])
                print("successfully updated a record:>", name)
            else:
                print("records is already in the database:>", name)            
        else:
            print("invalid field values ")
    else:
        print("invalid content")
      



SERVER = "mail.routcom.com"   
USER = "sitesurvey_forward@routcom.com"
PASSWORD = "Dupa@9058336774"
 

server = poplib.POP3(SERVER)
server.user(USER)
server.pass_(PASSWORD)


numMessages = len(server.list()[1])

message_list  = []

for i in range(numMessages) :
    message = []
    subject = ""
    (server_msg, body, octets) = server.retr(i+1)
    for j in body:
        try:
            msg = email.message_from_string(j.decode("utf-8"))
            if msg['Subject']:
                subject = msg['Subject']
                break
        except:
            pass
    
    
    if subject_phrase in subject:
        print('valid subject: >',subject)
        for j in body:
            try:
                msg = email.message_from_string(j.decode("utf-8"))
                strtext=msg.get_payload()
                if len(strtext) > 0:
                    message.append(strtext)
            except:
                pass
        message_item = {}
        message_item['subject'] = subject
        message_item['message'] = message
        message_list.append(message_item)
        site_surveys(message_item)
    else:
        print("invalid subject: >", subject)
        




