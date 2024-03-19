# Name and Student Number: 
  - ### Teja Chilukuri 101261938

# Link to youtube video: 
  - ### https://youtu.be/M_Qk3mHTYoY

# List of files: 
  - main.py: Contains the program 
  - requirements.txt: contains the packages used 
  - readme.md: contains this readme. 

## Compiling and Launching:

This Python program requires several dependencies to be installed before it can be executed. Below are instructions on how to install these dependencies either through a `requirements.txt` file or manually via pip.

### Installation of Dependencies:

 **Navigate to the Project Directory:**
   Open a terminal or command prompt, unzip the project folder, and navigate to the directory where the project files are located.

#### Option 1: Installing using `requirements.txt`


1. **Install Dependencies:**
   Execute the following command in the terminal:
   ```
   pip install -r requirements.txt
   ```
   This command will automatically install all the required packages listed in the `requirements.txt` file.

#### Option 2: Installing Manually

If installing through `requirements.txt` fails, you can manually install the required packages by pasting the following commands in your project terminal:

1. **Install datetime:**
   ```
   pip install datetime
   ```

2. **Install prettytable:**
   ```
   pip install prettytable
   ```

3. **Install psycopg2:**
   ```
   pip install psycopg2
   ```

### Launching the Program:

Once all the dependencies are installed, you can launch the program by executing the main Python file. Rhis can be done by running:
```
python main.py
```

### Validation checks: 

In order to improve user experience, I implemented the following validation checks: 
  1. Null check; None of the files can be null 
  2. Check to see if the inputted email already exists in the database; email is unique 
  3. Check to see if ID exists in the database (when trying to update and delete a user) 
  4. Parse Date correctly

### Using the Program: 

1. Upon launching the program, you will be prompted to input your database password. If the password is entered successfully, the project will be connect to your postgres database. Any of the default database credentials can be changed in `connection_to_db()` in **main.py**

2. After connecting, the program will display that the table has been successfully created and initialized. 

3. The main control menu will then appear. This control menu will call the appropriate CRUD methods bsaed on the user's input. The number correspond to the function, so in order to add a student to the table, the user has to click 1: 
  - 1 : add student
  - 2 : update student's email 
  - 3 : delete student
  - 4 : get all students 
  - 0 : exit 

  ### 1 : add a student 

   the user has input a valid first name, last name, email, and enrollment date. If all of the fields are valid, the student is added to the table

  ### 2 : Update student's email 

   The user has to input a valid student id and a new unique email. If all of the inputs are valid, the student is updated 

  ### 3 : Delete student 

   The user has to input a valid student id. If the id exists in the database, the student is deleted 

  ### 4 : get all students 

   Fetches all of the students in the students table, and displays then in a table format (using a python package called **prettytable** to display the table) 

  ### 0 : exit 

  - After choosing to exit, the user can either enter 1 to drop the table, or 0 to not drop table. 
  - The program is terminated



