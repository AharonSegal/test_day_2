from app.config.mysql_connection import MySQLClient

host = "localhost"
port = 3306
user= "root"
password = "root_pwd"
database = "digital_hunter"

client = MySQLClient(host, port, user, password, database)

def query_1(mysql_client):
    sql = """
        SELECT entity_id ,target_name ,priority_level ,movement_distance_km
        FROM targets 
        WHERE priority_level IN (1, 2)
        AND movement_distance_km > 5
        ORDER BY movement_distance_km 
        DESC
    """.strip()
    return mysql_client.fetch_all(sql)

test = query_1(client)
print(test)