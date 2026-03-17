import mysql.connector

class MySQLClient:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "localhost",
            port = 3306,
            user= "root",
            password = "root_pwd",
            database = "digital_hunter",
            connection_timeout=5
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()

client = MySQLClient()

class DAL:

    def get_high_priority_targets(self):
        """Fetch high priority targets (level 1-2) with movement over 5 km"""
        sql = """
            SELECT 
                entity_id,
                target_name,
                priority_level,
                movement_distance_km
            FROM targets 
            WHERE priority_level IN (1, 2)
                AND movement_distance_km > 5
            ORDER BY movement_distance_km DESC
        """.strip()
        return client.fetch_all(sql)

    def count_signal_types(self):
        """Show count of each signal type"""
        sql = """
            SELECT 
                signal_type, 
                COUNT(*) as count_intel_types
            FROM intel_signals
            GROUP BY signal_type 
            ORDER BY count_intel_types DESC 
        """.strip()
        return client.fetch_all(sql)
    
    def most_entity(self):
        """3 most appearing UNKNOWN entity"""
        sql = """
            WITH all_unknowns AS (
                SELECT entity_id FROM attacks 
                WHERE entity_id LIKE 'TGT-UNKNOWN%'
                UNION ALL 
                SELECT entity_id FROM intel_signals 
                WHERE entity_id LIKE 'TGT-UNKNOWN%'
                UNION ALL 
                SELECT entity_id FROM damage_assessments 
                WHERE entity_id LIKE 'TGT-UNKNOWN%'
                UNION ALL 
                SELECT entity_id FROM targets 
                WHERE entity_id LIKE 'TGT-UNKNOWN%'
            )
            SELECT 
                entity_id, 
                COUNT(*) AS id_count
            FROM all_unknowns 
            GROUP BY entity_id 
            ORDER BY id_count DESC LIMIT 3
        """.strip()
        return client.fetch_all(sql)
    
    def day_night_distance(self):
        """this gave for each id the sum day and a row with id for sum night
            but no entity was twice cause the edited all becae night 

            i need to procede so i will consider this working for now 
            and not mod the data for better testing 
            #TODO: CONTINUE
        """
        sql = """
        WITH seperate_day_night AS (
        SELECT 
        entity_id, 
        timestamp, 
        distance_from_last,
        CASE
            WHEN HOUR(timestamp) >= 8
            AND  HOUR(timestamp) < 20
            THEN 'day'
            ELSE 'night'
        END AS day_or_night
        FROM intel_signals
    ),

    entity_sum AS (
        SELECT 
            entity_id, 
            day_or_night, 
            SUM(distance_from_last) AS total_dist
        FROM seperate_day_night
        GROUP BY entity_id, day_or_night
    )

    SELECT * FROM entity_sum;
        """.strip()
        return client.fetch_all(sql)
    

    
    def get_cors_by_time(self,entity_id: str):
        """
        returns a list of tuple coordinates [(lat,lon)...]
        """
        sql = """
        SELECT reported_lat, reported_lon 
        FROM intel_signals 
        WHERE entity_id = %s
        ORDER BY `timestamp` 
        """.strip()
        return [client.fetch_all(sql, [entity_id])]
    
# dal = DAL()
# lst_dat = dal.get_cors_by_time('TGT-006')
# for x in lst_dat:
#     print(x)
    