import tkinter as tk
import tkinter.font as font
import customtkinter
import datetime as dt
import mysql.connector as mariadb
from tkinter import messagebox as msg

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
        group_id int(4),
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


cursor.execute('''
    insert into `group` values
    (1023, "Overwatch", 8, 0),
    (1111, "Testing", 4, 0),
    (1024, "Talon", 2, 200.00),
    (1021, "Helix Corporation", 2, 0);
''')
mariadb_connection.commit()

cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
cursor.execute('''
    insert into `transaction` values
    (1, 'Gun Rental', 1021, 10000, 600.00, str_to_date('10/13/2023', '%m/%d/%Y'), NULL, NULL, 10000),
    (2, 'Suit Maintenance', 44444, 11111, 1000.00, str_to_date('05/25/2023','%m/%d/%Y'), NULL, NULL, 11111),
    (3, 'Ice Wall Molder', 11111, 77777, 6900.00, str_to_date('04/12/2020', '%m/%d/%Y'), NULL, NULL, 77777),
    (4, 'Scanners', 11111, 1024, 200.00, str_to_date('01/01/2021', '%m/%d/%Y'), NULL, 1024, NULL),
    (5, 'Bills', 1023, 11111, 200.00, str_to_date('01/02/2023','%m/%d/%Y'), str_to_date('01/10/2023', '%m/%d/%Y'), NULL, 11111),
    (6, 'Utilities', 1111, 11111, 200.00, str_to_date('01/22/2023','%m/%d/%Y'), NULL, 1111, NULL); 

''')
mariadb_connection.commit()

cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
cursor.execute('''
    insert into has values
        (11111, 1023),
        (22222, 1023),
        (44444, 1023),
        (55555, 1023),
        (77777, 1023),
        (88888, 1023),
        (99999, 1023),
        (10000, 1023),
        (11111, 1024),
        (33333, 1024),
        (11111, 1021),
        (66666, 1021),
        (10000, 1111),
        (11111, 1111),
        (22222, 1111),
        (33333, 1111);
''')
mariadb_connection.commit()

### FEATURES ------------------------------------------------------------------------
# add user function
def add_user(user_id, balance, fname, mname, lname):

    if len(user_id) != 5:
        msg.showerror(title="Error", message="Error: Length of User ID should be 5")
    else:
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
        defaultDisplay()
    
# add group function
def add_group(gid, gname, mem_no, balance):
    sql_statement = "INSERT INTO `group` VALUES(" + gid + ",'" + gname + "'" + ","+ mem_no + "," + balance + ");"
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
    query = "SELECT * FROM transaction WHERE transaction_id=" + tid
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

# search a transaction by name
def search_transaction_name(tname):
    query = "SELECT * FROM transaction WHERE transaction_name LIKE '%" + tname + "%'"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

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



##### REPORTS TO BE GENERATED


# view expenses from a certain month
def view_month(month):
    sqlstatement = "SELECT * FROM transaction WHERE MONTH(transaction_date) = " + month
    cursor.execute(sqlstatement)
    for x in cursor:
        print(x)

# view all expenses made with a friend
def search_transaction_friend(fid):
    result=[]
    if (len(fid)==5):
        query = "SELECT * FROM transaction WHERE (user_id=" + str(fid) + " and loaner=10000) or (user_id=10000 and loaner=" + str(fid) + ")"
        result = cursor.execute(query,)
        result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

# view all expenses made with a group
def search_transaction_group(gid):
    result=[]
    if (len(gid)==4):
        query = "SELECT * FROM transaction WHERE (group_id=" + str(gid) + " and loaner=10000) or (user_id=10000 and loaner=" + str(gid) + ")"
        result = cursor.execute(query,)
        result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

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

def add_transaction(tid, tname, loaner, loanee, amount, pdate, gid, uid, add, borlend, type):
    type = input3.get()
    if (len(input3.get())==5):
        if (borlend=="Borrow"):
            uid = 10000
        else:
            loaner = 10000
            uid = type
            loanee = uid            
    elif (len(input3.get())==4):
        if (borlend=="Borrow"):
            uid = 10000
        else:
            loaner = 10000
            uid = type
            loanee = uid
    
    # getting all the transaction ids
    cursor.execute("SELECT transaction_id FROM transaction")
    tids = [str(x[0]) for x in cursor.fetchall()]

    # getting all the friend and group ids
    cursor.execute("SELECT user_id FROM user WHERE user_id != 10000")
    lids = [str(x[0]) for x in cursor.fetchall()]
    cursor.execute("SELECT group_id FROM `group`")
    lids.extend([str(x[0]) for x in cursor.fetchall()])

    # validation of inputs
    if tid == "" or tname == "" or loaner == "" or loanee=="" or amount=="":
        msg.showerror(title="Error", message="Error: Missing Field/s")
    elif not tid.isnumeric():
        msg.showerror(title="Error", message="Error: Transaction ID should only contain numerals")
    elif tid in tids:  
        msg.showerror(title="Error", message="Error: Transaction ID is already taken")
    elif len(tid) > 5:
        msg.showerror(title="Error", message="Error: Length of Transaction ID should be less than 6")
    elif not input3.get() in lids:
        msg.showerror(title="Error", message="Error: Loaner/Loanee ID does not exist")        
    elif not(len(input3.get()) == 5 or len(input3.get()) == 4):
        msg.showerror(title="Error", message="Error: Length of Loaner/Loanee ID should be 4 or 5")
    elif len(tname)>20:
        msg.showerror(title="Error", message="Error: Length of Transaction Name should be less than 21")  
    elif not amount.isnumeric():
        msg.showerror(title="Error", message="Error: Amount should only contain numerals") 
    elif len(amount)>6:  
        msg.showerror(title="Error", message="Error: Amount should be less than 1000000")
    else:
        loaner = str(loaner)
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
                sql_statement = "INSERT INTO transaction VALUES("+tid+", '"+ tname +"', "+ loaner +", "+ loanee +", "+ amount +", str_to_date('"+ tdate +"', '%m/%d/%Y'), " + "NULL, NULL, " + str(uid) + ")"
        
        cursor.execute(sql_statement)
        mariadb_connection.commit()
        add.destroy()
        defaultTransactionDisplay()



        # update balance of user
        if (borlend=="Borrow"):
            if (len(loaner)==5):
                upid = "user_id"
                tbl = "user"
            else:
                upid = "group_id"
                tbl = "`group`"
            cursor.execute("UPDATE user SET balance=balance+"+amount+" where user_id=10000")
            mariadb_connection.commit()
            cursor.execute("UPDATE "+tbl+" SET balance=balance-"+amount+" where "+upid+"="+loaner)
            mariadb_connection.commit()
        elif (borlend=="Lend"):
            if (len(loanee)==5):
                upid = "user_id"
                tbl = "user"
            else:
                upid = "group_id"
                tbl = "`group`"
            cursor.execute("UPDATE user SET balance=balance-"+amount+" where user_id=10000")
            mariadb_connection.commit()
            cursor.execute("UPDATE "+tbl+" SET balance=balance+"+amount+" where "+upid+"="+loanee)
            mariadb_connection.commit()
        displayBal()

        # update balance of users in the group

def addTransaction(borlend):
    add = customtkinter.CTkToplevel()
    add.grab_set()

    global input1
    global input2
    global input3
    global input4

    lbl1 = customtkinter.CTkLabel(add, text="Transaction ID")
    input1 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl1.pack()
    input1.pack()

    lbl2 = customtkinter.CTkLabel(add, text="Transaction Name")
    input2 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl2.pack()
    input2.pack()

    type = 0
    match borlend:
        case "Borrow":
            lbl3 = customtkinter.CTkLabel(add, text="Loaner ID")
            input3 = customtkinter.CTkEntry(add, width=350, height=20)
            lbl3.pack()
            input3.pack()
            type = 10000
        case "Lend":
            lbl3 = customtkinter.CTkLabel(add, text="Loanee ID")
            input3 = customtkinter.CTkEntry(add, width=350, height=20)
            lbl3.pack()
            input3.pack()

    lbl4 = customtkinter.CTkLabel(add, text="Amount")
    input4 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl4.pack()
    input4.pack()
    

    gid = "NULL"
    uid = "NULL"


    button = customtkinter.CTkButton(add, text="Add Transaction", command=lambda: add_transaction(input1.get(), input2.get(), input3.get(), str(type), input4.get(), "NULL", str(gid), str(uid), add, borlend, type))
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


#--------------------------------------- transaction tab ------------------------------------------------------
global transactions

def deleteTransactionLabels():
    for widget in transactions.winfo_children():
        widget.destroy()

def validateDate(dte):
    try:
        if dte != dt.datetime.strptime(dte, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return False
    except ValueError:
        return True

def edit_transaction(id):

    # getting all the friend and group ids
    cursor.execute("SELECT user_id FROM user")
    lids = [str(x[0]) for x in cursor.fetchall()]
    cursor.execute("SELECT group_id FROM `group`")
    lids.extend([str(x[0]) for x in cursor.fetchall()])

    # validation for edit inputs
    if tnameInput.get() == "" or loanerInput.get() == "" or loanerInput.get() == "" or tdateInput.get()=="":
        msg.showerror(title="Error", message="Error: Missing Field/s")
    elif len(tnameInput.get())>21:
        msg.showerror(title="Error", message="Error: Missing Field/s")
    elif not loanerInput.get() in lids:
        msg.showerror(title="Error", message="Error: Loaner ID does not exist")   
    elif not loaneeInput.get() in lids:
        msg.showerror(title="Error", message="Error: Loanee ID does not exist")
    elif validateDate(tdateInput.get()):
        msg.showerror(title="Error", message="Error: Incorrect data format, should be YYYY-MM-DD")
    else:  
        #update transaction info using this query
        query = "UPDATE transaction SET transaction_name = %s, loaner = %s, loanee = %s, transaction_date = %s WHERE transaction_id = %s"
        inputs = (tnameInput.get(), loanerInput.get(), loaneeInput.get(), tdateInput.get(), id)
        cursor.execute(query, inputs)
        mariadb_connection.commit()
        defaultTransactionDisplay()


def editTransactionNow(id, index):
    edit = customtkinter.CTkToplevel()
    edit.grab_set()

    # get the tuple
    query = "SELECT * FROM transaction WHERE transaction_id = %s"
    name = (id, )
    result = cursor.execute(query, name)
    result = cursor.fetchall()

    global tnameInput
    global loanerInput
    global loaneeInput
    global tdateInput

    #get values you want to be updated
    tname = customtkinter.CTkLabel(edit, text="Transaction Name")
    tname.pack()
    tnameInput = customtkinter.CTkEntry(edit, width=350, height=20)
    tnameInput.insert(0, result[0][1])
    tnameInput.pack()

    loaner = customtkinter.CTkLabel(edit, text="Loaner")
    loaner.pack()
    loanerInput = customtkinter.CTkEntry(edit, width=350, height=20)
    loanerInput.insert(0, result[0][2])
    loanerInput.pack()

    loanee = customtkinter.CTkLabel(edit, text="Loanee")
    loanee.pack()
    loaneeInput = customtkinter.CTkEntry(edit, width=350, height=20)
    loaneeInput.insert(0, result[0][3])
    loaneeInput.pack()

    tdate = customtkinter.CTkLabel(edit, text="Transaction Date")
    tdate.pack()
    tdateInput = customtkinter.CTkEntry(edit, width=350, height=20)
    tdateInput.insert(0, result[0][5])
    tdateInput.pack()

    button = customtkinter.CTkButton(edit, text="Submit Edit", command=lambda: edit_transaction(id))
    button.pack(padx=10, pady=10)

def update_transaction_scrollable_frame(result):
    #delete existing labels
    deleteTransactionLabels()

    for i, transaction in enumerate(result):
        num = 0
        id_reference = str(transaction[0])
        if transaction[6] != None:
            ste = "normal"
        else:
            ste="disabled"
        customtkinter.CTkButton(transactions, text="Settle", width=50, fg_color="#2B2B2B", command=lambda d= id_reference :settleTransaction(d)).grid(column=9, row=5+i, sticky= tk.E, padx=(70,10), pady = (30, 0))
        customtkinter.CTkButton(transactions, text="Delete", width=50, fg_color="#2B2B2B", state=ste, command=lambda d= id_reference :deleteTransaction(d)).grid(column=10, row=5+i, sticky= tk.E, padx=(0,10), pady = (30, 0))
        customtkinter.CTkButton(transactions, text="Edit", width=50, fg_color="#2B2B2B", command=lambda  d= id_reference:editTransactionNow(d, i)).grid(column=11, row=5+i, sticky= tk.E, padx=(0,5), pady = (30, 0))
    
        for data in transaction:
            if num < 7:
                search_label = customtkinter.CTkLabel(transactions, text = data)
                search_label.grid(row=5+i, column= num, padx= (40, 0), pady = (30, 0))
            num +=1 


def searchTransactionNow():
    selected = tsearch_drop.get()
    query = ""  # Initialize the variable with a default value
    result = []

    searchVal = transactionSearch.get()
    if selected == "Search by..":
        query = "SELECT * FROM transaction ORDER BY transaction_name"
    if selected == "Transaction Name":
        #search by transaction name
        search_transaction_name(searchVal)
    if selected == "Friend ID":
        #search by friend ID
        search_transaction_friend(searchVal)
    if selected == "Group ID":
        #search by Group ID
        search_transaction_group(searchVal)
    # else:
    #     result = "Select from drop down"

    if (result != []):
        update_transaction_scrollable_frame(result)

def defaultTransactionDisplay():
    query = "SELECT * FROM transaction ORDER BY transaction_id"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

def deleteTransaction(id):
    query = "DELETE FROM transaction WHERE transaction_id = %s"
    toDel = (id, )
    cursor.execute(query, toDel)
    mariadb_connection.commit()
    defaultTransactionDisplay()

def displayByMonth(month):
    query = ""
    match month:
        case "January":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=1 ORDER BY transaction_id"
        case "February":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=2 ORDER BY transaction_id"
        case "March":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=3 ORDER BY transaction_id"
        case "April":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=4 ORDER BY transaction_id"
        case "May":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=5 ORDER BY transaction_id"
        case "June":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=6 ORDER BY transaction_id"
        case "July":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=7 ORDER BY transaction_id"
        case "August":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=8 ORDER BY transaction_id"
        case "September":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=9 ORDER BY transaction_id"
        case "October":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=10 ORDER BY transaction_id"
        case "November":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=11 ORDER BY transaction_id"
        case "December":
            query = "SELECT * FROM transaction WHERE MONTH(transaction_date)=12 ORDER BY transaction_id"
        case _:
            query = "SELECT * FROM transaction ORDER BY transaction_id"

    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

def settleTransaction(id):
    # updates transaction and adds payment date
    curr = dt.datetime.now()
    curdate = str(curr.month) + "/" + str(curr.day) + "/" + str(curr.year)
    query = "UPDATE transaction SET payment_date=str_to_date('"+curdate+"', '%m/%d/%Y') WHERE transaction_id =" + id
    cursor.execute(query)
    mariadb_connection.commit()
    defaultTransactionDisplay()


    # update balances of users
    # update balance of groups
    # update balance of users in the group



tab1.columnconfigure(index=0, weight=1)
tab1.columnconfigure(index=7, weight=1)
button_font = font.Font(size=20)
tbalance = customtkinter.CTkLabel(tab1, text="Total Balance:", font=("Segoi UI", 20))
tbalance.grid(row=0, column=1, pady=(30, 5))

abalance = None
def displayBal():
    global abalance
    if abalance!=None:
        abalance.destroy()
    abalance = customtkinter.CTkLabel(tab1, text="Php" + str(curr_balance()), font=("Segoi UI", 20), text_color="#31A37C")
    abalance.grid(row=0, column=2, pady=(30, 5))


tab1.after_idle(displayBal)

history = customtkinter.CTkButton(tab1, text="Show History", font=("Segoe UI", 15), command = defaultTransactionDisplay)
history.grid(row=1, column=1, pady=5)

transactionSearch = customtkinter.CTkEntry(tab1, width=300, height=25, corner_radius=100, fg_color="White", border_width=0, text_color="#2B2B2B")
transactionSearch.grid(row=1, column=3, pady=5, padx=5)

id_search = customtkinter.CTkButton(tab1, width=75, height=30, text="Search by ID", corner_radius=5, command =lambda: search_transaction_id(transactionSearch.get()))
id_search.grid(row=1,column=4, padx=5)

custom_search = customtkinter.CTkButton(tab1, width=75, height=30, text="Custom Search", corner_radius=5, fg_color="#4B4947", command= searchTransactionNow)
custom_search.grid(row=1,column=5, pady=5, padx=5)

tsearch_drop = customtkinter.CTkComboBox(tab1, values=["Transaction Name", "Friend ID", "Group ID"])
tsearch_drop.grid(row=1, column=6, sticky = tk.W, pady = 5, padx=5)
tsearch_drop.set("Search by..")

transactions = customtkinter.CTkScrollableFrame(tab1, width = 900, height = 350, fg_color="#4B4947", corner_radius=0)
transactions.grid(row=3, column=1, columnspan=6, pady=(0,5))

transactionsLabel = customtkinter.CTkLabel(tab1, width=918, height= 30, fg_color = "#242424", text= "")
transactionsLabel.grid(row=2, column=1, columnspan=6, pady= (10,0), padx = (0,0))
tidLbl=customtkinter.CTkLabel(tab1, width=30, height= 20, fg_color = "#242424", text= "ID")
tidLbl.place(x=105 , y =120)
tnameLbl=customtkinter.CTkLabel(tab1, width=50, height= 20, fg_color = "#242424", text= "Expense Name")
tnameLbl.place(x=175 , y =120)
loanerLbl=customtkinter.CTkLabel(tab1, width=50, height= 20, fg_color = "#242424", text= "Loaner")
loanerLbl.place(x=296 , y =120)
loaneeLbl=customtkinter.CTkLabel(tab1, width=50, height= 20, fg_color = "#242424", text= "Loanee")
loaneeLbl.place(x=370 , y =120)
amtLbl=customtkinter.CTkLabel(tab1, width=50, height= 20, fg_color = "#242424", text= "Amount")
amtLbl.place(x=450 , y =120)
tdateLbl=customtkinter.CTkLabel(tab1, width=50, height= 20, fg_color = "#242424", text= "Date Created")
tdateLbl.place(x=532 , y =120)
pdateLbl=customtkinter.CTkLabel(tab1, width=50, height= 20, fg_color = "#242424", text= "Payment Date")
pdateLbl.place(x=633 , y =120)



filterByMonth = customtkinter.CTkLabel(tab1, text="Filter By Month", font=("Segoe UI", 15))
filterByMonth.grid(row=4, column=1, pady=5)

monthFilter = customtkinter.CTkComboBox(tab1, values=["January", "February", "March", "April",
                                                   "May", "June", "July", "August",
                                                   "September", "October", "November", "December"],
                                     command=displayByMonth)
monthFilter.grid(row=4, column=2, pady=5, padx=5)
monthFilter.set("Month")


borrow = customtkinter.CTkButton(tab1, width=75, height=30, text="     Borrow     ", corner_radius=5, command= lambda: addTransaction("Borrow"))
borrow.grid(row=4,column=5, pady=5, padx=5)
lend = customtkinter.CTkButton(tab1, width=75, height=30, text="      Lend      ", corner_radius=5, fg_color="#4B4947", command= lambda: addTransaction("Lend"))
lend.grid(row=4,column=6, pady=5, padx=5)

tab1.after_idle(defaultTransactionDisplay)

#---------------------------------------user tab ------------------------------------------------------
global users

def deleteLabels():
    for widget in users.winfo_children():
        widget.destroy()

def edit_user(id):
    #update user info using this query
    query = "UPDATE user SET first_name = %s, middle_name = %s, last_name = %s WHERE user_id = %s"
    inputs = (fnameInput.get(), mnameInput.get(), lnameInput.get(), id)
    cursor.execute(query, inputs)
    mariadb_connection.commit()
    defaultDisplay()

def editNow(id, index):
    edit = customtkinter.CTkToplevel()
    edit.grab_set()

    # get the tuple
    query = "SELECT * FROM user WHERE user_id = %s"
    name = (id, )
    result = cursor.execute(query, name)
    result = cursor.fetchall()

    global fnameInput
    global mnameInput
    global lnameInput

    #get values you want to be updated
    fname = customtkinter.CTkLabel(edit, text="First Name")
    fname.pack()
    fnameInput = customtkinter.CTkEntry(edit, width=350, height=20)
    fnameInput.insert(0, result[0][2])
    fnameInput.pack()

    mname = customtkinter.CTkLabel(edit, text="Middle Name")
    mname.pack()
    mnameInput = customtkinter.CTkEntry(edit, width=350, height=20)
    mnameInput.insert(0, result[0][3])
    mnameInput.pack()

    lname = customtkinter.CTkLabel(edit, text="Last Name")
    lname.pack()
    lnameInput = customtkinter.CTkEntry(edit, width=350, height=20)
    lnameInput.insert(0, result[0][4])
    lnameInput.pack()

    button = customtkinter.CTkButton(edit, text="Submit Edit", command=lambda: edit_user(id))
    button.pack(padx=10, pady=10)

def update_scrollable_frame(result):
    #delete existing labels
    deleteLabels()

    for i, user in enumerate(result):
        num = 0
        id_reference = str(user[0])
        customtkinter.CTkButton(users, text="Delete", width=50, fg_color="#2B2B2B", command=lambda d= id_reference :deleteUser(d)).grid(column=11, row=5+i, sticky= tk.E, padx=(70,10), pady = (30, 0))
        customtkinter.CTkButton(users, text="Edit", width=50, fg_color="#2B2B2B", command=lambda  d= id_reference:editNow(d, i)).grid(column=12, row=5+i, sticky= tk.E, padx=(0,5), pady = (30, 0))

        for data in user:
            search_label = customtkinter.CTkLabel(users, text = data)
            search_label.grid(row=5+i, column= num, padx= (40, 0), pady = (30, 0))
            num +=1 

def searchNow():
    selected = search_drop.get()
    query = ""  # Initialize the variable with a default value

    if selected == "Search by..":
        query = "SELECT * FROM user order by first_name"
    if selected == "Search by..":
        query = "SELECT * FROM user order by first_name"
    if selected == "First Name":
        #search by first name
        query = "SELECT * FROM user where first_name = %s order by first_name "
    if selected == "Last Name":
        #search by last name
        query = "SELECT * FROM user where last_name = %s order by first_name"
    if selected == "Middle Name":
        #search by middle name
        query = "SELECT * FROM user where middle_name = %s order by first_name"
    if selected == "User ID":
       #search by user ID
       query = "SELECT * FROM user where user_id = %s order by first_name"
    # else:
    #     result = "Select from drop down"
    

    searchVal = search_box.get()
    if searchVal == "":
        result = cursor.execute(query, )
        result = cursor.fetchall()
        update_scrollable_frame(result)

    else:
        # Update the scrollable frame with the new data
        name = (searchVal,)
        result = cursor.execute(query, name)
        result = cursor.fetchall()
        update_scrollable_frame(result)
    
    if not result:
            result = "Record Not Found..."

def defaultDisplay():
    query = "SELECT * FROM user ORDER BY first_name"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_scrollable_frame(result)

def deleteUser(id):
    query = "DELETE FROM user WHERE user_id = %s"
    toDel = (id, )
    cursor.execute(query, toDel)
    mariadb_connection.commit()
    defaultDisplay()

def viewFriendOutbal():
    query = "select * from USER where Balance > 0 and user_id != 10000 order by balance desc"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_scrollable_frame(result)
    

tab2.columnconfigure(index=0, weight=1)
tab2.columnconfigure(index=6, weight=1)

button_font = font.Font(size=20)
# search bar and buttons
search_box = customtkinter.CTkEntry(tab2, width=300, height=25, corner_radius=100, fg_color="White", border_width=0, text_color="#2B2B2B")
search_box.grid(row=1, column=3, sticky = tk.W, pady = (50, 5), padx = (70, 0))

#Buttons
search_button = customtkinter.CTkButton(tab2, width=75, height=30, text="Search", corner_radius=5 , command = searchNow)
search_button.grid(row=2,column=3, sticky = tk.W, pady = (5, 5), padx = (70, 0))

viewAll_button = customtkinter.CTkButton(tab2, width=75, height=30, text="View All", corner_radius=5 , command = defaultDisplay, fg_color="#565B5E")
viewAll_button.grid(row=2,column=3, sticky = tk.W, pady = (5, 5), padx = (150, 0))

viewOutstanding_button = customtkinter.CTkButton(tab2, width=75, height=30, text="Outstanding Records", corner_radius=5 , command = viewFriendOutbal, fg_color="#242424")
viewOutstanding_button.grid(row=2,column=3, sticky = tk.W, pady = (5, 5), padx = (230, 0))
#drop down
search_drop = customtkinter.CTkComboBox(tab2, values=["First Name", "Last Name", "Middle Name","User ID",])
search_drop.grid(row=1, column=4, sticky = tk.W, pady = (50, 5))
search_drop.set("Search by..")

#Scrollable table
users = customtkinter.CTkScrollableFrame(tab2, width = 720, height = 350, fg_color="#4B4947", corner_radius=0)
users.grid(row=6, column=1, columnspan=5, pady=(0,0))

#Label
usersLabel = customtkinter.CTkLabel(tab2, width=737, height= 30, fg_color = "#242424", text= "")
usersLabel.grid(row=5, column=1, columnspan=5, pady= (10,0), padx = (0,0))
idLbl=customtkinter.CTkLabel(tab2, width=50, height= 20, fg_color = "#242424", text= "ID")
idLbl.place(x=200 , y =140)
balLbl=customtkinter.CTkLabel(tab2, width=50, height= 20, fg_color = "#242424", text= "Balance")
balLbl.place(x=280 , y =140)
fnameLbl=customtkinter.CTkLabel(tab2, width=50, height= 20, fg_color = "#242424", text= "First Name")
fnameLbl.place(x=370 , y =140)
mnameLbl=customtkinter.CTkLabel(tab2, width=50, height= 20, fg_color = "#242424", text= "Middle Name")
mnameLbl.place(x=460 , y =140)
lnameLbl=customtkinter.CTkLabel(tab2, width=50, height= 20, fg_color = "#242424", text= "Last Name")
lnameLbl.place(x=560 , y =140)

#Add user 
addUser = customtkinter.CTkButton(tab2, width=110, height=30, text="Add Friend", corner_radius=5, command = add1)
addUser.grid(row=11,column=5, sticky = tk.E, padx=5, pady= (10,0))

# ==================================== GROUPS ===================================================

global groups

def editGroup(id):
    #update group info using this query
    query = "UPDATE `group` SET group_name = %s WHERE group_id = %s"
    inputs = (groupNameInput.get(), id)
    cursor.execute(query, inputs)
    mariadb_connection.commit()
    defaultGroupDisplay()

def editGroupNow(id, index):
    edit = customtkinter.CTkToplevel()
    edit.grab_set()

    # get the tuple
    query = "SELECT * FROM `group` WHERE group_id = %s"
    name = (id, )
    result = cursor.execute(query, name)
    result = cursor.fetchall()

    global groupNameInput

    #get values you want to be updated
    groupNameInput = customtkinter.CTkLabel(edit, text="Group Name")
    groupNameInput.pack()
    groupNameInput = customtkinter.CTkEntry(edit, width=350, height=20)
    groupNameInput.insert(0, result[0][1])
    groupNameInput.pack()

    button = customtkinter.CTkButton(edit, text="Submit Edit", command=lambda: editGroup(id))
    button.pack(padx=10, pady=10)

def deleteGroup(id):
    query = "DELETE FROM `group` WHERE group_id = %s"
    toDel = (id, )
    cursor.execute(query, toDel)
    mariadb_connection.commit()
    defaultGroupDisplay()

def deleteGroupLabels():
    for widget in groups.winfo_children():
        widget.destroy()

def update_group_scrollable_frame(result):
    #delete existing labels
    deleteGroupLabels()

    for i, group in enumerate(result):
        num = 0 
        id_reference = str(group[0])
        customtkinter.CTkButton(groups, text="Delete", width=50, fg_color="#2B2B2B", command=lambda g=id_reference:deleteGroup(g)).grid(column=11, row=5+i, sticky= tk.E, padx=(50,10), pady = (30, 0))
        customtkinter.CTkButton(groups, text="Edit", width=50, fg_color="#2B2B2B", command=lambda:editGroupNow(id_reference, i)).grid(column=12, row=5+i, sticky= tk.E, padx=(0,5), pady = (30, 0))

        for data in group:
            search_label = customtkinter.CTkLabel(groups, text = data)
            search_label.grid(row=5+i, column= num, padx= (40, 0), pady = (30, 0))
            num +=1 

def defaultGroupDisplay():
    query = "SELECT * FROM `group` ORDER BY group_id"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_group_scrollable_frame(result)
    
def showGroupWithOutstandingBalance():
    query = "SELECT * FROM `group` where balance > 0 ORDER BY balance"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_group_scrollable_frame(result)

def getAllGroupBalance():
    query = "SELECT sum(balance) FROM `group`"
    cursor.execute(query)
    return(cursor.fetchone()[0])
    
# search a group by id
def searchGroupByID(id):
    query = "SELECT * FROM `group` WHERE group_id=" + id
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_group_scrollable_frame(result)
    
# search a group by name
def searchGroupByName(name):
    query = "SELECT * FROM `group` WHERE group_name LIKE '%" + name + "%'"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_group_scrollable_frame(result)

def addNewGroup():
    add = customtkinter.CTkToplevel()
    add.grab_set()

    global newGroupID
    global newGroupName
    # global newGroupMembers
    # global newGroupBalance

    lbl1 = customtkinter.CTkLabel(add, text="Group ID")
    newGroupID = customtkinter.CTkEntry(add, width=350, height=20)
    lbl1.pack()
    newGroupID.pack()

    lbl2 = customtkinter.CTkLabel(add, text="Group Name")
    newGroupName = customtkinter.CTkEntry(add, width=350, height=20)
    lbl2.pack()
    newGroupName.pack()

    # member parameter is set to 1 initially (self only)
    button = customtkinter.CTkButton(add, text="Add Group", command=lambda: add_group(newGroupID.get(), newGroupName.get(), str(1), str(0)))
    button.pack(padx=10, pady=10)

tab3.columnconfigure(index=0, weight=1)
tab3.columnconfigure(index=7, weight=1)
button_font = font.Font(size=20)

totalBalanceFromGroups = customtkinter.CTkLabel(tab3, text="Total balance from groups:  ", font=("Segoi UI", 20))
totalBalanceFromGroups.grid(row=0, column=1, pady=(30, 5))
totalBalanceFromGroupsValue = customtkinter.CTkLabel(tab3, text="PHP. " + str(getAllGroupBalance()), font=("Segoi UI", 20), text_color="#31A37C")
totalBalanceFromGroupsValue.grid(row=0, column=2, pady=(30, 5))

searchBar = customtkinter.CTkEntry(tab3, width=200, height=25, corner_radius=100, fg_color="White", border_width=0, text_color="#2B2B2B")
searchBar.grid(row=1, column=1, pady=5, padx=5)

searchByGroupIDBtn = customtkinter.CTkButton(tab3, width=75, height=30, text="Search by Group ID", corner_radius=5, command = lambda: searchGroupByID(searchBar.get()) )
searchByGroupIDBtn.grid(row=1,column=2, padx=5)

searchByGroupNameBtn = customtkinter.CTkButton(tab3, width=75, height=30, text="Search by Group Name", corner_radius=5, fg_color="#4B4947", command = lambda: searchGroupByName(searchBar.get()))
searchByGroupNameBtn.grid(row=1,column=3, pady=5, padx=5)

# CREATES THE TABLE
groups = customtkinter.CTkScrollableFrame(tab3, width = 550, height = 350, fg_color="#4B4947", corner_radius=0)
groups.grid(row=3, column=1, columnspan=6, pady=(0,5))

groupLabel = customtkinter.CTkLabel(tab3, width=570, height= 30, fg_color = "#242424", text= "")
groupLabel.grid(row=2, column=1, columnspan=6, pady= (10,0), padx = (0,0))
groupIDLabel=customtkinter.CTkLabel(tab3, width=30, height= 20, fg_color = "#242424", text= "Group ID")
groupIDLabel.place(x=275 , y =120)
groupNameLabel=customtkinter.CTkLabel(tab3, width=50, height= 20, fg_color = "#242424", text= "Group Name")
groupNameLabel.place(x=375 , y =120)
memberNumberLabel=customtkinter.CTkLabel(tab3, width=50, height= 20, fg_color = "#242424", text= "Member Count")
memberNumberLabel.place(x=475 , y =120)
groupBalanceLabel=customtkinter.CTkLabel(tab3, width=50, height= 20, fg_color = "#242424", text= "Balance")
groupBalanceLabel.place(x=575 , y =120)


# add new group
addGroupBtn = customtkinter.CTkButton(tab3, text="Add group", font=("Segoe UI", 15), command = addNewGroup)
addGroupBtn.grid(row=4, column=1, pady=5)

# all groups are shown
showAllGroups = customtkinter.CTkButton(tab3, text="Show all groups", font=("Segoe UI", 15), command = defaultGroupDisplay)
showAllGroups.grid(row=4, column=2, pady=5)

# only groups with outstanding balance are shown
showGroupsWithBalance = customtkinter.CTkButton(tab3, text="Show outstanding", font=("Segoe UI", 15), command = showGroupWithOutstandingBalance)
showGroupsWithBalance.grid(row=4, column=3, pady=5)

# runs the app
app.mainloop()