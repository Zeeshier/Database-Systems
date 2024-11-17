
-- Insert data into table
INSERT INTO students (id, name, age, department)
VALUES 
    (1, 'Zeeshan', 20, 'Computer Science'),
    (2, 'Huraira', 22, 'Pharmacy'),
    (3, 'Haris', 21, 'DPT'),
    (4, 'Talha', 23, 'LBS'),
    (5, 'Saram', 19, 'English');


-- Delete Data
DELETE FROM students
WHERE department = 'LBS';


-- Insert Data
INSERT INTO students (id, name, age, department)
VALUES
   (6, 'Talha',24, 'Math'),
   (7,'Rohan',20, 'Chemistry')


-- Update Data
UPDATE students 
SET id= 4 
WHERE id= 5

UPDATE students
SET id = CASE
    WHEN id = 6 THEN 5
    WHEN id = 7 THEN 6
END
WHERE id IN (6, 7);

