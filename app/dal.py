from app.config.cinnection import client

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