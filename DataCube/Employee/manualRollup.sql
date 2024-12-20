SELECT country,gender,SUM(salary) AS totalsalary
FROM employee
GROUP BY country,gender    
UNION ALL
SELECT country,NULL,SUM(salary) AS totalsalary
FROM employee
GROUP BY country
UNION ALL
SELECT NULL,NULL,SUM(salary) AS totalsalary
FROM employee; 