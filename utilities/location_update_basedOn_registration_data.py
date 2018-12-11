#this is for windows
#import MySQLdb as mysql
import mysql.connector as mysql
import csv
import datetime
from operator import itemgetter


def fetch_customer_from_custList(cust_id, cust_list):
    for i in range(len(cust_list)):
        if cust_id == cust_list[i][0]:
            return cust_list[i]
    return 0

    
def neighbour_list_update(cursor, custormer, cust_list,amount):
    neighbours = []
    distances= []
    print(customer)
    cust_id = customer[0]
    for i in range(len(cust_list)):
        lat_diff = abs(float(customer[2]) -float(cust_list[i][2]))
        lng_diff = abs(float(customer[3]) -float(cust_list[i][3]))
        dist = lat_diff + lng_diff
        dist_rec = [cust_list[i][0],dist]
        distances.append(dist_rec)
    distances = sorted(distances, key=itemgetter(1))
    neighbours = [x[0] for x in distances]
    neighbours = neighbours[:amount]
    neighbour_list = ""
    for ele in neighbours:
        neighbour_list += str(ele) + ","
    neighbour_list = neighbour_list[:-1]        
    print(cust_id, neighbour_list)        
    cursor.execute("UPDATE locations_locations SET neighbours=%s WHERE id=%s", (neighbour_list,cust_id))


def update_radio_data(cursor,cust, reg_list,field_id):
    reg_data = []
    cust_id = cust[0]
    cust_name = cust[1]
    for reg in reg_list:
        try:
            if cust_name == reg[field_id].lower().strip():
                if(int(reg[5]) !=0):
                    temp= [reg[0],reg[1],reg[2],reg[5],reg[6],reg[7], reg[8], reg[11]]
                    reg_data.append(temp)
        except:
            continue
    active_rec = []        
    if len(reg_data) > 0 :
        now = datetime.datetime.now()
        time_stamp = str(now.year) + '-' + str(now.month) + '-' + str(now.day)  + ' ' + str(now.hour)  + ':'  + str(now.minute) + ':00'
        try:
            active_rec = reg_data[-1:][0]
#            print(reg_data)
            print("active rec", active_rec[3])        
#            sql = "select * from  locations_locations where id='"+str(cust_id) + "';"
#            cursor.execute(sql)
#            active_cust = cursor.fetchone()
            if int(active_rec[3]) != 0:
                print('here', int(active_rec[3]))
                cursor.execute("UPDATE locations_locations SET ap_id=%s,rssi=%s, snr=%s, ccq_tx=%s, ccq_rx=%s, created_time=%s, updated_time=%s WHERE id=%s", (active_rec[2], active_rec[3],active_rec[4],active_rec[5],active_rec[6],active_rec[7],time_stamp,cust_id))
                #print("{0} record is updated. RSSI value {1}".format(cust_name, active_record[3]))
                print("{0} record is updated with correct RSSI value {1}".format(cust_name,active_rec[3]))
            else:
                print("{0} record is not updated due to RSSI value {1}".format(cust_name, active_rec[3]))
        except:
            print("{0} Update Error".format(cust_name))
    return active_rec


# running system
#conn = mysql.connect(user='root', password='...',host='.....',database='.....',  use_unicode=True, charset="utf8")
conn = mysql.connect(user='root', password='....',host='.....',database='.....',  use_unicode=True, charset="utf8")
cursor = conn.cursor()        

sql_loc = "select * from  locations_locations;"
#with runnning system
#sql_reg = "select * from  routcom.registrations_registrations;"
sql_reg = "select * from  registrations;"

cursor.execute(sql_loc)
customers = cursor.fetchall()
cust_list = []
for c in customers:
    cust_list.append([c[0],c[9],c[10],c[11]])


    
cursor.execute(sql_reg)
registrations = cursor.fetchall()    

count =0 
reg_list = []



for customer in cust_list:
    result = update_radio_data(cursor, customer, registrations, 1)
    #neighbour_list_update(cursor, customer, cust_list, 15)

cust_id = 1

#sql = "select * from locations_locations where id='"+str(cust_id)+"';"
#print(sql)
#cursor.execute(sql)
#customer = cursor.fetchone()
#print(customer)

#customer = fetch_customer_from_custList(cust_id,cust_list)

#neighbour_list_update(cursor, customer, cust_list, 15)




conn.commit()
cursor.close()
print("Done")         
