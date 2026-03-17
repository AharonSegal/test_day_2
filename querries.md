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

# 4
day or night was static
--- 
il be using the signal table
classify for each if day or night - HOUR() Function

IF intel_hour IS BETWEEN 8 AND 20 then its day
ELSE night

then for each entity_id sort to 2 groups (day,night)

for each entity sum its day and night cols
use distance_from_last_field (new col)
each entity is one line now with hte sum of distsnce day and sistance night 
filter al that have 
for day check if distance = 0
for night check if distance > 10
---
step 1: seperate day and night
WITH seperate_day_night AS (
SELECT entity_id ,timestamp,
CASE
	WHEN HOUR(timestamp) >= 8 
	AND  HOUR(timestamp) < 20 
	THEN 'day'
	ELSE 'night'
END AS day_or_night
FROM intel_signals 
)
SELECT day_or_night, COUNT(*) AS counted
FROM seperate_day_night 
GROUP BY day_or_night 

*** THIS RETURNED EMPTY
i was positive this was good and also looking around didnt see any night times 
moding the time was also a task 
i found this addtime function and updated 
---
UPDATE intel_signals 
SET timestamp = ADDTIME(timestamp,'10:00:00')
WHERE entity_id = 'TGT-001'

SELECT * 
FROM intel_signals 
WHERE entity_id = 'TGT-001'
---
output of the counter now:
day	516
night	50
---
the function worked!
---


step 2: sum each with distance 

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

this gave for each id the sum day and a row with id for sum night
but no entity was twice cause the edited all becae night 

i need to procede so i will consider this working for now 
and not mod the data for better testing 
#TODO: COME BACK AND TEST
---
step 3: filter entities with day dist 0 night dist 10+




# 5
get input of entity_id
query all the intel for that id
ORDER BY timestamp
---
SELECT * 
FROM intel_signals 
WHERE entity_id = 'TGT-006'
ORDER BY `timestamp` 
---
now to get the lon and lat into lists
and iterate on those list and display the points on the graph
---

# 6 

