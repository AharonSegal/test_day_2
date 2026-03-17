# -------------------
# | RAW QUERIES     |
# -------------------

# 1: 
hight priority target movement over 5 km
---
filters priority (1,2)
filters movement > 5
show in descending order
---
SELECT entity_id ,target_name ,priority_level ,movement_distance_km
FROM targets 
WHERE priority_level IN (1, 2)
AND movement_distance_km > 5
ORDER BY movement_distance_km 
DESC

# 2:
show count of each signal type 
---
SELECT signal_types
GROUP them into their basic values
COUNT how many in each group
ORDER them in DESC order
---
SELECT signal_type, COUNT(*) as count_intel_types
FROM intel_signals
GROUP BY signal_type 
ORDER BY count_intel_types 
DESC 

# 3:
3 most appearing UNKNOWN entity 
---
clarify
    based on simulation.py -> unknown_entity is generated for attack,damage,intel 
    rather than -> TGT-015
    unknown entity -> TGT-UNKNOWN-103
    so even though im not seeing UNKNOWN in the targets table i think it can be there 
    cause in the code yesterday i only validated that it was a str 
    but maybe i was supposed to validate a clearer format
    so for this query i will include the targets table (even thought it dosent have any)
---
simplified on one table
    SELECT entity_id, COUNT(*) AS id_count
    FROM intel_signals 
    WHERE entity_id LIKE 'TGT-UNKNOWN%'
    GROUP BY entity_id 
    ORDER BY id_count 
    DESC 
    LIMIT 3
---
merge all to one subquery
on that sub do like the simplified 
---
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
SELECT entity_id, COUNT(*) AS id_count
FROM all_unknowns 
GROUP BY entity_id 
ORDER BY id_count 
DESC 
LIMIT 3