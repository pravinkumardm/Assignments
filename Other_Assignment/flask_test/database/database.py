import mysql.connector

database_configuration = {
    'host' :"localhost", 
    'password' :"DB2023#pythonuser_+", 
    'user' :"python_password_checker",
    'database': 'passwordchecker'}

def get_connection():
    return mysql.connector.connect(host=database_configuration['host'], password=database_configuration['password'], user=database_configuration['user'], database=database_configuration['database'])

def insert_password(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO username_password (username, password) VALUES (%s, %s)"
    values = (username, password)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return True


def fetch_passwords():
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM username_password"
    # query = "ALTER TABLE `passwordchecker`.`username_password` CHANGE COLUMN `pid` `pid` INT NOT NULL AUTO_INCREMENT ;"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

if __name__ == "__main__":
    fetch_passwords()