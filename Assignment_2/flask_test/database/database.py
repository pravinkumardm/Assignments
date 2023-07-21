import mysql.connector

#Dictionary to store all the database related inputs
db_config = {
    'host' :"localhost", 
    'password' :"DB2023#pythonuser_+", 
    'user' :"python_password_checker",
    'database': 'passwordchecker'}


def get_connection(host=db_config['host'], password=db_config['password'], user=db_config['user'], database=db_config['database']):
    '''
    Function to create a connection to mysql server.
    Inputs: host, password, user, database
    Output: mySQL Connector object
    '''
    connection = mysql.connector.connect(host = host, password = password, user = user, database = database)
    return connection

def insert_password(username, password, table_name="username_password"):
    '''
    Function to insert data into the table
    Inputs: username, password, table_name
    Output: True if table is updated else False
    '''
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO "+ table_name +" (username, password) VALUES (%s, %s)"
        values = (username, password)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        return False


def fetch_passwords(table_name="username_password"):
    '''
    Function to fetch all the data from database.
    Inputs: username, password, table_name
    Output: True if table is updated else False
    '''
    connection = get_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
