-- Create Course table
CREATE TABLE Course (
    Course_No INT PRIMARY KEY,
    Course_Name VARCHAR(255),
    Credit_Hours INT
);

-- Create Instructor table
CREATE TABLE Instructor (
    Instructor_ID INT PRIMARY KEY,
    Last_Name VARCHAR(255),
    First_Name VARCHAR(255),
    Address VARCHAR(255),
    Zip VARCHAR(10),
    Office_No VARCHAR(20)
);

-- Create Approved_Instructor table
CREATE TABLE Approved_Instructor (
    Instructor_ID INT,
    Course_No INT,
    PRIMARY KEY (Instructor_ID, Course_No),
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID),
    FOREIGN KEY (Course_No) REFERENCES Course(Course_No)
);

-- Create Student table
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY,
    Last_Name VARCHAR(255),
    First_Name VARCHAR(255),
    Address VARCHAR(255),
    Zip VARCHAR(10),
    Major VARCHAR(255),
    Class VARCHAR(20),
    Status VARCHAR(20)
);

-- Create Campus table
CREATE TABLE Campus (
    Campus_Name VARCHAR(255) PRIMARY KEY,
    Address VARCHAR(255),
    Zip VARCHAR(10),
    Phone_No VARCHAR(20)
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
    FOREIGN KEY (Room_No) REFERENCES Room(Room_No),
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID),
    FOREIGN KEY (Campus_Name) REFERENCES Campus(Campus_Name),
    FOREIGN KEY (Course_No) REFERENCES Course(Course_No)
);

-- Create Room table
CREATE TABLE Room (
    Room_No INT PRIMARY KEY,
    Campus_Name VARCHAR(255),
    Facility VARCHAR(255),
    Capacity INT,
    FOREIGN KEY (Campus_Name) REFERENCES Campus(Campus_Name)
);

-- Create Student_Grade table
CREATE TABLE Student_Grade (
    Student_ID INT,
    Class_ID INT,
    Student_Grade VARCHAR(10),
    PRIMARY KEY (Student_ID, Class_ID),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY (Class_ID, Campus_ID, Room_No) REFERENCES Class(Campus_ID, Room_No)
);



-- Student_ID - Primary Key, Foreign key


-- Table Name: Class
-- Attributes:
-- Campus_ID- Primary Key
-- Room_No - Primary Key, Foreign key
-- Course_No
-- Section_No
-- Semester_Name
-- Years
-- Instructor_ID
-- Campus_Name
-- Start_Date
-- Start_Time


-- Table Name: Room
-- Attributes:
-- Room_No- Primary Key
-- Campus_Name - Primary Key, Foreign key
-- Facility
-- Capacity

-- Table Name: Student_Grade
-- Attributes:
-- Student_ID - Primary Key, Foreign key
-- Class_ID - Primary Key, Foreign key
-- Student_Grade




-- Relations:
-- Student to Student_Grade : zero or many
-- Student_Grade to Student : one


-- Class to Student_Grade : zero or many
-- Student_Grade to Class : one

-- Campus to Room : zero or many
-- Room to Campus : one

-- Campus to Room : zero or many
-- Room to Campus : one

-- Class to Room : one (Dotted Line Relation)
-- Room to Class : zero or many (Dotted Line Relation)

-- Class to Approved_Instructor : one (Dotted Line Relation)
-- Approved_Instructor to Class : zero or many (Dotted Line Relation)