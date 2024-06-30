CREATE DATABASE employee_management;
USE employee_management;

CREATE TABLE employees(
 emp_id INT NOT NULL UNIQUE PRIMARY KEY,
 emp_name VARCHAR(30) NOT NULL,
 emp_gender VARCHAR(255) NOT NULL,
 emp_position VARCHAR(255) NOT NULL,
 emp_dep VARCHAR(30) NOT NULL, 
 emp_email VARCHAR(30) NOT NULL UNIQUE,
 emp_contact VARCHAR(15) NOT NULL UNIQUE,
 emp_password VARCHAR(30) NOT NULL UNIQUE,
 emp_address VARCHAR(150) NOT NULL
);

CREATE TABLE attendance(
emp_id INT  NOT NULL,
employee_name VARCHAR(70) NOT NULL,
date DATE NOT NULL, 
check_in_time TIME, 
check_out_time TIME,
FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE
);


SELECT * FROM attendance;
SELECT * FROM employees;
