
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS STUDENT;
DROP TABLE IF EXISTS CAMPUS;
DROP TABLE IF EXISTS ROOM;
DROP TABLE IF EXISTS COURSE;
DROP TABLE IF EXISTS INSTRUCTOR;
DROP TABLE IF EXISTS APPROVED_INSTRUCTOR;
DROP TABLE IF EXISTS CLASS;
DROP TABLE IF EXISTS STUDENT_GRADE;
SET FOREIGN_KEY_CHECKS=1;


CREATE TABLE Course (
    Course_No INT PRIMARY KEY AUTO_INCREMENT,
    Course_Name VARCHAR(255) UNIQUE NOT NULL,
    Credit_Hours INT CHECK (Credit_Hours BETWEEN 1 AND 4) NOT NULL
);

-- Create Instructor table
CREATE TABLE Instructor (
    Instructor_ID INT PRIMARY KEY AUTO_INCREMENT,
    Last_Name VARCHAR(255) NOT NULL,
    First_Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Zip VARCHAR(10),
    Office_No VARCHAR(20) NOT NULL
);

-- Create Approved_Instructor table
CREATE TABLE Approved_Instructor (
    Instructor_ID INT,
    Course_No INT,
    PRIMARY KEY (Instructor_ID, Course_No),
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID) ON UPDATE CASCADE,
    FOREIGN KEY (Course_No) REFERENCES Course(Course_No) ON UPDATE CASCADE
);

-- Create Student table
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    Last_Name VARCHAR(255) NOT NULL,
    First_Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Zip VARCHAR(10),
    Major VARCHAR(255),
    Class VARCHAR(20),
    Status VARCHAR(20) CHECK (Status IN ('A', 'B', 'C', 'D', 'E', 'F', 'W', 'E')) NOT NULL
);

-- Create Campus table
CREATE TABLE Campus (
    Campus_Name VARCHAR(255) PRIMARY KEY,
    Address VARCHAR(255),
    Zip VARCHAR(10),
    Phone_No VARCHAR(20)
);

-- Create Room table
CREATE TABLE Room (
    Room_No INT PRIMARY KEY AUTO_INCREMENT,
    Campus_Name VARCHAR(255),
    Facility VARCHAR(255),
    Capacity INT,
    FOREIGN KEY (Campus_Name) REFERENCES Campus(Campus_Name) ON UPDATE CASCADE
);

-- Create Class table
CREATE TABLE Class (
    Campus_ID INT,
    Room_No INT,
    Course_No INT,
    Section_No INT,
    Semester_Name VARCHAR(255),
    Years INT,
    Instructor_ID INT,
    Campus_Name VARCHAR(255),
    Start_Date DATE,
    Start_Time TIME,
    PRIMARY KEY (Campus_ID, Room_No),
    FOREIGN KEY (Room_No) REFERENCES Room(Room_No) ON UPDATE CASCADE,
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID) ON UPDATE CASCADE,
    FOREIGN KEY (Campus_Name) REFERENCES Campus(Campus_Name) ON UPDATE CASCADE,
    FOREIGN KEY (Course_No) REFERENCES Course(Course_No) ON UPDATE CASCADE
);

-- Create Student_Grade table
CREATE TABLE Student_Grade (
    Student_ID INT,
    Class_Campus_ID INT,
    Class_Room_No INT,
    Student_Grade VARCHAR(10) CHECK (Student_Grade IN ('A', 'B', 'C', 'D', 'E', 'F', 'W', 'E')) NOT NULL,
    PRIMARY KEY (Student_ID, Class_Campus_ID, Class_Room_No),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON UPDATE CASCADE,
    FOREIGN KEY (Class_Campus_ID, Class_Room_No) REFERENCES Class(Campus_ID, Room_No) ON UPDATE CASCADE
);

-- Insert data into the Course table
INSERT INTO Course (Course_Name, Credit_Hours) VALUES
('Math 101', 3),
('English 101', 4),
('History 101', 3);

-- Insert data into the Instructor table
INSERT INTO Instructor (Last_Name, First_Name, Office_No) VALUES
('Smith', 'John', 'Office1'),
('Doe', 'Jane', 'Office2'),
('Johnson', 'Michael', 'Office3');

-- Insert data into the Campus table
INSERT INTO Campus (Campus_Name, Address, Zip, Phone_No) VALUES
('Main Campus', '123 Main St', '12345', '555-1234'),
('East Campus', '456 East St', '67890', '555-5678');

-- Insert data into the Room table
INSERT INTO Room (Campus_Name, Facility, Capacity) VALUES
('Main Campus', 'Room 101', 50),
('East Campus', 'Room 201', 40);

-- Insert data into the Class table
INSERT INTO Class (Campus_ID, Room_No, Course_No, Section_No, Semester_Name, Years, Instructor_ID, Campus_Name, Start_Date, Start_Time) VALUES
(1, 1, 1, 1, 'Fall', 2023, 1, 'Main Campus', '2023-09-01', '08:00:00'),
(2, 2, 2, 2, 'Fall', 2023, 2, 'East Campus', '2023-09-01', '10:00:00');

-- Insert data into the Student table
INSERT INTO Student (Last_Name, First_Name, Address, Zip, Major, Class, Status) VALUES
('Doe', 'John', '123 Oak St', '54321', 'Computer Science', 'Freshman', 'A'),
('Johnson', 'Alice', '456 Maple St', '98765', 'English Literature', 'Sophomore', 'B'),
('Smith', 'Bob', '789 Pine St', '13579', 'History', 'Junior', 'C');

-- Insert data into the Student_Grade table
INSERT INTO Student_Grade (Student_ID, Class_Campus_ID, Class_Room_No, Student_Grade) VALUES
(1, 1, 1, 'A'),
(2, 2, 2, 'B'),
(3, 1, 1, 'C');

-- Commit changes
COMMIT;

-- Show tables
SHOW TABLES;

-- Show data for each table
SELECT * FROM Course;
SELECT * FROM Instructor;
SELECT * FROM Approved_Instructor;
SELECT * FROM Student;
SELECT * FROM Campus;
SELECT * FROM Room;
SELECT * FROM Class;
SELECT * FROM Student_Grade;