import tkinter
import customtkinter
import datetime as dt
import mysql.connector as mariadb

# makes a table window with inputs list from select and window title
def table(lst, title):
    top = customtkinter.CTkToplevel()
    top.title(title)

    for i in range(len(lst)):
        for j in range(len(lst[0])): 
            e = customtkinter.CTkLabel(top, text=lst[i][j])
            e.grid(row=i, column=j, padx=20, pady=10)

    top.grab_set()

# backend ------------------------------------------------------------------------------------

# signing in to mariadb
mariadb_connection = mariadb.connect(user="root", password="jovelyn", host="localhost", port="3306")
# creating cursor for mysql queries
create_cursor = mariadb_connection.cursor()


### one time queries for initial state of database -------------------------------------------

# create_cursor.execute("CREATE DATABASE test_database")
# create_cursor.execute("SHOW DATABASES")

create_cursor.execute("USE test_database")

### DDL STATEMENTS FOR CREATING TABLES -------------------------------------------------------
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

### inserting initial state
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
# mariadb_connection.commit()

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

### FEATURES ------------------------------------------------------------------------
# add user function
def add_user(user_id, balance, fname, mname, lname):
    fname="'"+fname+"'"
    mname="'"+mname+"'"
    lname="'"+lname+"'"
    sql_statement = "INSERT INTO user VALUES(" + user_id + "," + balance + ","+ fname + "," + mname +"," + lname + ");"
    create_cursor.execute(sql_statement)
    mariadb_connection.commit()
    input1.delete(0,"end")
    input2.delete(0,"end")
    input3.delete(0,"end")
    input4.delete(0,"end")
    input5.delete(0,"end")


# add transaction function
def add_transaction(tid, tname, loaner, loanee, amount, pdate, gid, uid):
    curr = dt.datetime.now()
    tdate = str(curr.month) + "/" + str(curr.day) + "/" + str(curr.year)
    if (pdate!="NULL"):
        if (gid != "NULL"):
            sql_statement = "INSERT INTO transaction VALUES("+tid+", '"+ tname +"', "+ loaner +", "+ loanee +", "+ amount +", str_to_date('"+ tdate +"', '%m/%d/%Y'), " + "str_to_date('"+ pdate +"','%m/%d/%Y'), "+ gid + ", " + "NULL)"
        else:
            sql_statement = "INSERT INTO transaction VALUES("+tid+", '"+ tname +"', "+ loaner +", "+ loanee +", "+ amount +", str_to_date('"+ tdate +"', '%m/%d/%Y'), " + "str_to_date('"+ pdate +"','%m/%d/%Y'), NULL, " + uid + ")"
    else:
        if (gid != "NULL"):
            sql_statement = "INSERT INTO transaction VALUES("+tid+", '"+ tname +"', "+ loaner +", "+ loanee +", "+ amount +", str_to_date('"+ tdate +"', '%m/%d/%Y'), " + "NULL, "+ gid + ", " + "NULL" + ")"
        else:
            sql_statement = "INSERT INTO transaction VALUES("+tid+", '"+ tname +"', "+ loaner +", "+ loanee +", "+ amount +", str_to_date('"+ tdate +"', '%m/%d/%Y'), " + "NULL, NULL, " + uid + ")"
    create_cursor.execute(sql_statement)
    mariadb_connection.commit()
    
# add group function
def add_group(gid, gname, mem_no, balance):
    sql_statement = "INSERT INTO `group` VALUES(" + gid + "," + gname + ","+ mem_no + "," + balance + ");"
    print(sql_statement)
    create_cursor.execute(sql_statement)
    mariadb_connection.commit()

# delete user by id
def del_user(uid):
    sqlstatement = "DELETE FROM user WHERE user_id = " + uid
    create_cursor.execute(sqlstatement)
    mariadb_connection.commit()

# delete transaction by id
def del_transaction(tid):
    sqlstatement = "DELETE FROM transaction WHERE transaction_id = " + tid
    create_cursor.execute(sqlstatement)
    mariadb_connection.commit()

# delete all settled transactions
def clear_transaction():
    create_cursor.execute("DELETE FROM transaction WHERE payment_date IS NOT NULL;")
    mariadb_connection.commit()

# delete group by id
def del_group(gid):
    sqlstatement = "DELETE FROM `group` WHERE group_id = " + gid

# search a transaction by id
def search_transaction_id(tid):
    sqlstatement = "SELECT * FROM transaction WHERE transaction_id=" + tid
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)

# search a transaction by name
def search_transaction_name(tname):
    sqlstatement = "SELECT * FROM transaction WHERE transaction_name LIKE '%" + tname + "%'"
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)

# search a user by id
def search_user_id(uid):
    sqlstatement = "SELECT * FROM user WHERE user_id=" + uid
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)

# search a user by name
def search_user_name(uname):
    sqlstatement = "SELECT * FROM user WHERE CONCAT(first_name, middle_name, last_name) LIKE '%" + uname + "%'"
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)

# search a group by id
def search_grp_id(gid):
    sqlstatement = "SELECT * FROM `group` WHERE group_id=" + gid
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)

# search a group by name
def search_grp_name(gname):
    sqlstatement = "SELECT * FROM `group` WHERE group_name LIKE '%" + gname + "%'"
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)



# update user to follow


### TEST CASES

# add transaction testcase
# add_transaction("6", "asdf", "10203", "11111", "500.00", "01/10/2023", "NULL", "11111")

# add group testcase
# add_group("12345", "'New_Group'", "0", "0")

# test case for delete user by id
# del_user("12345")

# test case for delete transaction by id
# del_transaction("6")

# test case for deleting settled transactions (must delete transaction #5)
# clear_transaction()

# test case for deleting group by id
# del_group("12345")

# test case for searching transaction by id
# search_transaction_id("1")
# test case for searching transaction by name
# search_transaction_name("ol")

# test case for searching user by id
# search_user_id("99999")
# test case for searchin user by name
# search_user_name("jack")

# test case for searching group by id
# search_grp_id("10203")
# test case for searching group by name
# search_grp_name("on")

### TABLE CHECKER 
# create_cursor.execute("SELECT * FROM `group`")
# for x in create_cursor:
#     print(x)



##### REPORTS TO BE GENERATED


# view expenses from a certain month
def view_month(month):
    sqlstatement = "SELECT * FROM transaction WHERE MONTH(transaction_date) = " + month
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)
# view_month("1")

# # view all expenses made with a friend
# def view_friend(friend):
#     sqlstatement = "SELECT * FROM transaction WHERE user_id = " + friend + "loaner ="
#     create_cursor.execute(sqlstatement)
#     for x in create_cursor:
#         print(x)
# view_friend("11111")

# # view all expenses made with a group
# def view_group(group):
#     sqlstatement = "SELECT * FROM transaction where Group_id =  " + group
#     create_cursor.execute(sqlstatement)
#     for x in create_cursor:
#         print(x)

# view current balance from all expenses
def curr_balance():
    sqlstatement = "select balance from USER where user_id = 10000"
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)
# curr_balance()

# view all friends with outstanding balance;
def view_friend_outbalance():
    sqlstatement = "select * from USER where Balance > 0 and user_id != 10000"
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)
# view_friend_outbalance()

# view all groups
def view_groups():
    sqlstatement = "SELECT * FROM `group`"
    create_cursor.execute(sqlstatement)
    
    lst = [("Group ID", "Group Name", "Number of Members", "Balance")] + create_cursor.fetchall()
    table(lst, "Groups")

    for x in create_cursor:
        print(x)

    

def view_group_outbalance():
    sqlstatement = "SELECT * FROM `group` WHERE balance > 0"
    create_cursor.execute(sqlstatement)
    for x in create_cursor:
        print(x)
# view_group_outbalance()



# frontend ---------------------------------------------------------------------------
def handleSubmit():
    try:
        view_groups()
        submissionText.configure(text="Submission Success", text_color="white")
    except:
        submissionText.configure(text="Submission Fail", text_color="red")





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

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(padx=20, pady=20)

tabview.add("Manage Reports")  # add tab at the end
tabview.add("View Information")  # add tab at the end
tabview.set("Manage Reports")  # set currently visible tab
tab1 = tabview.tab("Manage Reports")
tab2 = tabview.tab("View Information") 

def add1():
    add = customtkinter.CTkToplevel()
    add.grab_set()

    global input1
    global input2
    global input3
    global input4
    global input5

    lbl1 = customtkinter.CTkLabel(add, text="User ID")
    input1 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl1.pack()
    input1.pack()

    lbl2 = customtkinter.CTkLabel(add, text="Balance")
    input2 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl2.pack()
    input2.pack()

    lbl3 = customtkinter.CTkLabel(add, text="First Name")
    input3 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl3.pack()
    input3.pack()

    lbl4 = customtkinter.CTkLabel(add, text="Middle Name")
    input4 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl4.pack()
    input4.pack()

    lbl5 = customtkinter.CTkLabel(add, text="Last Name")
    input5 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl5.pack()
    input5.pack()

    button = customtkinter.CTkButton(add, text="Add User", command=lambda: add_user(input1.get(), input2.get(), input3.get(), input4.get(), input5.get()))
    button.pack(padx=10, pady=10)

button1 = customtkinter.CTkButton(tab1, text="Add User", command=add1)
button1.pack(padx=10, pady=10)
button2 = customtkinter.CTkButton(tab1, text="Add Transaction", command=handleSubmit)
button2.pack(padx=10, pady=10)
button3 = customtkinter.CTkButton(tab1, text="Add Group", command=handleSubmit)
button3.pack(padx=10, pady=10)



submissionText = customtkinter.CTkLabel(tab1, text="")
submissionText.pack()


button = customtkinter.CTkButton(tab2, text="Show Groups", command=handleSubmit)
button.pack(padx=10, pady=10)

# runs the app
app.mainloop()