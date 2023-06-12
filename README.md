# CMSC-127-Project
# Authors:
    -- Bautista, Adrianne Mae
    -- Fabico, Marthine Angel
    -- Quinlat, Angelo Jasper

# Application Specs
    # TRANSACTION  
        1. Search Function
            - user is allowed to search by transaction ID
            - there is also a feature that the user can custom suearch (by transaction name, friend ID and group ID)
                ** note that the result of search is only where the main user "11111" has transaction with*
        2. Show History
            - display all transaction
        3. Filter by month
            - displays transaction based on the month where transaction is created
        4. Delete
            - user can delete transaction once it is settled
            - desabled if not yet settled
        5. Settled
            - mean that the transaction is already paid
            - payment date is updated once settled
        6. Edit
            - user can edit the transaction name, loanee and loaner (ID) and transaction date
        7. Borrow
            - User (11111) is set as loaner
            - automatically updates total balance
        8. Lend
            - User (11111) is set as loanee
            - automatically updates total balance
        9. Show all unsettled
            - displays unsettled transaction
        10. Total Balance
            - shows current balance of the user 11111 and updates when there is a new transaction
        

    # USER
        1. Search Function
            - search bar will be search data based on the dropdown (First Name, Middle Name, Last Name and user ID)
        2. View All
            - Display all existing friends
        3. Outstanding Records
            - distaplay user that has current balance in descending order
        4. Delete
            - it is disabled when the user has current balance
            - can only be deleted if user balance is 0
            - once user is deleted it will automatically update the member count of the group where user (being deleted) belongs
        5. Edit
            - User can edit First name, MIddle Name and Last Name of Friends
        6. Add Friend
            - User can add friend

    # GROUP
        1. Search
            - can search by group name or group ID
            - display group being searched
        2. Add Group
            - can add group
            - the user (11111), is the default first member of the newly created group
        3. Show Members
            - opens a new window that shows current members and ables to add an existing user (friend) to the group
        4. Show All groups
            - display exisitng groups
        5. Show outstanding group
            - display group with exisitng balance in descending order
        6. Delete
            - delete is disabled when it still has balance
        7. Edit
            - User can only edit group name
        8. Total Group Balance
            - shows current balance of the group and updates when there is a new transaction
        
        