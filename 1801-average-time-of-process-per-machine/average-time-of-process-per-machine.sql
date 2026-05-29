# Write your MySQL query statement below
SELECT 
    start_obj.machine_id,
    ROUND(AVG(end_obj.timestamp - start_obj.timestamp), 3) AS processing_time
FROM Activity AS start_obj
JOIN Activity AS end_obj
ON start_obj.machine_id = end_obj.machine_id
AND start_obj.process_id = end_obj.process_id
WHERE start_obj.activity_type = 'start'
AND end_obj.activity_type = 'end'
GROUP BY start_obj.machine_id;