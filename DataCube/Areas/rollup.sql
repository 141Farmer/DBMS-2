SELECT continent,country,city,SUM(saleAmount) AS totalsale
FROM Areas
GROUP BY ROLLUP(continent,country,city);