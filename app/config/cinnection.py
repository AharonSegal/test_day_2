from app.config.mysql_connection import MySQLClient

host = "localhost"
port = 3306
user= "root"
password = "root_pwd"
database = "digital_hunter"

client = MySQLClient(host, port, user, password, database)