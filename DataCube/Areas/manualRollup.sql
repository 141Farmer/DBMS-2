SELECT continent,country,city,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY continent,country,city    
UNION ALL
SELECT continent,country,NULL,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY continent,country
UNION ALL
SELECT continent,NULL,NULL,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY continent
UNION ALL
SELECT NULL,NULL,NULL,SUM(saleAmount) AS totalsale
FROM Areas;

    
