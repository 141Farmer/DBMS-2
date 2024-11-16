SELECT continent,country,city,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY CUBE(continent,country,city);