import mysql.connector as mysql
import csv



conn = mysql.connect(user='root', password='.....',host='.....',database='.....',  use_unicode=True, charset="utf8")
cursor = conn.cursor()        


f = open('registrations.csv','r')
reader = csv.reader(f, delimiter = ';')
header = next(reader, None)

header_str = ''
for i in range(1,len(header)):
    if i < len(header) - 1:
        header_str+= "`"+ header[i]+"`,"
    else:
        header_str+= "`"+ header[i]+"`"

for row in reader:
    try:
        line = ""
        for i,r in enumerate(row):
            if i >0 and i < len(row) -1:
                line += "'"+ r + "',"
            elif i > 0:
                line += "'"+ r + "'"
        if len(line) > 0:            
            sql = "insert into scraper.registrations("+header_str+") values (" + line+ ");"
            cursor.execute(sql)
    except:
        print('something went wrong')
        continue            


conn.commit()
cursor.close()
print("Done")    
