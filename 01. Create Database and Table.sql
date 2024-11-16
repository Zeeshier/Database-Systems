-- Create a new database
CREATE DATABASE students;

-- Select the database to work in
USE  students;

-- Create a table called students
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    department VARCHAR(50)
);
