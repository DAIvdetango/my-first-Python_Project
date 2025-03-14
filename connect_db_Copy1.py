import mysql.connector

# база данных для извлечения информации
dbconfig_select = {'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
                    'user': 'ich1',
                    'password': 'password',
                    'database': 'sakila'}

def connect_to_db_sakila():
    global dbconfig_select
    global connection, cursor
    try:
        connection = mysql.connector.connect(**dbconfig_select)
        cursor = connection.cursor()
        return connection, cursor
    except Error as e:
        print(f"Error connecting to database: {e}")
    return None    

# база данных для записи запросов
dbconfig_insert = {'host': 'ich-edit.edu.itcareerhub.de',
                    'user': 'ich1',
                    'password': 'ich1_password_ilovedbs',
                    'port': 3306,
                    'database': 'project_130524_Ivanna'}

def connect_to_db_ich():
    try:
        connection = mysql.connector.connect(**dbconfig_insert)
        cursor = connection.cursor()
        return connection, cursor
    except Error as e:
        print(f"Error connecting to database: {e}")
    return None

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

