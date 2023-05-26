import tkinter
import customtkinter
import mysql.connector as mariadb

# backend

# signing in to mariadb
mariadb_connection = mariadb.connect(user="root", password="jovelyn", host="localhost", port="3306")
# creating cursor for mysql queries
create_cursor = mariadb_connection.cursor()


### one time queries for initial state of database

# create_cursor.execute("CREATE DATABASE test_database")
# create_cursor.execute("SHOW DATABASES")

create_cursor.execute("USE test_database")

# create_cursor.execute("create table user(user_id int(5), balance decimal(8, 2), first_name varchar(20), middle_name varchar(20), last_name varchar(20), primary key(user_id));")
# create_cursor.execute("create table `group`(group_id int(5), group_name varchar(20), number_of_members int(4), balance decimal(8, 2), primary key(group_id));")
# create_cursor.execute('''
#     create table transaction(
#         transaction_id int(5),
#         transaction_name varchar(20),
#         loaner int(5),
#         loanee int(5),
#         amount decimal(8, 2),
#         transaction_date date,
#         payment_date date,
#         group_id int(5),
#         user_id int(5),
#         primary key (transaction_id),
#         constraint transaction_group_id_fk foreign key(group_id) references `group`(group_id),
#         constraint transaction_user_id_fk foreign key (user_id) references user(user_id)
#     );
# ''')
# create_cursor.execute('''
#     create table has(
#         user_id int(5),
#         group_id int(5),
#         constraint table_user_id_fk foreign key (user_id) references user(user_id),
#         constraint table_group_id_fk foreign key(group_id) references `group`(group_id)
#     );
# ''')

# create_cursor.execute("SHOW TABLES")
# for x in create_cursor:
#     print(x)

# sql_statement = '''
#     INSERT INTO user VALUES 
#     (11111, 500.00, 'Maria', 'Maganda', 'Makiling'),
#     (22222, 6900.00, 'Angela', 'Mercy', 'Ziegler'),
#     (33333, 8000.00, 'Gabriel', 'Reaper', 'Reyes'),
#     (44444, 4440.00, 'Jack', 'Soldier', 'Morrison'),
#     (55555, 40.00, 'Ana', 'Sup', 'Amari'),
#     (66666, 800.00, 'Fareeha', 'Pharah', 'Amari'),
#     (77777, 65000.00, 'Mei', 'Ice', 'Wall'),
#     (88888, 100.00, 'Brigitte', 'Tough', 'Lindholm'),
#     (99999, 7000.00, 'Reinhardt', 'Hammer', 'Wilhelm'),
#     (10000, 10000.00, 'Torbjorn', 'Turret', 'Lindholm');

# '''
# create_cursor.execute(sql_statement)
# mariadb_connection.commit()

# create_cursor.execute("SELECT * FROM user")
# for x in create_cursor:
#     print(x)

# create_cursor.execute('''
#     insert into `group` values
#     (10203, "Overwatch", 8, 0),
#     (10204, "Talon", 2, 200.00),
#     (10201, "Helix Corporation", 2, 0);
# ''')

# create_cursor.execute("SELECT * FROM `group`")
# for x in create_cursor:
#     print(x)

# create_cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
# create_cursor.execute('''
#     insert into `transaction` values
#     (1, 'Gun Rental', 10201, 10000, 600.00, str_to_date('10/13/2023', '%m/%d/%Y'), NULL, NULL, 10000),
#     (2, 'Suit Maintenance', 44444, 11111, 1000.00, str_to_date('05/25/2023','%m/%d/%Y'), NULL, NULL, 11111),
#     (3, 'Ice Wall Molder', 11111, 77777, 6900.00, str_to_date('04/12/2020', '%m/%d/%Y'), NULL, NULL, 77777),
#     (4, 'Scanners', 11111, 10204, 200.00, str_to_date('01/01/2021', '%m/%d/%Y'), NULL, 10204, NULL),
#     (5, 'Bills', 10203, 11111, 200.00, str_to_date('01/02/2023','%m/%d/%Y'), str_to_date('01/10/2023', '%m/%d/%Y'), NULL, 11111); 

# ''')
# mariadb_connection.commit()

# create_cursor.execute("SELECT * FROM transaction")
# for x in create_cursor:
#     print(x)

# create_cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
# create_cursor.execute('''
#     insert into has values
#         (11111, 10203),
#         (22222, 10203),
#         (44444, 10203),
#         (55555, 10203),
#         (77777, 10203),
#         (88888, 10203),
#         (99999, 10203),
#         (10000, 10203),
#         (11111, 10204),
#         (33333, 10204),
#         (11111, 10201),
#         (66666, 10201);
# ''')
# mariadb_connection.commit()

### reports to be generated
# add user function
def add_user(user_id, balance, fname, mname, lname):
    sql_statement = "INSERT INTO user VALUES(" + user_id + "," + balance + ","+ fname + "," + mname +"," + lname + ");"
    create_cursor.execute(sql_statement)
    mariadb_connection.commit()

# add transaction function
def add_transaction(input):
    sql_statement = "INSERT INTO transaction VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    create_cursor.execute(sql_statement, input)
    mariadb_connection.commit()
    
# add group function
def add_group(input):
    sql_statement = "INSERT INTO `group` VALUES(%s, %s, %s, %s)"
    create_cursor.execute(sql_statement, input)
    mariadb_connection.commit()


add_user("12345", "0", "aj", "c", "quinlat")

create_cursor.execute("SELECT * FROM user")
for x in create_cursor:
    print(x)


# frontend
def handleSubmit():
    try:
        submissionText.configure(text="Submission Success", text_color="white")
    except:
        submissionText.configure(text="Submission Fail", text_color="red")
    friend.delete(0, 'end')




# setting themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

# making app window
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Expense Tracker")

# editing windows title
title = customtkinter.CTkLabel(app, text="Hello World!")
title.pack(padx=10, pady=10)

# making a string var for input
friendVar = tkinter.StringVar()
friend = customtkinter.CTkEntry(app, width=350, height=40, textvariable=friendVar)
friend.pack()

# making a button that calls a function
button = customtkinter.CTkButton(app, text="Submit", command=handleSubmit)
button.pack(padx=10, pady=10)

submissionText = customtkinter.CTkLabel(app, text="")
submissionText.pack()


# runs the app
app.mainloop()