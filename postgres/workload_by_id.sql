CREATE OR REPLACE FUNCTION wlCalls(wlId INT)
    RETURNS TABLE(id int, "timestamp" timestamp without time zone, time_delta double precision, service_instance character varying, service_type character varying)
AS $$
SELECT *
FROM service_call
WHERE timestamp 
BETWEEN 
(SELECT ts_init FROM workloads WHERE Id=wlId)
AND 
(SELECT ts_end FROM workloads WHERE Id=wlId);
$$ LANGUAGE SQL;

SELECT * FROM wlCalls(24)