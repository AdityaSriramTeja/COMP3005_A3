import psycopg2
from prettytable import PrettyTable
from datetime import datetime

# CONNECT TO DATABASE
def connection_to_db():

  # prompt the user for the password
  user_password = input("Enter database password: ")
  port_number = 5432
  database_name = "postgres"
  user_name = "postgres"
  try:

    # make a connection object
    connection = psycopg2.connect(host=  "localhost", user=user_name, dbname=database_name , password= user_password, port= port_number)
    print("Successfully connected to the Database with name ", database_name)

    # return the connection object is connected successfully
    return connection

  except:
    print("Error while connecting to the database")

# CREATE THE TABLE
def create_table(connection):
  try:
    cursor = connection.cursor()
    # create the table
    cursor.execute(""" CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                enrollment_date DATE

    );
    """)

    print("SUCCESSFULLY CREATED THE TABLE")
    # commit the change so that it is reflected in the database
    connection.commit()
    cursor.close()
  except Exception as error:
    print("Error creating the table ", error)

# INITIALIZE THE DATABASE
def initialize_database(connection):
  try:
    cursor = connection.cursor()

    #insert the three rows into the database
    cursor.execute("""INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
      ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
      ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
      ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
    """)
    print("SUCCESSFULLY INITIALIZED THE TABLE")

    # commit the change so that it is reflected in the database
    connection.commit()
    cursor.close()
  except Exception as error:
    print("Error initializing the table ", error)


# THE BELOW 4 METHODS ARE THE CRUD METHODS

# CRUD: READ OPERATION TO GET ALL STUDENTS
def getAllStudents(connection):
  try:
    # initialized the objects
    cursor = connection.cursor()
    table = PrettyTable()
    # execute the query to retrieve all of the rows
    cursor.execute("""SELECT * FROM students""")

    # store the column names in an array, this is used as the field names for our table object. cursor.description has the column name details
    columns = [columnName[0] for columnName in cursor.description]
    # set the field names for the tables to the columns array
    table.field_names = columns

    # iterate through each row in our database, and add the row to the table object.
    for row in cursor.fetchall():
      table.add_row(row)

    # print the table object
    print("\nStudents Table:\n")
    print(table, "\n")

    cursor.close()
  except Exception as error:
    print("Error while reading fetching all students ", error)

# WRITE OPERATION TO ADD A STUDENT TO THE TABLE
def addStudent(connection, first_name, last_name ,email, enrollment_date):
  try:
    cursor = connection.cursor()

    query = """INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
      (%s, %s, %s, %s)
    """

    # execute the SQL query to insert the data into the database
    cursor.execute(query, (first_name, last_name ,email, enrollment_date))

    print("SUCCESSFULLY ADDED THE STUDENT TO THE TABLE")

    # commit in order to push the change to the database, else the query wont be reflected
    connection.commit()
    cursor.close()
  except Exception as error:
    print("Error adding student ", error )

# UPDATE OPERATION TO UPDATE A STUDENT'S EMAIL
def updateStudentEmail(connection, student_id, new_email):
  try:
    cursor = connection.cursor()

    # execute the query to set the email where id is the user's inputted id
    query = """UPDATE students SET email = %s WHERE id = %s
    """
    cursor.execute(query, (new_email, student_id))

    print("SUCCESSFULLY UPDATED THE STUDENT'S EMAIL")

    # commit the change to the database, so that it can reflect the change
    connection.commit()
    cursor.close()
  except Exception as error:
    print("Error updating student ", error)

# DELETE TO DELETE A STUDENT BASED ON ID
def deleteStudent(connection, student_id):
  try:
    cursor = connection.cursor()

    # execute the query to delete the corresponding student from the table

    query = """DELETE FROM students WHERE id = %s
    """
    cursor.execute(query, (student_id,))

    print("SUCCESSFULLY DELETED THE STUDENT FROM THE TABLE")

    # commit the change to the database, so that it can reflect the change
    connection.commit()
    cursor.close()
  except Exception as error:
    print("Error Deleting student ", error)

# DROP TABLE
def dropTable(connection):
  try:
    cursor = connection.cursor()
    # execute the query to drop the table

    cursor.execute("""DROP TABLE students""")
    print("SUCCESSFULLY DROPPED THE TABLE")

    # commit to reflect the change
    connection.commit()
    cursor.close()
  except Exception as error:
    print("Error while dropping the table ", error)

# BELOW TWO METHODS ARE ONLY VALIDATION METHODS

# CHECK IF EMAIL IS UNIQUE (IMPORTANT WHEN ADDING OR UPDATING A USER)
def checkIfEmailIsUnique(connection, email):
  try:
    cursor = connection.cursor()
    # query for all the rows that contain the email = user's inputted email.
    # if the number of rows queried is more than 0, then the email already exists, and it is not a unique email
    query = """SELECT email FROM students WHERE email = %s"""
    cursor.execute(query, (email,))
    unique = False
    if cursor.rowcount == 0:
      unique = True
    cursor.close()
    return unique

  except Exception as error:
    print("Error while reading emails ", error)

# CHECK IF THE USER ID EXISTS (IMPORTANT WHEN TRYING TO UPDATE OR DELETE THE USER )
def checkIfIdExists(connection, id):
  try:
    cursor = connection.cursor()

    # query for all of the rows where id = user's inputted id.
    # if the number of rows queries is 0, then the id doesn't exist, which means we cannot update or delete that row in the first place.
    query = """SELECT id FROM students WHERE id = %s"""
    cursor.execute(query, (id,))
    exists= True
    if cursor.rowcount == 0:
      exists= False
    cursor.close()
    return exists

  except Exception as error:
    print("Error while reading ids ", error)

# THE BELOW 4 METHODS ARE THE METHODS WHICH PROMPT THE USER FOR DATA

# USER INPUT FOR ID, AND VALIDATE USER INPUT: NOT NULL (AND CHECK IF ID EXSISTS FOR UPDATE AND DELETE OPERATIONS)
def completeValicationForId(connection):

  # keep prompting the user for the correct input. Data cannot be null
  # return the id when input is valid
  while True:
    id= input("Enter student id: ")

    if not id:
      print("ID CANNOT BE NULL")
    else:
      id = int(id)
      # if id is not null, check is the id exists in the database
      if checkIfIdExists(connection, id) == False:
        print("ID DOES NOT EXIST")
      else:
        return id

# USER INPUT FOR FIRST NAME, AND VALIDATE INPUT: NOT NULL
def completeValidationForFirstName():

  # keep prompting the user for the correct input. Data cannot be null .
  # return the first_name once input is valid
  while True:
    first_name = input("Enter first name: ")

    if first_name:
      return first_name
    else:
      print("FIRST NAME CANNOT BE NULL")

# USER INPUT FOR LAST NAME, AND VALIDATE INPUT: NOT NULL
def completeValidationForLastName():

   # keep prompting the user for the correct input. Data cannot be null .
  # return the last_name once input is valid
  while True:
    last_name = input("Enter last name: ")

    if last_name:
      return last_name
    else:
      print("LAST NAME CANNOT BE NULL")

# USER INPUT FOR EMAIL, AND VALIDATE INPUT: NOT NULL AND UNIQUE
def completeValidationForEmail(connection):
  # keep prompting the user for the correct input. Data cannot be null .
  # return the email once input is valid
  while True:
    email= input("Enter email: ").strip()

    if not email:
      print("Email cannot be null")
    else :
      # if email is not null, check if the email is unique
      if checkIfEmailIsUnique(connection, email) == False:
        print("EMAIL ALREADY EXISTS, PLEASE TRY ANOTHER EMAIL")
      else:
        return email

# USER INPUT FOR ENROLLMENT DATE AND VALIDATE DATE: NOT NULL AND FOLLOWS YYYY-MM-DD
def completeValidationForDate():
  # keep prompting the user for the correct input. Data cannot be null and it needs to be formatted correct.
  # return the date once input is valid
  while True:
    date= input("Enter enrollment date (YYYY-MM-DD): ")

    try:
      if date == datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
        return date

    except ValueError:
      print("INVALID DATE. DATE MUST BE IN THE FOLLOWING FORMAT: YYYY-MM-DD, for example 2023-01-01")

def main():

  # create a connection to the database
  connection = connection_to_db()

  # if connected successfully
  if connection:

    # create a students table
    create_table(connection)

    # initialize the table with the 3 default rows
    initialize_database(connection)

    # keep prompting the user for input, and trigger the approriate CRUD function till the user chooses to quit
    while True:
      choice = input("Please enter choice you want to make (1: add student, 2: update student email, 3: delete student, 4: get all students, 0:exit): ")

      if choice == "1":

        # all of these values will be initalized correctly, because the methods contain the validation
        first_name = completeValidationForFirstName()
        last_name = completeValidationForLastName()
        email = completeValidationForEmail(connection)
        date = completeValidationForDate()

        # add student to the table
        addStudent(connection, first_name, last_name, email, date )

      elif choice == "2":
        # all of these values will be initalized correctly, because the methods contain the validation
        id = completeValicationForId(connection)
        email=  completeValidationForEmail(connection)

        # update the student's email
        updateStudentEmail(connection, id, email)

      elif choice  == "3":
        # all of these values will be initalized correctly, because the methods contain the validation
        id = completeValicationForId(connection)

        # delete the student
        deleteStudent(connection, id)

      elif choice == "4":
        # fetch all of the students
        getAllStudents(connection)

      elif choice  == "0":
        # check if the user would like to drop the table
        wouldDropTable = input("Would you like to drop/delete the table (0: No, 1: Yes ): ")

        if wouldDropTable == "1":
          dropTable(connection)

        print("Thank you for using the application")
        break

    # close connection
    connection.close()

if __name__ == "__main__":
  main()
