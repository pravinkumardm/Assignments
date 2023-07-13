CREATE USER 'python_password_checker'@'localhost' IDENTIFIED BY 'DB2023#pythonuser_+';
GRANT ALL PRIVILEGES ON passwordchecker.* TO 'python_password_checker'@'localhost';
FLUSH PRIVILEGES;
CREATE DATABASE passwordchecker;
USE passwordchecker;
CREATE TABLE username_password (
    pid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);
