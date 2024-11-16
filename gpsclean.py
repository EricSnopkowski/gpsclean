
#First download dependicies, see requierments.txt
#sudo apt install libmariadb3 libmariadb-dev
#pip install mariadb
#more info at https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
import mariadb
from dotenv import load_dotenv  
import os  
from geopy.distance import geodesic
from datetime import datetime

#Input parameters
load_dotenv()  # take environment variables
maxdiff = 50  #max difference in meters
who = "SS"  #witch person
#Variables definition
totalpoints = 0
mlat=0
mlon=0
mdiff=0
deletedpoints=0

#Connect to MariaDB read and loop
try:
    conn = mariadb.connect(
        user=os.getenv('MARIADB_USER'),
        password=os.getenv('MARIADB_PASSWORD'),
        host=os.getenv('MARIADB_HOST'),
        database=os.getenv('MARIADB_DATABASE'))
    readdb = conn.cursor()
except mariadb.Error as e:
                print(f"Failed to connect to MariaDB for reading: {e}")
                exit()
#Connect to MariaDB
try:
    conn2 = mariadb.connect(
        user=os.getenv('MARIADB_USER'),
        password=os.getenv('MARIADB_PASSWORD'),
        host=os.getenv('MARIADB_HOST'),
        database=os.getenv('MARIADB_DATABASE'))
    updatedb = conn2.cursor()
except mariadb.Error as e:
                print(f"Failed to connect to MariaDB for updating: {e}")
                exit()

#Load selected data from MariaDB
readdb.execute("SELECT lat,lon,timestamp2 FROM owntracks WHERE  timestamp2 >= '2024-08-04 0:00' AND timestamp2 <= '2024-08-04 23:59' and name = '" + who + "' ORDER BY name,timestamp2")

#Loop thoug data
for (lat,lon,timestamp2) in readdb:
   totalpoints = totalpoints +1
   #at first point save basepoint
   if totalpoints == 1:
      mlat = lat
      mlon = lon
   #at next points calculate distance to basepoint
   else:
      basepoint = (mlat, mlon)
      nextpoint = (lat, mlon)
      mdiff = geodesic(basepoint, nextpoint).meters
      #if diff is less then mark point for deletion
      if mdiff < maxdiff:
         deletedpoints = deletedpoints + 1
         try:
             updatedb.execute("UPDATE owntracks SET name = '" + who + "del' WHERE timestamp2 = '" + f"{timestamp2:%Y-%m-%d %H:%M:%S%z}" + "' AND name = '"+ who +"'")
         except mariadb.Error as e2:
             print(f"Failed to update db: {e2}")
             exit()
      #if diff is more do nothing and use current point as new basepoint
      else:
         mlat = lat
         mlon = lon
   print(timestamp2, end="\r")
print('Total GPS point found :', totalpoints)
print('Points marked for deletion :', deletedpoints,'(',deletedpoints/totalpoints*100,'%)')

#Close MariaDB connections
conn2.commit()
conn.close()
conn2.close()
