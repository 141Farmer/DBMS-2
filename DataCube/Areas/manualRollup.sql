SELECT continent, country, city, SUM(CAST(saleAmount AS DECIMAL)) AS totalsale
FROM Areas
GROUP BY continent, country, city    
UNION ALL
SELECT continent, country, NULL AS city, SUM(CAST(saleAmount AS DECIMAL)) AS totalsale
FROM Areas
GROUP BY continent, country
UNION ALL
SELECT continent, NULL AS country, NULL AS city, SUM(CAST(saleAmount AS DECIMAL)) AS totalsale
FROM Areas
GROUP BY continent
UNION ALL
SELECT NULL As continent, NULL AS country, NULL AS city, SUM(CAST(saleAmount AS DECIMAL)) AS totalsale
FROM Areas;

    