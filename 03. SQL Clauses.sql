-- With Clause
WITH NewStudents AS (
    SELECT 7 AS id, 'Ali' AS name, 19 AS age, 'Computer Science' AS department
    UNION ALL
    SELECT 8, 'Babar', 18, 'Pharmacy'
    UNION ALL
    SELECT 9, 'Junaid', 19, 'Biology'
    UNION ALL
    SELECT 10, 'Hashir', 20, 'LBS'
    UNION ALL
    SELECT 11, 'Furkan', 21, 'English'
)
INSERT INTO students (id, name, age, department)
SELECT id, name, age, department
FROM NewStudents;

-- Group By

SELECT department, AVG(score) AS avg_score
FROM students
GROUP BY department
HAVING AVG(score) > 85;
