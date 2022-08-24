import mysql.connector
from mysql.connector import errorcode
import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
}

# connecting to database and creating a cursor to exe queries
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

DB_NAME = 'sql_python'

TABLES = {}
TABLES['employees_schedule'] = (
    "CREATE TABLE employees_schedule (id INT AUTO_INCREMENT PRIMARY KEY, day VARCHAR(255), date VARCHAR(255),hours VARCHAR(255), employee_name VARCHAR(255))"
)


def create_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET "
                   "'utf8'".format(DB_NAME))
    print("Databse {} created".format(DB_NAME))


def create_tables():
    cursor.execute("USE {}".format(DB_NAME))
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table ({}) ".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exist")
            else:
                print(err.msg)


# CRUD functions
def add_shifts(day, date, hours, employee_name):
    qry = "INSERT INTO employees_schedule(day, date, hours, employee_name) VALUES(%s,%s,%s,%s)"
    cursor.execute(qry, (day, date, hours, employee_name))
    cnx.commit()
    shift_id = cursor.lastrowid
    print("Added shift {}".format(shift_id))


def get_shifts():
    qry = "SELECT * FROM employees_schedule"
    cursor.execute(qry)
    result = cursor.fetchall()

    for row in result:
        print(row)


def update_shifts(id, day, date):
    qry = "UPDATE employees_schedule SET day=%s, date=%s WHERE id= %s"
    cursor.execute(qry, (day, date, id))
    cnx.commit()
    print("shift updated{}".format(id))


def delete_shift(id):
    qry = "DELETE FROM employees_schedule WHERE id = %s "
    cursor.execute(qry, (id,))
    cnx.commit()


create_database()
create_tables()

add_shifts('Sun', '11/2/2022', '11:00-17:00', 'tamir')
update_shifts(4, 'updy', '11/05/2022')
delete_shift(10)
get_shifts()
