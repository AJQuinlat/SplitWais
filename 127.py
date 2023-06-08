import tkinter as tk
import tkinter.font as font
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
mariadb_connection = mariadb.connect(user="root", password="MariaDB", host="localhost", port="3306")
# creating cursor for mysql queries
cursor = mariadb_connection.cursor()


### one time queries for initial state of database -------------------------------------------


cursor.execute("DROP DATABASE IF EXISTS test_database")
cursor.execute("CREATE DATABASE test_database")
cursor.execute("USE test_database")

### DDL STATEMENTS FOR CREATING TABLES -------------------------------------------------------
cursor.execute("create table user(user_id int(5), balance decimal(8, 2), first_name varchar(20), middle_name varchar(20), last_name varchar(20), primary key(user_id));")
cursor.execute("create table `group`(group_id int(5), group_name varchar(20), number_of_members int(4), balance decimal(8, 2), primary key(group_id));")
cursor.execute('''
    create table transaction(
        transaction_id int(5),
        transaction_name varchar(20),
        loaner int(5),
        loanee int(5),
        amount decimal(8, 2),
        transaction_date date,
        payment_date date,
        group_id int(5),
        user_id int(5),
        primary key (transaction_id),
        constraint transaction_group_id_fk foreign key(group_id) references `group`(group_id),
        constraint transaction_user_id_fk foreign key (user_id) references user(user_id)
    );
''')
cursor.execute('''
    create table has(
        user_id int(5),
        group_id int(5),
        constraint table_user_id_fk foreign key (user_id) references user(user_id),
        constraint table_group_id_fk foreign key(group_id) references `group`(group_id)
    );
''')

### inserting initial state
sql_statement = '''
    INSERT INTO user VALUES 
    (11111, 500.00, 'Maria', 'Maganda', 'Makiling'),
    (22222, 6900.00, 'Angela', 'Mercy', 'Ziegler'),
    (33333, 8000.00, 'Gabriel', 'Reaper', 'Reyes'),
    (44444, 4440.00, 'Jack', 'Soldier', 'Morrison'),
    (55555, 40.00, 'Ana', 'Sup', 'Amari'),
    (66666, 800.00, 'Fareeha', 'Pharah', 'Amari'),
    (77777, 65000.00, 'Mei', 'Ice', 'Wall'),
    (88888, 100.00, 'Brigitte', 'Tough', 'Lindholm'),
    (99999, 7000.00, 'Reinhardt', 'Hammer', 'Wilhelm'),
    (10000, 10000.00, 'Torbjorn', 'Turret', 'Lindholm');

'''
cursor.execute(sql_statement)
mariadb_connection.commit()

# cursor.execute("SELECT * FROM user")
# for x in cursor:
#     print(x)

cursor.execute('''
    insert into `group` values
    (10203, "Overwatch", 8, 0),
    (10204, "Talon", 2, 200.00),
    (10201, "Helix Corporation", 2, 0);
''')
mariadb_connection.commit()

# cursor.execute("SELECT * FROM `group`")
# for x in cursor:
#     print(x)

cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
cursor.execute('''
    insert into `transaction` values
    (1, 'Gun Rental', 10201, 10000, 600.00, str_to_date('10/13/2023', '%m/%d/%Y'), NULL, NULL, 10000),
    (2, 'Suit Maintenance', 44444, 11111, 1000.00, str_to_date('05/25/2023','%m/%d/%Y'), NULL, NULL, 11111),
    (3, 'Ice Wall Molder', 11111, 77777, 6900.00, str_to_date('04/12/2020', '%m/%d/%Y'), NULL, NULL, 77777),
    (4, 'Scanners', 11111, 10204, 200.00, str_to_date('01/01/2021', '%m/%d/%Y'), NULL, 10204, NULL),
    (5, 'Bills', 10203, 11111, 200.00, str_to_date('01/02/2023','%m/%d/%Y'), str_to_date('01/10/2023', '%m/%d/%Y'), NULL, 11111); 

''')
mariadb_connection.commit()

cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
cursor.execute('''
    insert into has values
        (11111, 10203),
        (22222, 10203),
        (44444, 10203),
        (55555, 10203),
        (77777, 10203),
        (88888, 10203),
        (99999, 10203),
        (10000, 10203),
        (11111, 10204),
        (33333, 10204),
        (11111, 10201),
        (66666, 10201);
''')
mariadb_connection.commit()

### FEATURES ------------------------------------------------------------------------
# add user function
def add_user(user_id, balance, fname, mname, lname):
    fname="'"+fname+"'"
    mname="'"+mname+"'"
    lname="'"+lname+"'"
    sql_statement = "INSERT INTO user VALUES(" + user_id + "," + balance + ","+ fname + "," + mname +"," + lname + ");"
    cursor.execute(sql_statement)
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
    cursor.execute(sql_statement)
    mariadb_connection.commit()
    
# add group function
def add_group(gid, gname, mem_no, balance):
    sql_statement = "INSERT INTO `group` VALUES(" + gid + "," + gname + ","+ mem_no + "," + balance + ");"
    print(sql_statement)
    cursor.execute(sql_statement)
    mariadb_connection.commit()

# delete user by id
def del_user(uid):
    sqlstatement = "DELETE FROM user WHERE user_id = " + uid
    cursor.execute(sqlstatement)
    mariadb_connection.commit()

# delete transaction by id
def del_transaction(tid):
    sqlstatement = "DELETE FROM transaction WHERE transaction_id = " + tid
    cursor.execute(sqlstatement)
    mariadb_connection.commit()

# delete all settled transactions
def clear_transaction():
    cursor.execute("DELETE FROM transaction WHERE payment_date IS NOT NULL;")
    mariadb_connection.commit()

# delete group by id
def del_group(gid):
    sqlstatement = "DELETE FROM `group` WHERE group_id = " + gid

# search a transaction by id
def search_transaction_id(tid):
    sqlstatement = "SELECT * FROM transaction WHERE transaction_id=" + tid
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)

# search a transaction by name
def search_transaction_name(tname):
    sqlstatement = "SELECT * FROM transaction WHERE transaction_name LIKE '%" + tname + "%'"
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)

# search a user by id
def search_user_id(uid):
    sqlstatement = "SELECT * FROM user WHERE user_id=" + uid
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)

# search a user by name
def search_user_name(uname):
    sqlstatement = "SELECT * FROM user WHERE CONCAT(first_name, middle_name, last_name) LIKE '%" + uname + "%'"
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)

# search a group by id
def search_grp_id(gid):
    sqlstatement = "SELECT * FROM `group` WHERE group_id=" + gid
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)

# search a group by name
def search_grp_name(gname):
    sqlstatement = "SELECT * FROM `group` WHERE group_name LIKE '%" + gname + "%'"
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)



# update user to follow



##### REPORTS TO BE GENERATED


# view expenses from a certain month
def view_month(month):
    sqlstatement = "SELECT * FROM transaction WHERE MONTH(transaction_date) = " + month
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)
# view_month("1")

# view all expenses made with a friend
def view_all_transaction():
    cursor.execute("SELECT * FROM transaction")
    return(cursor.fetchall())


# # view all expenses made with a friend
# def view_friend(friend):
#     sqlstatement = "SELECT * FROM transaction WHERE user_id = " + friend + "loaner ="
#     cursor.execute(sqlstatement)
#     for x in cursor:
#         print(x)
# view_friend("11111")

# # view all expenses made with a group
# def view_group(group):
#     sqlstatement = "SELECT * FROM transaction where Group_id =  " + group
#     cursor.execute(sqlstatement)
#     for x in cursor:
#         print(x)

# view current balance from all expenses
def curr_balance():
    sqlstatement = "select balance from USER where user_id = 10000"
    cursor.execute(sqlstatement)
    return(cursor.fetchone()[0])

# view all friends with outstanding balance;
def view_friend_outbalance():
    sqlstatement = "select * from USER where Balance > 0 and user_id != 10000"
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)
# view_friend_outbalance()

# view all groups
def view_groups():
    sqlstatement = "SELECT * FROM `group`"
    cursor.execute(sqlstatement)
    
    lst = [("Group ID", "Group Name", "Number of Members", "Balance")] + cursor.fetchall()
    table(lst, "Groups")

    for x in cursor:
        print(x)

    

def view_group_outbalance():
    sqlstatement = "SELECT * FROM `group` WHERE balance > 0"
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)
# view_group_outbalance()


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

# frontend ---------------------------------------------------------------------------

# setting themes
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

# making app window
class MainApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Expense Tracker")
        self.after(1, self.wm_state, 'zoomed')

app = MainApp()

tabview = customtkinter.CTkTabview(master=app, width=1080, height=720)
tabview.pack(padx=20, pady=50)

tabview.add("Expense")  # add tab at the end
tabview.add("Friends")  # add tab at the end
tabview.add("Groups")  # add tab at the end
tabview.set("Expense")  # set currently visible tab
tab1 = tabview.tab("Expense")
tab2 = tabview.tab("Friends")
tab3 = tabview.tab("Groups")


tab1.columnconfigure(index=0, weight=1)
tab1.columnconfigure(index=6, weight=1)
tbalance = customtkinter.CTkLabel(tab1, text="Total Balance:", font=("Segoi UI", 20))
tbalance.grid(row=0, column=1, pady=(30, 5))
abalance = customtkinter.CTkLabel(tab1, text="Php" + str(curr_balance()), font=("Segoi UI", 20), text_color="#31A37C")
abalance.grid(row=0, column=2, pady=(30, 5))

history = customtkinter.CTkLabel(tab1, text="History", font=("Segoe UI", 15))
history.grid(row=1, column=1, pady=5)
search = customtkinter.CTkEntry(tab1, width=300, height=25, corner_radius=100, fg_color="White", border_width=0, text_color="#2B2B2B")
search.grid(row=1, column=3, pady=5, padx=5)
id_search = customtkinter.CTkButton(tab1, width=75, height=30, text="Search by ID", corner_radius=5)
id_search.grid(row=1,column=4, padx=5)
name_search = customtkinter.CTkButton(tab1, width=75, height=30, text="Search by Name", corner_radius=5, fg_color="#4B4947")
name_search.grid(row=1,column=5, pady=5, padx=5)

expenses = customtkinter.CTkScrollableFrame(tab1, width = 720, height = 350, fg_color="#4B4947", corner_radius=0)
expenses.grid(row=2, column=1, columnspan=5, pady=5)

customtkinter.CTkLabel(expenses, text="ID").grid(column=1, row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Name").grid(column=2,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Loaner").grid(column=3,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Loanee").grid(column=4,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Amount").grid(column=5,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Date Created").grid(column=6,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Date Paid").grid(column=7,row=1, padx=10)

transactions = view_all_transaction()
for i in range(len(transactions)):
    for j in range(7):
        if transactions[i][j] == None:
            customtkinter.CTkLabel(expenses, text="-").grid(column=j+1, row=i+2, padx=10)
        else:    
            customtkinter.CTkLabel(expenses, text=transactions[i][j]).grid(column=j+1, row=i+2, padx=10, pady=30)
        
        customtkinter.CTkButton(expenses, text="Settle", width=50, fg_color="#2B2B2B").grid(column=8, row=i+2, padx=(30,2))
        customtkinter.CTkButton(expenses, text="Delete", width=50, fg_color="#2B2B2B").grid(column=9, row=i+2, padx=2)
        customtkinter.CTkButton(expenses, text="Edit", width=50, fg_color="#2B2B2B").grid(column=10, row=i+2, padx=2)



filterby = customtkinter.CTkLabel(tab1, text="Filter By Month", font=("Segoe UI", 15))
filterby.grid(row=3, column=1, pady=5)

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox = customtkinter.CTkComboBox(tab1, values=["January", "February", "March", "April",
                                                   "May", "June", "July", "August",
                                                   "September", "October", "November", "December"],
                                     command=combobox_callback)
combobox.grid(row=3, column=2, pady=5, padx=5)
combobox.set("Month")

borrow = customtkinter.CTkButton(tab1, width=75, height=30, text="Search by ID", corner_radius=5)
borrow.grid(row=3,column=4, pady=5, padx=5)
lend = customtkinter.CTkButton(tab1, width=75, height=30, text="Search by Name", corner_radius=5, fg_color="#4B4947")
lend.grid(row=3,column=5, pady=5, padx=5)


#---------------------------------------user tab ------------------------------------------------------
global users

tab2.columnconfigure(index=0, weight=1)
tab2.columnconfigure(index=6, weight=1)

button_font = font.Font(size=20)
# search bar and buttons
search_box = customtkinter.CTkEntry(tab2, width=300, height=25, corner_radius=100, fg_color="White", border_width=0, text_color="#2B2B2B")
search_box.grid(row=1, column=3, sticky = tk.W, pady = (50, 5), padx = (70, 0))

def deleteLabels():
    for widget in users.winfo_children():
        widget.destroy()

def update_scrollable_frame(result, allData):

    deleteLabels()

    for i in range(len(result)):
        search_label = customtkinter.CTkLabel(users, text = result[i])
        search_label.grid(row=5+i, column=5, columnspan=5, pady=5)


    #orig code startes here
    # search_label = customtkinter.CTkLabel(users, text = result)
    # search_label.grid(row=5, column=1, columnspan=5, pady=5)

def searchNow():
    selected = search_drop.get()
    query = ""  # Initialize the variable with a default value

    if selected == "Search by..":
        query = "SELECT * FROM user"
    if selected == "First Name":
        #search by first name
        query = "SELECT * FROM user where first_name = %s"
    if selected == "Last Name":
        #search by last name
        query = "SELECT * FROM user where last_name = %s"
    if selected == "Middle Name":
        #search by middle name
        query = "SELECT * FROM user where middle_name = %s"
    if selected == "User ID":
       #search by user ID
       query = "SELECT * FROM user where user_id = %s"
    # else:
    #     result = "Select from drop down"
    

    # this is for getting the range of all data usesd for reseting scrollable
    allDataQuery = "SELECT * FROM user"
    allData = cursor.execute(allDataQuery, )
    allData = cursor.fetchall()

    searchVal = search_box.get()
    if searchVal == "":
        result = cursor.execute(query, )
        result = cursor.fetchall()
        update_scrollable_frame(result, allData)

    else:
        name = (searchVal,)
        result = cursor.execute(query, name)
        result = cursor.fetchall()
        update_scrollable_frame(result, allData)

    if not result:
        result = "Record Not Found..."

    # Update the scrollable frame with the new data
   

def defaultDisplay():
    defaultDisplayQuery = "SELECT * FROM user"
    defaultDisplayResult = cursor.execute(defaultDisplayQuery, )
    defaultDisplayResult = cursor.fetchall()
    update_scrollable_frame(defaultDisplayResult)


search_button = customtkinter.CTkButton(tab2, width=75, height=30, text=" Search", corner_radius=5 , command = searchNow)
search_button.grid(row=2,column=3, sticky = tk.W, pady = (5, 5), padx = (70, 0))

#drop down
search_drop = customtkinter.CTkComboBox(tab2, values=["First Name", "Last Name", "Middle Name","User ID",], command=combobox_callback)
search_drop.grid(row=1, column=4, sticky = tk.W, pady = (50, 5))
search_drop.set("Search by..")


users = customtkinter.CTkScrollableFrame(tab2, width=720, height=350, fg_color="#4B4947", corner_radius=0)
users.grid(row=5, column=1, columnspan=5, pady=5)



users = customtkinter.CTkScrollableFrame(tab2, width = 720, height = 350, fg_color="#4B4947", corner_radius=0)
users.grid(row=5, column=1, columnspan=5, pady=5)


addUser = customtkinter.CTkButton(tab2, width=110, height=30, text="Add Friend", corner_radius=5, command = add1)
addUser.grid(row=11,column=5, sticky = tk.E, padx=5, pady=5)

# ==================================== GROUPS ===================================================

tab3.columnconfigure(index=0, weight=1)
tab3.columnconfigure(index=6, weight=1)
totalGroupBalanceLabel = customtkinter.CTkLabel(tab2, text="Total balance from all groups:", font=("Segoi UI", 20))
totalGroupBalanceLabel.grid(row=0, column=1, pady=(30, 5))
totalGroupBalance = customtkinter.CTkLabel(tab2, text="Php" + str(curr_balance()), font=("Segoi UI", 20), text_color="#31A37C")
totalGroupBalance.grid(row=0, column=2, pady=(30, 5))

# history = customtkinter.CTkLabel(tab1, text="Groups", font=("Segoe UI", 15))
# history.grid(row=1, column=1, pady=5)
searchBarGroup = customtkinter.CTkEntry(tab2, width=300, height=25, corner_radius=100, fg_color="White", border_width=0, text_color="#2B2B2B")
searchBarGroup.grid(row=1, column=3, pady=5, padx=5)
searchByGroupID = customtkinter.CTkButton(tab2, width=75, height=30, text="Search by Group ID", corner_radius=5)
searchByGroupID.grid(row=1,column=4, padx=5)
searchByGroupName = customtkinter.CTkButton(tab2, width=75, height=30, text="Search by Group Name", corner_radius=5, fg_color="#4B4947")
searchByGroupName.grid(row=1,column=5, pady=5, padx=5)

expenses = customtkinter.CTkScrollableFrame(tab1, width = 720, height = 350, fg_color="#4B4947", corner_radius=0)
expenses.grid(row=2, column=1, columnspan=5, pady=5)    

customtkinter.CTkLabel(expenses, text="ID").grid(column=1, row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Name").grid(column=2,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Loaner").grid(column=3,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Loanee").grid(column=4,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Amount").grid(column=5,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Date Created").grid(column=6,row=1, padx=10)
customtkinter.CTkLabel(expenses, text="Date Paid").grid(column=7,row=1, padx=10)

transactions = view_all_transaction()
for i in range(len(transactions)):
    for j in range(7):
        if transactions[i][j] == None:
            customtkinter.CTkLabel(expenses, text="-").grid(column=j+1, row=i+2, padx=10)
        else:    
            customtkinter.CTkLabel(expenses, text=transactions[i][j]).grid(column=j+1, row=i+2, padx=10, pady=30)
        
        customtkinter.CTkButton(expenses, text="Settle", width=50, fg_color="#2B2B2B").grid(column=8, row=i+2, padx=(30,2))
        customtkinter.CTkButton(expenses, text="Delete", width=50, fg_color="#2B2B2B").grid(column=9, row=i+2, padx=2)
        customtkinter.CTkButton(expenses, text="Edit", width=50, fg_color="#2B2B2B").grid(column=10, row=i+2, padx=2)



filterby = customtkinter.CTkLabel(tab1, text="Filter By Month", font=("Segoe UI", 15))
filterby.grid(row=3, column=1, pady=5)

def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox = customtkinter.CTkComboBox(tab1, values=["January", "February", "March", "April",
                                                   "May", "June", "July", "August",
                                                   "September", "October", "November", "December"],
                                     command=combobox_callback)
combobox.grid(row=3, column=2, pady=5, padx=5)
combobox.set("Month")

borrow = customtkinter.CTkButton(tab1, width=75, height=30, text="Search by ID", corner_radius=5)
borrow.grid(row=3,column=4, pady=5, padx=5)
lend = customtkinter.CTkButton(tab1, width=75, height=30, text="Search by Name", corner_radius=5, fg_color="#4B4947")
lend.grid(row=3,column=5, pady=5, padx=5)

# runs the app
app.mainloop()