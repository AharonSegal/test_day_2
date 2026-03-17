# -------------------
# | RAW QUERIES     |
# -------------------

# 1: 
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
SELECT signal_types
GROUP them into their basic values
COUNT how many in each group
ORDER them in DESC order

SELECT signal_type, COUNT(*) as count_intel_types
FROM intel_signals
GROUP BY signal_type 
ORDER BY count_intel_types 
DESC 
