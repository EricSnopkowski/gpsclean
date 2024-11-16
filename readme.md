# CleanDb

This is a python script to cleanup gps positions in a mariadb database.
If a gps point is a range of 50m of the last point it will be deleted.
So only points >50m distance will remain in the database. 
Use the requirements.txt file to load modules : pip install -r requirements.txt

parameters needs to be set a .env file like this :
MARIADB_HOST=xxx.xxx.xxx.xxx
MARIADB_USER=root
MARIADB_PASSWORD=12345
MARIADB_DATABASE=data

