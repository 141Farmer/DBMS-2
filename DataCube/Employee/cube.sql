SELECT country,gender,SUM(salary) AS totalsalary
FROM employee
GROUP BY CUBE(country,gender);