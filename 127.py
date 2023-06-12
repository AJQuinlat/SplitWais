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
mariadb_connection = mariadb.connect(user="root", password="addymae10", host="localhost", port="3306")
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

### FUNCTIONS ------------------------------------------------------------------------
# add user function
def add_user(user_id, fname, mname, lname):

    #set deafult balance
    balance = "0.00"

    #search if id is existing
    searchQuery = "SELECT COUNT(*) FROM  user where user_id = %s"
    idsearch = (user_id,)
    result = cursor.execute(searchQuery, idsearch)
    result = cursor.fetchall()

    if len(user_id) != 5:
        msg.showerror(title="Error", message="Error: Length of User ID should be 5")
    elif not user_id.isnumeric():
       msg.showerror(title="Error", message="Error: User ID should only contain numerals")
    else:
        #if there is no same existing id 
        if result[0][0] == 0:
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
            msg.showinfo("User added", "User has been added successfully")
            defaultDisplay()
        else:
            msg.showerror(title="Error", message="Error: User ID is already in used.") 

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
    

# delete transaction by id
def del_transaction(tid):
    sqlstatement = "DELETE FROM transaction WHERE transaction_id = " + tid
    cursor.execute(sqlstatement)
    mariadb_connection.commit()

# delete all settled transactions
def clear_transaction():
    cursor.execute("DELETE FROM transaction WHERE payment_date IS NOT NULL;")
    mariadb_connection.commit()

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

# view all expenses made with a friend
def search_transaction_friend(fid):
    result=[]
    if (len(fid)==5):
        query = "SELECT * FROM transaction WHERE (user_id=" + str(fid) + " and loaner=11111) or (user_id=11111 and loaner=" + str(fid) + ")"
        result = cursor.execute(query,)
        result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

# view all expenses made with a group
def search_transaction_group(gid):
    result=[]
    if (len(gid)==4):
        query = "SELECT * FROM transaction WHERE (group_id=" + str(gid) + " and loaner=11111) or (user_id=11111 and loaner=" + str(gid) + ")"
        result = cursor.execute(query,)
        result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

# view current balance from all expenses
def curr_balance():
    sqlstatement = "select balance from USER where user_id = 11111"
    cursor.execute(sqlstatement)
    return(cursor.fetchone()[0])

def add1():
    add = customtkinter.CTkToplevel()
    add.grab_set()

    global input1
    global input2
    global input3
    global input4

    lbl1 = customtkinter.CTkLabel(add, text="User ID")
    input1 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl1.pack()
    input1.pack()

    lbl2 = customtkinter.CTkLabel(add, text="First Name")
    input2 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl2.pack()
    input2.pack()

    lbl3 = customtkinter.CTkLabel(add, text="Middle Name")
    input3 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl3.pack()
    input3.pack()

    lbl4 = customtkinter.CTkLabel(add, text="Last Name")
    input4 = customtkinter.CTkEntry(add, width=350, height=20)
    lbl4.pack()
    input4.pack()

    button = customtkinter.CTkButton(add, text="Add User", command=lambda: add_user(input1.get(), input2.get(), input3.get(), input4.get()))
    button.pack(padx=10, pady=10)

def add_transaction(tid, tname, loaner, loanee, amount, pdate, gid, uid, add, borlend, type):
    type = input3.get()
    if (len(input3.get())==5):
        if (borlend=="Borrow"):
            uid = 11111
        else:
            loaner = 11111
            uid = type
            loanee = uid            
    elif (len(input3.get())==4):
        if (borlend=="Borrow"):
            uid = 11111
        else:
            loaner = 11111
            uid = type
            loanee = uid
    
    # getting all the transaction ids
    cursor.execute("SELECT transaction_id FROM transaction")
    tids = [str(x[0]) for x in cursor.fetchall()]

    # getting all the friend and group ids
    cursor.execute("SELECT user_id FROM user WHERE user_id != 11111")
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
        msg.showinfo("Transaction Added", "Transaction has been added successfully")
        defaultTransactionDisplay()



        # update balance of user
        if (borlend=="Borrow"):
            if (len(loaner)==5):
                upid = "user_id"
                tbl = "user"
            else:
                upid = "group_id"
                tbl = "`group`"

                # get all the users from a group
                cursor.execute("SELECT user_id FROM has NATURAL JOIN `group` WHERE group_id="+loaner)
                gusers = [x[0] for x in cursor.fetchall()]
                # update user balance from group transaction
                grpamt=str(float(amount)/float(len(gusers)))
                for user in gusers:
                    cursor.execute("UPDATE user SET balance=balance-"+grpamt+" where user_id="+str(user))

            cursor.execute("UPDATE user SET balance=balance+"+amount+" where user_id=11111")
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

                # get all the users from a group
                cursor.execute("SELECT user_id FROM has NATURAL JOIN `group` WHERE group_id="+loanee)
                gusers = [x[0] for x in cursor.fetchall()]
                # update user balance from group transaction
                grpamt=str(float(amount)/float(len(gusers)))
                for user in gusers:
                    cursor.execute("UPDATE user SET balance=balance+"+grpamt+" where user_id="+str(user))

            cursor.execute("UPDATE user SET balance=balance-"+amount+" where user_id=11111")
            mariadb_connection.commit()
            cursor.execute("UPDATE "+tbl+" SET balance=balance+"+amount+" where "+upid+"="+loanee)
            mariadb_connection.commit()
        displayBal()

        # update balance of users in the group

def addTransaction(borlend):
    add = customtkinter.CTkToplevel()
    add.grab_set()
    add.title("Add Transaction")
    add.after(201, lambda: add.iconbitmap('splitwais.ico'))

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
            type = 11111
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
        self.title("Split Wais")
        self.after(1, self.wm_state, 'zoomed')

app = MainApp()
app.iconbitmap("splitwais.ico")

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
        # get transaction info
        cursor.execute("SELECT * FROM transaction WHERE transaction_id="+id)
        curtrans = cursor.fetchone()
        amt = str(curtrans[4])
        loaner = str(curtrans[2])
        loanee = str(curtrans[3])

        # edit loaner and loanee balance

        # checks if loaner is a user or a group
        if len(loanerInput.get())==5:
            cursor.execute("UPDATE user SET balance=balance-"+amt+" where user_id="+loanerInput.get())
        elif len(loanerInput.get())==4:
            cursor.execute("UPDATE `group` SET balance=balance-"+amt+" where group_id="+loanerInput.get())

            # update user through group
        
        # checks if original transaction had a user or a group
        if len(loaner)==5:
            cursor.execute("UPDATE user SET balance=balance+"+amt+" where user_id="+loaner)
        elif len(loaner)==4:
            cursor.execute("UPDATE `group` SET balance=balance+"+amt+" where group_id="+loaner)

            # update user through group

        
        # checks if loanee is a user or a group
        if len(loaneeInput.get())==5:
            cursor.execute("UPDATE user SET balance=balance+"+amt+" where user_id="+loaneeInput.get())
        elif len(loaneeInput.get())==4:
            cursor.execute("UPDATE `group` SET balance=balance+"+amt+" where group_id="+loaneeInput.get())

            # update user through group


        # checks if original transaction had a user or a group
        if len(loanee)==5:
            cursor.execute("UPDATE user SET balance=balance-"+amt+" where user_id="+loanee)
        elif len(loanee)==4:
            cursor.execute("UPDATE `group` SET balance=balance-"+amt+" where group_id="+loanee)

            # update user through group


        #update transaction info using this query
        query = "UPDATE transaction SET transaction_name = %s, loaner = %s, loanee = %s, transaction_date = %s WHERE transaction_id = %s"
        inputs = (tnameInput.get(), loanerInput.get(), loaneeInput.get(), tdateInput.get(), id)
        cursor.execute(query, inputs)
        mariadb_connection.commit()

        msg.showinfo("Transaction Edited", "Transaction has been edited successfully")

        # redisplay transactions, users, and groups
        displayBal()
        defaultTransactionDisplay()
        defaultDisplay()
        defaultGroupDisplay()

def editTransactionNow(id, index):
    edit = customtkinter.CTkToplevel()
    edit.grab_set()
    edit.title("Add Transaction")
    edit.after(201, lambda: edit.iconbitmap('splitwais.ico'))

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
            st1 = "normal"
            st2 = "disabled"
        else:
            st1 = "disabled"
            st2 = "normal"
        
        customtkinter.CTkButton(transactions, text="Settle", width=50, fg_color="#2B2B2B", state=st2, command=lambda d= id_reference :settleTransaction(d)).grid(column=9, row=5+i, sticky= tk.E, padx=(70,10), pady = (30, 0))
        customtkinter.CTkButton(transactions, text="Delete", width=50, fg_color="#2B2B2B", state=st1, command=lambda d= id_reference :deleteTransaction(d)).grid(column=10, row=5+i, sticky= tk.E, padx=(0,10), pady = (30, 0))
        customtkinter.CTkButton(transactions, text="Edit", width=50, fg_color="#2B2B2B", state=st2, command=lambda  d= id_reference:editTransactionNow(d, i)).grid(column=11, row=5+i, sticky= tk.E, padx=(0,5), pady = (30, 0))
    
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
    msg.showinfo("Transaction Deleted", "Transaction has been deleted successfully")
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

    cursor.execute("SELECT * FROM transaction WHERE transaction_id="+id)
    trans = cursor.fetchone()

    loaner = str(trans[2])
    loanee = str(trans[3])
    amount = str(trans[4])

    
    if (loaner=="11111"):
        borlend = "Lend"
    elif (loanee=="11111"):
        borlend = "Borrow"

    # update balance of user
    if (borlend=="Borrow"):
        if (len(loaner)==5):
            upid = "user_id"
            tbl = "user"
        else:
            upid = "group_id"
            tbl = "`group`"

            # get all the users from a group
            cursor.execute("SELECT user_id FROM has NATURAL JOIN `group` WHERE group_id="+loaner)
            gusers = [x[0] for x in cursor.fetchall()]
            # update user balance from group transaction
            grpamt=str(float(amount)/float(len(gusers)))
            for user in gusers:
                cursor.execute("UPDATE user SET balance=balance+"+grpamt+" where user_id="+str(user))

        cursor.execute("UPDATE user SET balance=balance-"+amount+" where user_id=11111")
        mariadb_connection.commit()
        cursor.execute("UPDATE "+tbl+" SET balance=balance+"+amount+" where "+upid+"="+loaner)
        mariadb_connection.commit()
    elif (borlend=="Lend"):
        if (len(loanee)==5):
            upid = "user_id"
            tbl = "user"
        else:
            upid = "group_id"
            tbl = "`group`"

            # get all the users from a group
            cursor.execute("SELECT user_id FROM has NATURAL JOIN `group` WHERE group_id="+loanee)
            gusers = [x[0] for x in cursor.fetchall()]
            # update user balance from group transaction
            grpamt=str(float(amount)/float(len(gusers)))
            for user in gusers:
                cursor.execute("UPDATE user SET balance=balance-"+grpamt+" where user_id="+str(user))

        cursor.execute("UPDATE user SET balance=balance-"+amount+" where user_id=11111")
        mariadb_connection.commit()
        cursor.execute("UPDATE "+tbl+" SET balance=balance-"+amount+" where "+upid+"="+loanee)
        mariadb_connection.commit()
    displayBal()
    defaultDisplay()
    defaultGroupDisplay()

def showUnsettled():
    query = "SELECT * FROM transaction WHERE payment_date IS NULL"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_transaction_scrollable_frame(result)

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
borrow.grid(row=4,column=4, pady=5, padx=5)
lend = customtkinter.CTkButton(tab1, width=75, height=30, text="      Lend      ", corner_radius=5, fg_color="#4B4947", command= lambda: addTransaction("Lend"))
lend.grid(row=4,column=5, pady=5, padx=5)
unsettled = customtkinter.CTkButton(tab1, width=100, height=30, text="Show Unsettled", corner_radius=5, fg_color="#4B4947", command= showUnsettled)
unsettled.grid(row=4,column=6, pady=5, padx=5, sticky="w")

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
    msg.showinfo("Update Success", "User information has been updated.")
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
        if user[1] != 0.00:
            btnstate = "disable"
        else:
            btnstate = "normal"
        customtkinter.CTkButton(users, text="Delete", width=50, fg_color="#2B2B2B", state = btnstate, command=lambda d= id_reference :deleteUser(d)).grid(column=11, row=5+i, sticky= tk.E, padx=(70,10), pady = (30, 0))
        customtkinter.CTkButton(users, text="Edit", width=50, fg_color="#2B2B2B", command=lambda  d= id_reference:editNow(d, i)).grid(column=12, row=5+i, sticky= tk.E, padx=(0,5), pady = (30, 0))

        for data in user:
            search_label = customtkinter.CTkLabel(users, text = data)
            search_label.grid(row=5+i, column= num, padx= (40, 0), pady = (30, 0))
            num +=1 

def searchNow():
    selected = search_drop.get()
    query = ""  # Initialize the variable with a default value

    if selected == "Search by..":
        #since 11111 is the id of the user, it cant be shown in friends list
        query = "SELECT * FROM user where user_id != 11111 order by first_name"
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
    query = "SELECT * FROM user WHERE user_id != 11111 ORDER BY first_name"
    result = cursor.execute(query,)
    result = cursor.fetchall()
    update_scrollable_frame(result)

def deleteUser(id):
    checkBal = "SELECT Balance FROM user WHERE user_id = %s"
    check = (id,)
    checkresult = cursor.execute(checkBal, check)
    checkresult = cursor.fetchall()

    #if the user/friend does not have an existing balance then it can be deleted
    if checkresult[0][0] == 0.00:
        #get groups of the user
        userGroupQuery = "SELECT group_id from has where user_id = %s"
        userGroup = (id,)
        getGroup = cursor.execute(userGroupQuery, userGroup)
        getGroup = cursor.fetchall()

        if getGroup != []:
            #delete from has table first
            hasQuery = "DELETE FROM has WHERE user_id = %s" 
            deleteHas = (id,)
            cursor.execute(hasQuery, deleteHas)
            mariadb_connection.commit()

            for group in getGroup:
                updateMemberCount(group[0])
        
        #delete from users
        query = "DELETE FROM user WHERE user_id = %s"
        toDel = (id, )
        cursor.execute(query, toDel)
        mariadb_connection.commit()
        msg.showinfo("Delete Success", "User has been deleted successfully")
        defaultDisplay()

def viewFriendOutbal():
    query = "select * from USER where Balance > 0 and user_id != 11111 order by balance desc"
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
users.after_idle(defaultDisplay)

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

def editGroup(id, window):
    #update group info using this query
    query = "UPDATE `group` SET group_name = %s WHERE group_id = %s"
    inputs = (groupNameInput.get(), id)
    cursor.execute(query, inputs)
    mariadb_connection.commit()
    defaultGroupDisplay()
    # popup("Group edited", "successfully")
    msg.showinfo("Edit Group Success", "Group has been edited successfully!")
    window.destroy()

def editGroupNow(id):
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

    button = customtkinter.CTkButton(edit, text="Submit Edit", command=lambda: editGroup(id, edit))
    button.pack(padx=10, pady=10)

def deleteGroup(id):
    checkBal = f"select balance from `group` where group_id = {id}"
    balance = cursor.execute(checkBal)
    balance = cursor.fetchall()
    
    if (balance[0][0] == 0):
        query = "DELETE FROM `group` WHERE group_id = %s"
        toDel = (id, )
        cursor.execute(query, toDel)
        deleteHas = "DELETE FROM `has` where group_id=" + str(id)
        cursor.execute(deleteHas)
        mariadb_connection.commit()
        # popup("Group deleted", "successfully")
        msg.showinfo("Delete Group Success", "Group has been deleted successfully!")
        defaultGroupDisplay()
    else:
        msg.showerror(title="Error", message="Group cannot be deleted! Group still has unsettled transaction.")

def deleteGroupLabels():
    for widget in groups.winfo_children():
        widget.destroy()

def update_group_scrollable_frame(result):
    #delete existing labels
    deleteGroupLabels()
    
    for i, group in enumerate(result):
        num = 0 
        id_reference = str(group[0])
        if group[3] == 0:
            btnState = "normal"
        else:
            btnState = "disabled"
        
        customtkinter.CTkButton(groups, text="Delete", width=50, fg_color="#2B2B2B", state=btnState, command=lambda g=id_reference:deleteGroup(g)).grid(column=10, row=5+i, sticky= tk.E, padx=(50,10), pady = (30, 0))
        customtkinter.CTkButton(groups, text="Edit", width=50, fg_color="#2B2B2B", command=lambda g=id_reference:editGroupNow(g)).grid(column=11, row=5+i, sticky= tk.E, padx=(0,5), pady = (30, 0))
        customtkinter.CTkButton(groups, text="Show members", width=50, fg_color="#2B2B2B", command=lambda g =id_reference:showMembers(g)).grid(column=12, row=5+i, sticky= tk.E, padx=(0,5), pady = (30, 0))

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
    query = "SELECT * FROM `group` where balance > 0 ORDER BY balance desc"
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
    button = customtkinter.CTkButton(add, text="Add Group", command=lambda: addGroup(newGroupID.get(), newGroupName.get(), str(1), str(0), add))
    button.pack(padx=10, pady=10)
    
# add group function
def addGroup(gid, gname, mem_no, balance, window):
    checkGroup = f"select group_id from `group` where group_id={gid}"
    resultGroup = cursor.execute(checkGroup)
    resultGroup = cursor.fetchall()
    
    if (resultGroup == [] and len(gid) == 4):
        insertGroup = "INSERT INTO `group` VALUES(" + gid + ",'" + gname + "'" + ","+ mem_no + "," + balance + ");"
        cursor.execute(insertGroup)
        insertHas = "INSERT INTO `has` VALUES(" + str(11111) + ", " + gid + ");"
        cursor.execute(insertHas)
        mariadb_connection.commit()
        defaultGroupDisplay()
        # popup("Group added", "successfully")
        msg.showinfo("Add Group Success", "Group has been added successfully!")
    elif (len(gid) != 4):
        msg.showerror(title="Error", message="Group cannot be added! Group ID length should be 4.")
    else:
        msg.showerror(title="Error", message="Group cannot be added! Group already exists.")
        
    window.destroy()
    
def showMembers(groupId):
    show = customtkinter.CTkToplevel()
    show.grab_set()

    query = "SELECT u.first_name, u.last_name FROM `has` natural join user u where group_id = " + str(groupId) + " ORDER BY u.first_name"
    result = cursor.execute(query)
    result = cursor.fetchall()
    # update_group_scrollable_frame(result)

    label = customtkinter.CTkLabel(show, text="List of Members", font=("Segoe UI", 15, "bold"))
    label.pack()

    for member in result:
        customtkinter.CTkLabel(show, text=member[0] + " " + member[1]).pack()
        
    customtkinter.CTkButton(show, text="Add member", width=50, fg_color="#4B4947", command=lambda: addMember(groupId, show)).pack(pady=5, padx=5)
    
def addMember(groupId, window):
    window.destroy()
    add = customtkinter.CTkToplevel()
    add.grab_set()

    global memberId

    lbl1 = customtkinter.CTkLabel(add, text="Input Friend ID")
    memberId = customtkinter.CTkEntry(add, width=350, height=20)
    lbl1.pack()
    memberId.pack()

    # member parameter is set to 1 initially (self only)
    button = customtkinter.CTkButton(add, text="Confirm", command=lambda: confirmAddMember(groupId, memberId.get(), add))
    button.pack(padx=10, pady=10)

def confirmAddMember(groupId, memberId, window): # need validation
    checkMember = f"select user_id from `has` where user_id={memberId} and group_id={groupId}"
    memberResult = cursor.execute(checkMember)
    memberResult = cursor.fetchall()
    
    if (memberResult == [] and len(memberId) == 5):
        sql_statement = "INSERT INTO `has` VALUES(" + str(memberId) + ", " + str(groupId) + ");"
        cursor.execute(sql_statement)
        mariadb_connection.commit()
        # popup("Member added", "successfully")
        msg.showinfo("Add Member Success", "Member has been added successfully!")
        window.destroy()
        showMembers(groupId)
        updateMemberCount(groupId)
    elif (len(memberId) != 5):
        msg.showerror(title="Error", message="Member cannot be added! Member ID length should be 5.")
    else:
        msg.showerror(title="Error", message="Member cannot be added! Member already in the group.")
 
def updateMemberCount(groupId):
    sql_statement = "UPDATE `group` SET number_of_members=(SELECT COUNT(user_id) FROM `has` WHERE group_id=" + str(groupId) + ") WHERE group_id=" + str(groupId)
    cursor.execute(sql_statement)
    mariadb_connection.commit()
    defaultGroupDisplay()

# def popup(funx, status):
#     pop = customtkinter.CTkToplevel()
#     pop.wm_overrideredirect(True)
#     pop.geometry("+500+1100")
    
#     def destroy_popup():
#         if pop.winfo_exists():
#             pop.destroy()
    
#     customtkinter.CTkLabel(pop, text=f"{funx} {status}!").pack()
#     pop.after(3000, destroy_popup)
    
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
groups = customtkinter.CTkScrollableFrame(tab3, width = 650, height = 350, fg_color="#4B4947", corner_radius=0)
groups.grid(row=3, column=1, columnspan=6, pady=(0,5))

# shows all groups at the start
groups.after_idle(defaultGroupDisplay)

groupLabel = customtkinter.CTkLabel(tab3, width=668, height= 30, fg_color = "#242424", text= "")
groupLabel.grid(row=2, column=1, columnspan=6, pady= (10,0), padx = (0,0))
groupIDLabel=customtkinter.CTkLabel(tab3, width=30, height= 20, fg_color = "#242424", text= "Group ID")
groupIDLabel.place(x=225 , y =120)
groupNameLabel=customtkinter.CTkLabel(tab3, width=50, height= 20, fg_color = "#242424", text= "Group Name")
groupNameLabel.place(x=325 , y =120)
memberNumberLabel=customtkinter.CTkLabel(tab3, width=50, height= 20, fg_color = "#242424", text= "Member Count")
memberNumberLabel.place(x=425 , y =120)
groupBalanceLabel=customtkinter.CTkLabel(tab3, width=50, height= 20, fg_color = "#242424", text= "Balance")
groupBalanceLabel.place(x=525 , y =120)


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