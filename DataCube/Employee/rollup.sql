SELECT country,gender,SUM(salary) AS totalsalary
FROM employee
GROUP BY ROLLUP(country,gender);