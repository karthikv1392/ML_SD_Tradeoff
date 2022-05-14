SELECT * 
FROM service_status 
WHERE service_instance 
LIKE '%user%'
ORDER BY timestamp