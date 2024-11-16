SELECT NULL AS country,NULL AS gender,SUM(salary) AS totalsalary
FROM employee
UNION ALL
SELECT NULL,gender,SUM(salary) AS totalsalary
FROM employee
GROUP BY gender
UNION ALL
SELECT country,NULL,SUM(salary) AS totalsalary
FROM employee
GROUP BY country
UNION ALL
SELECT country,gender,SUM(salary) AS totalsalary
FROM employee
GROUP BY country,gender;