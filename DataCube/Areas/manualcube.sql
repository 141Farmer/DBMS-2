SELECT NULL AS continent,NULL AS country,NULL AS city,SUM(saleAmount) AS totalsale
FROM Areas
UNION ALL
SELECT NULL,NULL,city,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY city
UNION ALL
SELECT NULL,country,NULL,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY country
UNION ALL
SELECT continent,NULL,NULL,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY continent
UNION ALL
SELECT NULL,country,city,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY country,city
UNION ALL
SELECT continent,NULL,city,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY continent,city
UNION ALL
SELECT continent,country,NULL,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY continent,country
UNION ALL
SELECT continent,country,city,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY continent,country,city;